from django.views.generic import ListView, DetailView, FormView, View, TemplateView
from django.views.generic.edit import BaseUpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from .models import Transaction, BillingParams
from .forms import BillingParamsForm


class Dashboard(ListView):
    model = Transaction
    template_name = 'dashboard/main.html'
    paginate_by = 30

    def get_queryset(self):
        return super(Dashboard, self).get_queryset().filter(supplier = self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Dashboard, self).dispatch(*args, **kwargs)


class DashboardDetail(ListView):
    model = Transaction
    template_name = 'dashboard/detail.html'

    def get_queryset(self):
        return super(DashboardDetail, self).get_queryset().filter(supplier = self.request.user)

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


class IFrameProcess(View):
    def post(self, request, *args, **kwargs):
        return HttpResponse("ok")


class ProcessView(View):
    def post(self, request, *args, **kwargs):
        return HttpResponse("ok")

