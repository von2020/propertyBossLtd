from django.db import models
from django.utils import timezone
from accounts.models import UserRegistration

# Create your models here.
class Property(models.Model):
    title          = models.CharField(max_length=20, verbose_name='title')
    status         = models.CharField(max_length=20, verbose_name='status')
    types          = models.CharField(max_length=20, verbose_name='types')
    price          = models.IntegerField(default=0)
    slug           = models.SlugField(max_length=200)
    area           = models.CharField(max_length=20, verbose_name='area')
    bedrooms       = models.CharField(max_length=20, verbose_name='bedrooms')
    bathrooms      = models.CharField(max_length=20, verbose_name='bathrooms')
    image_one      = models.ImageField(upload_to='property/', default='')
    image_two      = models.ImageField(upload_to='property/', default='', null=True, blank=True)
    image_three    = models.ImageField(upload_to='property/', default='', null=True, blank=True)
    image_four     = models.ImageField(upload_to='property/', default='', null=True, blank=True)
    image_five     = models.ImageField(upload_to='property/', default='', null=True, blank=True)
    location       = models.CharField(max_length=200, verbose_name='location')
    description    = models.TextField(max_length=2000, verbose_name='description')
    created_on     = models.DateTimeField(default=timezone.now)
    customer       = models.ForeignKey(UserRegistration, on_delete= models.CASCADE, blank=True, null=True)


    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    @property
    def imageURL_one(self):
        try:
            url = self.image_one.url
        except:
            url = ''
        return url

    def imageURL_two(self):
        try:
            url = self.image_two.url
        except:
            url = ''
        return url

    def imageURL_three(self):
        try:
            url = self.image_three.url
        except:
            url = ''
        return url

    def imageURL_four(self):
        try:
            url = self.image_four.url
        except:
            url = ''
        return url

    def imageURL_five(self):
        try:
            url = self.image_five.url
        except:
            url = ''
        return url


class FeaturedProperty(models.Model):
    title          = models.CharField(max_length=20, verbose_name='featured_title')
    status         = models.CharField(max_length=20, verbose_name='featured_status')
    types          = models.CharField(max_length=20, verbose_name='featured_types')
    price          = models.IntegerField(default=0)
    slug           = models.SlugField(max_length=200, default='property')
    area           = models.CharField(max_length=20, verbose_name='featured_area')
    bedrooms       = models.CharField(max_length=20, verbose_name='featured_bedrooms')
    bathrooms      = models.CharField(max_length=20, verbose_name='featured_bathrooms')
    image_one      = models.ImageField(upload_to='property/', default='')
    image_two      = models.ImageField(upload_to='property/', default='')
    image_three    = models.ImageField(upload_to='property/', default='')
    image_four     = models.ImageField(upload_to='property/', default='')
    image_five     = models.ImageField(upload_to='property/', default='')
    location       = models.CharField(max_length=20, verbose_name='featured_location')
    description    = models.TextField(max_length=50, verbose_name='featured_description')
    created_on     = models.DateTimeField(default=timezone.now)
    customer       = models.ForeignKey(UserRegistration, on_delete= models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    

    @property
    def imageURL_one(self):
        try:
            url = self.image_one.url
        except:
            url = ''
        return url

    def imageURL_two(self):
        try:
            url = self.image_two.url
        except:
            url = ''
        return url

    def imageURL_three(self):
        try:
            url = self.image_three.url
        except:
            url = ''
        return url

    def imageURL_four(self):
        try:
            url = self.image_four.url
        except:
            url = ''
        return url

    def imageURL_five(self):
        try:
            url = self.image_five.url
        except:
            url = ''
        return url


