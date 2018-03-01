from django.conf.urls import url
from . import views         
urlpatterns = [
    url(r'^$', views.index),  
    url(r'^watchlist$', views.watchlist),
    url(r'^upcoming$', views.upcoming),
    url(r'^current$', views.current),
    url(r'^toprated$', views.toprated),
    url(r'search/(?P<search_option>\w+)/$', views.result), 
    url(r'search/searchpage$', views.search), 
    url(r'^add$', views.add),
    url(r'^(?P<id>\d+)$', views.show),
    url(r'^(?P<id>\d+)/add_list$', views.add_list),
    url(r'^(?P<id>\d+)/rm_list$', views.rm_list),
    url(r'^(?P<id>\d+)/add_review$', views.add_review),
    url(r'^(?P<id>\d+)/(?P<rev>\d+)/rm_review$', views.rm_review),
]
