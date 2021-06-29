from django import forms
from accounts.models import UserRegistration, Subscription, UpdateProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm

User = get_user_model()

ROLE_CHOICES= [
    ('agent', 'agent'),
    ('developer', 'developer'),
    ('landlord', 'landlord'),
    ]

class UserRegistrationForm(UserCreationForm):
    firstname = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Firstname'}))
    lastname  = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Lastname'}))
    email     = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'}))
    role      = forms.CharField(required=True, widget=forms.Select(choices=ROLE_CHOICES))
    phone_number = forms.CharField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Phone Number'}))
    whatsapp_phone_number = forms.CharField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'WhatsApp Phone Number'}))
    

    class Meta:
        model = User
        fields = (
            'firstname',
            'lastname',
            'email',
            'role',
            'phone_number',
            'whatsapp_phone_number',
            'password1',
            'password2'
            )


    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.firstname = self.cleaned_data['firstname']
        user.lastname = self.cleaned_data['lastname']
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        user.phone_number = self.cleaned_data['phone_number']
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    email     = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'email'}))
    password1 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = (
            'email',
			'password1'
            )

    def save(self, commit=False):
        user = super(LoginForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.password1 = self.cleaned_data['password1']
        if commit:
            user.set_password(user.password)
            user.save()
            return user

PLAN_CHOICES = [
    ('standard', 'Standard'),
    ('premium', 'Premium'),
    ('gold', 'Gold'),
]

class SubscriptionForm(forms.ModelForm):
    duration = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Duration'}))
    amount = forms.CharField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Amount'}))
    listings = forms.CharField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Listings'}))
    plan = forms.MultipleChoiceField(
        widget=forms.RadioSelect,
        choices=PLAN_CHOICES,
    )
    # is_standard = forms.CharField( widget=forms.CheckboxSelectMultiple)
    # is_premium  = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Message'}))
    # is_gold     = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Message'}))

    class Meta:
        model = Subscription
        fields = (
            'duration',
            'amount',
            'listings',
            'plan',
            )


class EditUserRegistrationForm(UserCreationForm):
    firstname    = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Firstname'}))
    lastname     = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Lastname'}))
    email        = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'}))
    role         = forms.CharField(required=False, widget=forms.Select(choices=ROLE_CHOICES))
    phone_number = forms.CharField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Phone Number'}))
    
    

    class Meta:
        model = User
        fields = (
            'firstname',
            'lastname',
            'email',
            'role',
            'phone_number'
            
            
            )

    def save(self, commit=True):
        user = super(EditUserRegistrationForm, self).save(commit=False)
        user.firstname = self.cleaned_data['firstname']
        user.lastname = self.cleaned_data['lastname']
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        user.phone_number = self.cleaned_data['phone_number']


class EditProfileForm(UserCreationForm):
    
    

    class Meta:
        model = UpdateProfile
        fields = (
            'profile_pic',
            'id_card'  
            )

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        user.profile_pic = self.cleaned_data['profile_pic']
        user.id_card = self.cleaned_data['id_card']
    