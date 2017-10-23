from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^homepage$', views.homepage),
    url(r'^processquote$', views.processquote),
    url(r'^addfavorite/(?P<quote_id>\d+)$', views.addfavorite),
    url(r'^removefavorite/(?P<quote_id>\d+)$', views.removefavorite),
    url(r'^users/(?P<user_id>\d+)$', views.userpage),
]