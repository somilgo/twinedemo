from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^main/', views.main, name='main'),
    url(r'^job/(?P<pk>[0-9]+)/$', views.job, name='job'),
    url(r'^recruiter/(?P<pk>[0-9]+)/$', views.recruiter, name='recruiter'),
]