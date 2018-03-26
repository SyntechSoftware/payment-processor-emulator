from django.views.generic import ListView, DetailView, FormView, View, TemplateView
from django.views.generic.edit import BaseUpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from datetime import date
import json
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

from .models import Transaction, BillingParams
from .forms import BillingParamsForm

from .utils import process_pay


class Dashboard(ListView):
    model = Transaction
    template_name = 'dashboard/main.html'
    paginate_by = 30

    def get_queryset(self):
        return super(Dashboard, self).get_queryset().filter(supplier = self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Dashboard, self).dispatch(*args, **kwargs)


class DashboardDetail(DetailView):
    model = Transaction
    template_name = 'dashboard/detail.html'

    def get_queryset(self):
        return super(DashboardDetail, self).get_queryset().filter(supplier = self.request.user)

    def get_context_data(self, **kwargs):
        context = super(DashboardDetail, self).get_context_data(**kwargs)
        context['params'] = json.loads(self.object.params)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardDetail, self).dispatch(*args, **kwargs)


class DashboardParams(FormView):
    form_class = BillingParamsForm
    model = BillingParams
    template_name = 'dashboard/params.html'

    def get_object(self, queryset=None):
        obj, created = BillingParams.objects.get_or_create(supplier=self.request.user)
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(DashboardParams, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.form_class(request.POST or None, instance=self.object)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('dashboard_param'))
        return self.render_to_response(self.get_context_data())

    def get_form_kwargs(self):
        kwargs = super(DashboardParams, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardParams, self).dispatch(*args, **kwargs)


class IFrameView(TemplateView):
    template_name = 'iframe.html'

    def get_context_data(self, **kwargs):
        context = super(IFrameView, self).get_context_data(**kwargs)
        params = { key: self.request.GET.get(key, '') for key in self.request.GET }
        params['supplier'] = getattr(self, 'supplier', None)
        context['values'] = params
        context['months'] = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        context['years'] = range(date.today().year % 100, date.today().year%100 + 20)
        return context

    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        User = get_user_model()
        supplier = User.objects.filter(username=kwargs.get('supplier')).first()
        if not supplier:
            return HttpResponse("<body>Error: <span>Not supplier not found</span></body>")
        self.supplier = supplier
        return super(IFrameView, self).get(request, *args, **kwargs)


class IFrameProcess(TemplateView):
    template_name = "process.html"
    http_method_names = ['post']

    def __init__(self, **kwargs):
        super(IFrameProcess, self).__init__(**kwargs)
        self.results = {}
        self.to_url = '/done/'

    def get_context_data(self, **kwargs):
        context = super(IFrameProcess, self).get_context_data(**kwargs)
        context['values'] = self.results
        context['to_url'] = self.to_url
        return context

    @xframe_options_exempt
    def post(self, request, *args, **kwargs):
        User = get_user_model()
        supplier = User.objects.filter(username = request.POST.get('supplier')).first()
        if not supplier:
            return HttpResponse("<body>Error: <span>Not supplier not found</span></body>")
        params = { key: request.POST.get(key, '') for key in request.POST if not key == 'csrfmiddlewaretoken' }
        results = process_pay(params, supplier, True)
        self.results = results
        self.to_url = results.get('to_url')
        if self.to_url:
            del results['to_url']

        return super(IFrameProcess, self).get(request, *args, **kwargs)


class IFrameDone(View):
    @xframe_options_exempt
    def post(self, request, *args, **kwargs):
        return HttpResponse("""
        <html><body>%s</body></html>""" % ("Success!" if request.POST.get('Response') else "Fail!"))

    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        return HttpResponse("""
        <html><body>%s</body></html>""" % ("Success!" if request.POST.get('Response') else "Fail!"))

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(IFrameDone, self).dispatch(request, *args, **kwargs)


class ProcessView(View):
    def post(self, request, *args, **kwargs):
        User = get_user_model()
        supplier = User.objects.filter(username = request.POST.get('supplier')).first()
        if not supplier:
            return HttpResponse("<body>Error: <span>Not supplier not found</span></body>")
        params = { key: request.POST.get(key, '') for key in request.POST }
        return HttpResponse(process_pay(params, supplier))

    def get(self, request, *args, **kwargs):
        User = get_user_model()
        supplier = User.objects.filter(username = request.GET.get('supplier')).first()
        if not supplier:
            return HttpResponse("<body>Error: <span>Not supplier not found</span></body>")
        params = { key: request.GET.get(key, '') for key in request.GET }
        return HttpResponse(process_pay(params, supplier))

