from django.urls import path
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import TemplateView
from properties import views

urlpatterns = [

    path('add_property/', views.add_property, name='add_property'),
    path('my_properties/', views.my_properties, name='my_properties'),
    

    ]
