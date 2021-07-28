from django.urls import path
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import TemplateView
from properties import views

app_name = "properties"

urlpatterns = [

    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate'),    
    path('add_property/', views.add_property, name='add_property'),
    path('my_properties/', views.my_properties, name='my_properties'),
    path('update_property/<str:pk>/', views.update_property, name='update_property'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('<slug:slug>/', views.PropertyDetail_two.as_view(), name='property_detail_two'),

    
    

    ]
