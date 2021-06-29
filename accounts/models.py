from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# from properties.models import Property
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from datetime import datetime, timedelta, timezone, tzinfo, date


# Create your models here.
class UpdateProfile(models.Model):
    profile_pic       = models.ImageField(upload_to='profile_pics/', default='assets/img/avatar.png')
    id_card           = models.FileField(upload_to='documents/%Y/%m/%d', default='')
    # user              = models.ForeignKey(UserRegistration, on_delete= models.CASCADE, blank=True, null=True)
    created_on        = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'created_on'

    def __str__(self):
        return self.created_on


class UserRegistrationManager(BaseUserManager):
    def create_user(self, email, firstname,lastname,role, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname,
            role=role,
            
            )
        

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname, lastname, role, password=None):
        user = self.create_user(email, firstname=firstname, lastname=lastname, role=role,  password=password)
        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

AUTH_USER_MODEL = User



class UserRegistration(AbstractBaseUser):
    email             = models.EmailField(verbose_name='email address',max_length=255,unique=True,default='')
    firstname         = models.CharField(max_length=200,default='')
    lastname          = models.CharField(max_length=200,default='')
    role              = models.CharField(max_length=200,default='')
    phone_number      = models.IntegerField(default=0)
    whatsapp_phone_number = models.IntegerField(default=0)
    profile           = models.ForeignKey(UpdateProfile, on_delete= models.CASCADE, blank=True, null=True)
    created_on        = models.DateTimeField(auto_now_add=True)
    is_active         = models.BooleanField(default=True)
    is_admin          = models.BooleanField(default=False)
    
    objects = UserRegistrationManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'role' ]

    def __str__(self): 
        return '{} {}'.format(self.firstname, self.lastname)

    def fullname(self):
        return '{} {}'.format(self.firstname, self.lastname)

    # def __str__(self):
    #     return self.email

    def has_perm(self, perm, obj=None): 
        return True

    def has_module_perms(self, app_label): 
        return True

    @property
    def is_staff(self):
        return self.is_admin





today = date.today()

class Review(models.Model):
    messages       = models.TextField(max_length=50, verbose_name='messages')
    property_title = models.CharField(max_length=20, verbose_name='property_title')
    name           = models.CharField(max_length=20, verbose_name='name')
    email          = models.EmailField(verbose_name='email address',max_length=255,unique=True,default='')

    def __str__(self):
        return self.name





class Plan(models.Model):
    plan_choices =(
        ('Gold', 'Gold'),
        ('Premium', 'Premium'),
        ('Standard', 'Standard'),
        ('Free', 'Free'),
    )
    plan_duration =(
        ('Days', 'Days'),
        ('Weeks', 'Weeks'),
        ('Months', 'Months'),
    )
    slug               = models.SlugField(null=True, blank=True)
    plan_type          = models.CharField(choices=plan_choices, default='Free', max_length=30)
    duration           = models.PositiveIntegerField(default=7)
    duration_period    = models.CharField(choices=plan_duration, default='Days', max_length=100)
    images             = models.CharField(max_length=20, verbose_name='images')
    amount             = models.FloatField(default=0)
    listings           = models.IntegerField(default=0)

    def __str__(self):
        return self.plan_type


class UserPlan(models.Model):
    user           = models.OneToOneField(UserRegistration,related_name='user_plan',on_delete=models.SET_NULL, null=True)
    plan           = models.ForeignKey(Plan, related_name='user_plan', on_delete=models.SET_NULL, null=True)
    reference_code = models.CharField(max_length=100, default='',blank=True )
    def __str__(self):
        return self.user.email

@receiver(post_save, sender=UserPlan)
def create_subscription(sender, instance, *args, **kwargs):
    if instance:
        Subscription.objects.create(user_plan=instance, expires_in=datetime.now().date() + timedelta(days=instance.plan.duration))


class Subscription(models.Model):
    user_plan          = models.ForeignKey(UserPlan, on_delete=models.SET_NULL, null=True)
    expires_in         = models.DateField(null=True, blank=True)
    active             = models.BooleanField(default=True)

    def __str__(self):
        return self.user_plan.user.email

@receiver(post_save, sender=Subscription)
def update_active(sender, instance, *args, **kwargs):
    if instance.expires_in < today:
        subscription = Subscription.objects.get(id=instance.id)
        subscription.delete()

class PayHistory(models.Model):
    user                 = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, default=None)
    paystack_charge_id   = models.CharField(max_length=100, default='',blank=True )
    paystack_access_code = models.CharField(max_length=100, default='',blank=True )
    payment_for          = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    amount               = models.FloatField(default=0)
    paid                 = models.BooleanField(default=False)
    date                 = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email