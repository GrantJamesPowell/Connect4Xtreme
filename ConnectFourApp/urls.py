__author__ = 'grantpowell'

from django.conf.urls import url

from . import views

urlpatterns = [  # Mostly User Facing Stuff, Like account create and index
    url('^$', views.RedirectView.as_view(url='https://google.com'), name='index'),
    url('^createaccount$', views.UserCreate.as_view(), name='accountcreate'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),

] + [  # The Game Ajax Functions


]