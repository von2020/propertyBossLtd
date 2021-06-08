from django.shortcuts import render, redirect, HttpResponse
from accounts import forms
from accounts.forms import UserRegistrationForm, LoginForm
from properties.forms import PropertyForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from accounts.models import UserRegistration
from properties.models import Property, FeaturedProperty
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


# Create your views here.

def home(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful." )
            return redirect('/home')
        else:
            messages.error(request, "Sign Up not successful")
            return render(request, 'home/index.html',{'form':form})
        
    else: 
        form = UserRegistrationForm()   
    return render(request, 'home/index.html',{'form':form})


def loginPage(request):
    # cats = ProductCategory.objects.filter(parent=None)
    if request.method == 'POST':
        # form = LoginForm(data=request.POST)
    
        # if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
        
            if user is not None:
                # if user.is_active:
                    login(request, user)
                    messages.success(request, "You are now logged in " )
                    return redirect('/accounts/user_home')
            else:
                messages.error(request, "You are not a registered customer, CLICK ON MY ACCOUNT TO SIGN UP")
                return render(request, 'home/index.html')
            
    else:
        form = LoginForm()
        return render(request, 'home/index.html', {'form':form})

@login_required
def add_property(request): 
    if request.method == 'POST':
        form = PropertyForm(request.POST or None)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.customer_id = int(request.user.id)
            print(request.user.id)
            print(type(request.user.id))
            prop.save()
            messages.success(request, "Property Added Successfully" )
            return redirect('/accounts/user_dashboard',{'form':form})
        else:
            messages.error(request, "Property Not Added Successfully" )
            return redirect('/accounts/user_dashboard',{'form':form})
    else:   
        form = PropertyForm()
        return render(request, 'home/add_property.html', {'form':form})

@login_required
def my_properties(request): 
    # users = UserRegistration.objects.all()
    # properties = Property.objects.all()
    customer_properties = Property.objects.filter(customer=request.user.id)
    customer_featured_properties = FeaturedProperty.objects.filter(customer=request.user.id)
    
       
    return render(request, 'home/my_properties.html', {'props': customer_properties, 'featured_props':customer_featured_properties})
    # return render(request, 'home/user_dashboard.html', {'properties':properties, 'customer': customer})





def logoutUser(request):
    logout(request)
    messages.success(request, "You are logged out")
    return redirect('/home')