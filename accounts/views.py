from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from properties.models import Property, FeaturedProperty
from accounts.models import UserRegistration, Subscription, Plan
from accounts.forms import SubscriptionForm
# Create your views here.

@login_required
def user_home(request):
    return render(request, 'home/user_index.html')
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
def user_profile(request):
    properties = Property.objects.all()
    users = UserRegistration.objects.all()    
    return render(request, 'home/user_profile.html', {'properties':properties, 'users': users})

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
    
       
    