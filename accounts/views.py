from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from properties.models import Property, FeaturedProperty
from accounts.models import UserRegistration, Subscription, Plan, UpdateProfile
from accounts.forms import SubscriptionForm, EditUserRegistrationForm, UserRegistrationForm
from django.contrib import messages
from rest_framework.views import APIView
# from rest_framework.response import response
from rest_framework import status

# Create your views here.

@login_required
def user_home(request):
    property_list = Property.objects.all()
    properties = Property.objects.filter().order_by('-created_on')[0:20]
    featuredProperty_list = FeaturedProperty.objects.all()
    featuredProperties = FeaturedProperty.objects.filter().order_by('-created_on')[0:20]
    return render(request, 'home/user_index.html', {'property_list': property_list,'featuredProperty_list': featuredProperty_list,'properties': properties,'featuredProperties': featuredProperties})
@login_required
def user_dashboard(request): 
    
    # users = UserRegistration.objects.all()
    # properties = Property.objects.all()
    customer_properties = Property.objects.filter(customer=request.user.id)
    customer_featured_properties = FeaturedProperty.objects.filter(customer=request.user.id)
    # customer = get_object_or_404(UserRegistration)
    # properties = customer.properties_set.all()
       
    return render(request, 'home/user_dashboard.html', {'props': customer_properties, 'featured_props':customer_featured_properties})
    # return render(request, 'home/user_dashboard.html', {'properties':properties, 'customer': customer})

@login_required
def user_profile(request, id):
    properties = Property.objects.all()
    users = UserRegistration.objects.all()
    object = get_object_or_404(UserRegistration, id=id)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES or None, instance=object)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            messages.success(request, "Profile Update Successful." )
            return redirect('/accounts/user_dashboard')
        else:
            print(form.cleaned_data)
            messages.error(request, "Profile Update not successful")
            return render(request, 'home/user_dashboard.html',{'properties':properties, 'users': users, 'form': form})
    form = EditUserRegistrationForm(request.POST or None, instance=object)
    return render(request, 'home/user_profile.html', {'properties':properties, 'users': users, 'form': form})


    
@login_required
def view_profile(request):
    properties = Property.objects.all()
    users = UserRegistration.objects.all()
    
    return render(request, 'home/view_profile.html', {'properties':properties, 'users': users})

@login_required
def subscription_package(request): 
    # users = UserRegistration.objects.all()
    # properties = Property.objects.all()
    customer_sub = Subscription.objects.filter(customer=request.user.id)
    subscription_plan = Plan.objects.all()
    if request.method == 'POST':
        form = SubscriptionForm(request.POST or None)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.customer_id = int(request.user.id)
            print(request.user.id)
            print(type(request.user.id))
            prop.save()
            messages.success(request, "Subscription Successfully" )
            return redirect('/accounts/subscription',{'form':form})
        else:
            messages.error(request, "Subscription Not Successfully" )
            return redirect('/accounts/subscription',{'form':form})
    else:   
        form = SubscriptionForm
        return render(request, 'home/subscription_package.html', {'form':form, 'props': customer_sub, 'subscription_plan': subscription_plan})
    
       
    