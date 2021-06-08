from django import forms
from accounts.models import UserRegistration

from .models import Property

PAYMENT_CHOICES= [
    ('one month', 'one month'),
    ('two months', 'two months'),
    ('three months', 'three months'),
    ('four months', 'four months'),
    ('five months', 'five months'),
    ('six months', 'six months'),
    ]

STATUS= [
    ('rent', 'Rent'),
    ('sale', 'Sale'),
    
    
    ]

TYPES= [
    ('houses', 'Houses'),
    ('apartments', 'Apartments'),
    ('offices', 'Offices'),
    ('commercial', 'Commercial'),
    
    ]


class PropertyForm(forms.ModelForm):
    # customer     = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    title     = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Title'}))
    status     = forms.CharField(required=False, widget=forms.Select(choices=STATUS))
    types     = forms.CharField(required=False, widget=forms.Select(choices=TYPES))
    price     = forms.CharField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Price'}))
    area     = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Area'}))
    bedrooms     = forms.CharField(required=False, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Bedrooms'}))
    bathrooms     = forms.CharField(required=False, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Bathrooms'}))
    image_one     = forms.ImageField(required=False)
    image_two     = forms.ImageField(required=False)
    image_three     = forms.ImageField(required=False)
    image_four     = forms.ImageField(required=False)
    image_five     = forms.ImageField(required=False)
    location     = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Location'}))
    description    = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Description'}))
    
    

    class Meta:
        model = Property
        fields = (
            'title',
            'status',
            'types',
            'price',
            'area',
            'bedrooms',
            'bathrooms',
            'image_one',
            'image_two',
            'image_three',
            'image_four',
            'image_five',
            'location',
            'description'
            
            )

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop("request")
    #     super(PropertyForm, self).__init__(*args, **kwargs)
    #     self.fields["customer"].queryset = UserRegistration.objects.filter(user=self.request.user)
        # self.fields["whatever"].queryset = WhateverModel.objects.filter(user=self.request.user)
