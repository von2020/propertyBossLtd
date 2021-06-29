from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from properties.models import Property, FeaturedProperty
from accounts.models import UserRegistration, Subscription, Plan, UpdateProfile, UserPlan, PayHistory
from accounts.forms import SubscriptionForm, EditUserRegistrationForm, UserRegistrationForm, EditProfileForm
from django.contrib import messages
from datetime import datetime, timedelta, timezone, tzinfo, date
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
# from rest_framework.response import response
from rest_framework import status
import requests
import json

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
    if request.method == 'POST':
        u_form = EditUserRegistrationForm(request.POST or None, instance=request.user)
        p_form = EditProfileForm(request.POST, request.FILES or None, instance=request.user.profile)
        print('it is POST')
        if u_form.is_valid() and p_form.is_valid():
            print('u_form', u_form.cleaned_data)
            print('p_form', p_form.cleaned_data)
            u_form.save()
            p_form.save()
            messages.success(request, "Profile Update Successful.")
            return redirect('/accounts/user_profile')
        else:
            print('Not VALID')
            print('u_form', u_form.cleaned_data)
            print('p_form', p_form.cleaned_data)
            messages.error(request, "Profile Not Updated Successful.")
            return redirect('/accounts/user_profile')

    else:
        print('GET')
        u_form = EditUserRegistrationForm(instance=request.user)
        p_form = EditProfileForm(instance=request.user.profile)
       
        

    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'home/user_profile.html', context)


    
@login_required
def view_profile(request):    
        properties = Property.objects.all()
        users = UserRegistration.objects.all()
        try:
            user_plan = UserPlan.objects.get(user=request.user)
            subscriptions = Subscription.objects.filter(user_plan=user_plan).exists()
            print(subscriptions)
            print(user_plan)
            if subscriptions == False:
                print('Hello')
                return redirect('/accounts/view_profile')
            else:
                subscription = Subscription.objects.filter(user_plan=user_plan).last()
                print('see', subscription)
            return render(request, 'home/view_profile.html', {'properties':properties, 'users': users, 'sub':subscription})
            
        except:

            return render(request, 'home/view_profile.html', {'properties':properties, 'users': users})
    
@login_required
def subscription_package(request): 
    return render(request, 'home/subscription_package.html')
    
       
@login_required
def subscribe(request): 
    plan = request.GET.get('sub_plan')
    fetch_plan = Plan.objects.filter(plan_type=plan).exists()
    if fetch_plan == False:
        return redirect('subscribe')
    membership = Plan.objects.get(plan_type=plan)
    price = float(membership.amount)*100
    price = int(price)
    print('sk', 'Bearer ' +settings.PAYSTACK_SECRET_KEY)
    def init_payment(request):
        url = 'https://api.paystack.co/transaction/initialize'
        headers = {
            'Authorization': 'Bearer ' +settings.PAYSTACK_SECRET_KEY,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        datum = {
            "email": request.user.email,
            "amount": price
        }
        x = requests.post(url, data=json.dumps(datum), headers=headers)
        if x.status_code != 200:
            return str(x.status_code)

        results = x.json()
        return results
    initialized = init_payment(request)
    print(initialized['data']['authorization_url'])
    amount = price/100
    instance = PayHistory.objects.create(amount=amount, payment_for=membership, user=request.user, paystack_charge_id=initialized['data']['reference'], paystack_access_code=initialized['data']['access_code'])
    UserPlan.objects.filter(user=instance.user).update(reference_code=initialized['data']['reference'])
    link = initialized['data']['authorization_url']
    print('link',link)
    return HttpResponseRedirect(link)
    print(plan)
    print(membership.amount)
    return render(request, 'home/subscribe.html')


def call_back_url(request):
    reference = request.GET.get('reference')
    print('reference', reference)
    check_pay = PayHistory.objects.filter(paystack_charge_id=reference).exists()
    if check_pay == False:
        print('Error')
    else:
        payment = PayHistory.objects.get(paystack_charge_id=reference)

        def verify_payment(request):
            url = 'https://api.paystack.co/transaction/verify/' +reference
            headers = {
                'Authorization': 'Bearer ' +settings.PAYSTACK_SECRET_KEY,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }
            datum = {
                "reference": payment.paystack_charge_id,
            
            }
            
            x = requests.get(url, data=json.dumps(datum), headers=headers)
            if x.status_code != 200:
                return str(x.status_code)

            results = x.json()
            return results
    initialized = verify_payment(request)
    print(initialized['data']['status'])
    print(initialized['data']['reference'])
    if initialized['data']['status'] == 'success':
        PayHistory.objects.filter(paystack_charge_id=initialized['data']['reference']).update(paid=True)
        new_payment = PayHistory.objects.get(paystack_charge_id=initialized['data']['reference'])
        instance = Plan.objects.get(id=new_payment.payment_for.id)
        sub = UserPlan.objects.filter(reference_code=initialized['data']['reference']).update(plan=instance)
        user_plan = UserPlan.objects.get(reference_code=initialized['data']['reference'])
        Subscription.objects.create(user_plan=user_plan, expires_in=datetime.now().date() + timedelta(days=user_plan.plan.duration))
        print('instance', instance)
        return redirect('/accounts/subscribed')
    return render(request, 'home/payment.html')


def subscribed(request):
    
    user_plan = UserPlan.objects.get(user=request.user)
        
    subscription = Subscription.objects.filter(user_plan=user_plan).last()
    print('see', subscription)
    return render(request, 'home/subscribed.html', {'sub':subscription})
            
    

        