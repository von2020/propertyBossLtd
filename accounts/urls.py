from django.urls import path
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import TemplateView
from properties import views
from accounts import views

urlpatterns = [

    path('user_home/', views.user_home, name='user_home'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('subscription/', views.subscription_package, name='subscription_package'),
    

    ]
