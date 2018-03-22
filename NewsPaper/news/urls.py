from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^addNews/$', views.addNews, name='addNews'),
    url(r'^manageNews/$', views.manageNews, name='manageNews'),
    url(r'^getNews/$', views.getNews, name='getNews'),
    url(r'^newsSearch/$', views.newsSearch, name='newsSearch'),
]