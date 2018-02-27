from django.conf.urls import url
from . import views     
urlpatterns = [
    url(r'^$', views.logpage),
    url(r'^regpage/$', views.regpage),
    url(r'^regpage/register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^logout$', views.logout),
    url(r'^(?P<id>\d+)$', views.profile),
    url(r'^(?P<id>\d+)/update$', views.update),
]
