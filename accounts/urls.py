from django.urls import path
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_view
from properties import views
from accounts import views

urlpatterns = [

    path('user_home/', views.user_home, name='user_home'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('user_profile/<int:id>/', views.user_profile, name='user_profile'),
    path('subscription/', views.subscription_package, name='subscription_package'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscribed/', views.subscribed, name='subscribed'),
    path('payment/', views.call_back_url, name='payment'),
    path('reset_password/', auth_view.PasswordResetView.as_view(template_name="home/reset-password.html"), name='reset_password'),
    path('reset_password_sent/', auth_view.PasswordResetDoneView.as_view(template_name="home/reset-password-sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name="home/reset-password-confirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_view.PasswordResetCompleteView.as_view(template_name="home/reset-password-complete.html"), name='password_reset_complete'),

    ]
