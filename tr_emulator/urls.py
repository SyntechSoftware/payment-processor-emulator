"""tr_emulator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView
from .views import IFrameView, IFrameProcess,ProcessView, DashboardParams, DashboardDetail, Dashboard

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^dashboard/$', Dashboard.as_view(), name='dashboard'),
    url(r'^dashboard/(?P<pk>\d+)/$', DashboardDetail.as_view(), name='dashboard_detail'),
    url(r'^dashboard/params/$', DashboardParams.as_view(), name='dashboard_param'),
    url(r'^(?P<supplier>[a-z0-9]+)/', IFrameView.as_view()),
    url(r'^(?P<supplier>[a-z0-9]+)/iframe.php', IFrameView.as_view()),
    url(r'^process/$', IFrameProcess.as_view()),
    url(r'^cgi-bin/tranzila71u.cgi$', ProcessView.as_view()),
    url(r'^.*$', RedirectView.as_view(url='accounts/login/', permanent=False)),
]
