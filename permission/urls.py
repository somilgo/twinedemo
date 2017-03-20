from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^main/', views.main, name='main'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^sign_up/', views.sign_up, name='sign_up'),
    url(r'^create_job/', views.create_job, name='create_job'),
    url(r'^job/(?P<pk>[0-9]+)/$', views.job, name='job'),
    url(r'^recruiter/(?P<pk>[0-9]+)/$', views.recruiter, name='recruiter'),
]