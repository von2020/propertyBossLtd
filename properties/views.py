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
            get_plan = Plan.objects.get(plan_type='Free')
            UserPlan.objects.create(user=obj, plan=get_plan)
            messages.success(request, "Registration Successful." )
            return redirect('/')
        else:
            print(form.cleaned_data)
            messages.error(request, "Sign Up not successful")
            return render(request, 'home/index.html',{'property_list': property_list,'featuredProperty_list': featuredProperty_list,'properties': properties,'featuredProperties': featuredProperties,'form':form})
        
    else: 
        form = UserRegistrationForm()   
    return render(request, 'home/index.html',{'property_list': property_list,'featuredProperty_list': featuredProperty_list,'properties': properties,'featuredProperties': featuredProperties,'form':form})


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
            messages.success(request, "Property Added Successfully" )
            return redirect('/accounts/user_dashboard',{'form':form})
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





def logoutUser(request):
    logout(request)
    messages.success(request, "You are logged out")
    return redirect('/')