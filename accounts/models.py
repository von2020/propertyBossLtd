from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# from properties.models import Property
from django.utils import timezone
# Create your models here.


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
    profile_pic       = models.ImageField(null=True, blank=True)
    created_on        = models.DateTimeField(default=timezone.now)
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

class Review(models.Model):
    messages       = models.TextField(max_length=50, verbose_name='messages')
    property_title = models.CharField(max_length=20, verbose_name='property_title')
    name           = models.CharField(max_length=20, verbose_name='name')
    email          = models.EmailField(verbose_name='email address',max_length=255,unique=True,default='')

    def __str__(self):
        return self.name

# class Standard(models.Model):
#     name               = models.CharField(max_length=20, verbose_name='name_standard', default='')
#     featured           = models.IntegerField(default=0)
#     duration           = models.CharField(max_length=20, verbose_name='duration')
#     images             = models.CharField(max_length=20, verbose_name='images')
#     amount             = models.FloatField(default=0)
#     listings           = models.IntegerField(default=0)

#     def __str__(self):
#         return self.name

# class Premium(models.Model):
#     name               = models.CharField(max_length=20, verbose_name='name_premium', default='')
#     featured           = models.IntegerField(default=0)
#     duration           = models.CharField(max_length=20, verbose_name='duration')
#     images             = models.CharField(max_length=20, verbose_name='images')
#     amount             = models.FloatField(default=0)
#     listings           = models.IntegerField(default=0)

#     def __str__(self):
#         return self.name

class Plan(models.Model):
    name               = models.CharField(max_length=20, verbose_name='name', default='')
    featured           = models.IntegerField(default=0)
    duration           = models.CharField(max_length=20, verbose_name='duration')
    images             = models.CharField(max_length=20, verbose_name='images')
    amount             = models.FloatField(default=0)
    listings           = models.IntegerField(default=0)

    def __str__(self):
        return self.name



class Subscription(models.Model):
    customer           = models.ForeignKey(UserRegistration, on_delete= models.CASCADE, related_name='customer', blank=True, null=True)
    payment_date       = models.DateTimeField(default=timezone.now)
    duration           = models.CharField(max_length=20, verbose_name='duration')
    plan               = models.ForeignKey(Plan, on_delete= models.CASCADE, related_name='plan', blank=True, null=True)
    amount             = models.FloatField(default=0)
    listings           = models.IntegerField(default=0)
    is_standard        = models.BooleanField(default=False)
    is_premium         = models.BooleanField(default=False)
    is_gold            = models.BooleanField(default=False)

    def __str__(self):
        return self.duration

