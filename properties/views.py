from django.shortcuts import render, redirect, HttpResponse
from accounts import forms
from accounts.forms import UserRegistrationForm, LoginForm
from properties.forms import PropertyForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from accounts.models import UserRegistration, Plan, UserPlan, Subscription, PayHistory
from properties.models import Property, FeaturedProperty
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from hitcount.views import HitCountDetailView
from django.views.generic import View
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import generate_token 
from django.core.mail import EmailMessage
from datetime import datetime, timedelta, timezone, tzinfo, date

today = date.today()


# Create your views here.

def home(request):
    property_list = Property.objects.all()
    properties = Property.objects.filter().order_by('-created_on')[0:20]
    featuredProperty_list = FeaturedProperty.objects.all()
    featuredProperties = FeaturedProperty.objects.filter().order_by('-created_on')[0:20]
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            obj = form.save()

            email = obj.email
            current_site=get_current_site(request)
            email_subject='Activate Your Account'
            message=render_to_string('home/activate.html',
            {
                'user':form,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(obj.id)),
                'token':generate_token.make_token(obj)
            }) 
            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )

            email_message.send()

            get_plan = Plan.objects.get(plan_type='Free')
            instance = UserPlan.objects.create(user=obj, plan=get_plan)
            messages.success(request, "Registration Successful." )
            return redirect('/')
        else:
            print(form.cleaned_data)
            messages.error(request, "Sign Up not successful")
            return render(request, 'home/index.html',{'property_list': property_list,'featuredProperty_list': featuredProperty_list,'properties': properties,'featuredProperties': featuredProperties,'form':form})
        
    else: 
        form = UserRegistrationForm()   
    return render(request, 'home/index.html',{'property_list': property_list,'featuredProperty_list': featuredProperty_list,'properties': properties,'featuredProperties': featuredProperties,'form':form})



class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=UserRegistration.objects.get(pk=uid)
        except Exception as identifier:    
            user=None

        if user is not None and generate_token.check_token(user, token):
            user.is_active=True
            user.save( )
            messages.success(request, "Account Activated Successfully." )
            return redirect('/')
        else:
            return render(request, 'home/activate_failed.html', status=401)


class PropertyDetail(HitCountDetailView):
    model = Property
    template_name = 'home/single_property.html'
    context_object_name = 'property'
    form_class = UserRegistrationForm
    slug = 'slug'
    count_hit = True
    
        
    def get_context_data(self, *args, **kwargs):
        context = super(PropertyDetail, self).get_context_data(**kwargs)
        context.update({
        # 'cats' : ProductCategory.objects.filter(parent=None),
        'property_count' : Property.objects.count(),
        'form' : UserRegistrationForm(self.request.POST or None),
        
        })
        return context

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm()
        if form.is_valid():
            form.save()
            self.object = self.get_object()
            context = super(UserRegistrationForm, self).get_context_data(**kwargs)
            context['form'] = UserRegistrationForm
            return self.render_to_response(context=context)

        else:
            self.object = self.get_object()
            context = super(PropertyDetail, self).get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response( context=context)


class PropertyDetail_two(HitCountDetailView):
    model = Property
    template_name = 'home/user_single_property.html'
    context_object_name = 'property'
    form_class = UserRegistrationForm
    slug = 'slug'
    count_hit = True
    
        
    def get_context_data(self, *args, **kwargs):
        context = super(PropertyDetail_two, self).get_context_data(**kwargs)
        context.update({
        # 'cats' : ProductCategory.objects.filter(parent=None),
        'property_count' : Property.objects.count(),
        'form' : UserRegistrationForm(self.request.POST or None),
        
        })
        return context

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm()
        if form.is_valid():
            form.save()
            self.object = self.get_object()
            context = super(UserRegistrationForm, self).get_context_data(**kwargs)
            context['form'] = UserRegistrationForm
            return self.render_to_response(context=context)

        else:
            self.object = self.get_object()
            context = super(PropertyDetail_two, self).get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response( context=context)


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
        form = PropertyForm(request.POST, request.FILES or None)
        if form.is_valid():
            print(form.cleaned_data)
            prop = form.save(commit=False)
            prop.customer_id = int(request.user.id)        
            print(request.user.id)
            print(type(request.user.id))
            prop.save()
            print('prop', prop)
            messages.success(request, "Property Added Successfully" )
            return redirect('/accounts/user_dashboard',{'form':form, 'prop':prop})
        else:
            print(form.cleaned_data)
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


def update_property(request, pk):
    
    user_plan = UserPlan.objects.get(user=request.user)
    subscriptions = Subscription.objects.filter(user_plan=user_plan).exists()
    print(subscriptions)
    print(user_plan)
    users = UserRegistration.objects.all()
    
    try:
              
        if subscriptions == False:
            print('Hello')
            return redirect('/properties/my_properties')
        else:
            subscription = Subscription.objects.filter(user_plan=user_plan).last()
            print('see', subscription)
            properties = Property.objects.get(id=pk)
            if request.method == 'POST':
                form = PropertyForm(request.POST, request.FILES or None, instance=properties)
                if form.is_valid():
                    form.save()
                    return redirect('/properties/my_properties')
            form = PropertyForm(request.POST or None, instance=properties)
            context ={'form': form,'users': users, 'sub':subscription }
            return render(request, 'home/updateProperty.html', context)
    except:
        messages.error(request, "Network Error" )
        return render(request, 'home/my_properties.html', context)


def delete(request, id):
    properties = Property.objects.filter(id=id)
    properties.delete()
    return redirect('/properties/my_properties')



def logoutUser(request):
    logout(request)
    messages.success(request, "You are logged out")
    return redirect('/')