from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone
from accounts.models import UserRegistration
from django.db.models.signals import pre_save
from properties.utils import unique_slug_generator

# Create your models here.
class Property(models.Model):
    title          = models.CharField(max_length=20, verbose_name='title')
    status         = models.CharField(max_length=20, verbose_name='status')
    types          = models.CharField(max_length=20, verbose_name='types')
    price          = models.IntegerField(default=0)
    slug           = models.SlugField(max_length=200, null=True, blank=True)
    area           = models.CharField(max_length=20, verbose_name='area')
    bedrooms       = models.CharField(max_length=20, verbose_name='bedrooms')
    bathrooms      = models.CharField(max_length=20, verbose_name='bathrooms')
    image_one      = CloudinaryField(null=True, blank=True)
    image_two      = CloudinaryField(null=True, blank=True)
    image_three    = CloudinaryField(null=True, blank=True)
    image_four     = CloudinaryField(null=True, blank=True)
    image_five     = CloudinaryField(null=True, blank=True)
    location       = models.CharField(max_length=200, verbose_name='location')
    description    = models.TextField(max_length=2000, verbose_name='description')
    created_on     = models.DateTimeField(default=timezone.now)
    customer       = models.ForeignKey(UserRegistration, on_delete= models.CASCADE, blank=True, null=True)


    class Meta:
        ordering = ['-created_on']




    # def pre_save_slugify_receiver(sender, instance, *args, **kwargs):
    #     slug = slugify(instance.title)
    #     instance.slug = slug

    #     pre_save.connect(pre_save_slugify_receiver, sender=Post)

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

def slug_generator(sender, instance, *args, **kwargs):
        if not instance.slug:
            # instance.slug = 'SLUG'
            instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Property)


class FeaturedProperty(models.Model):
    title          = models.CharField(max_length=100, verbose_name='featured_title')
    status         = models.CharField(max_length=100, verbose_name='featured_status')
    types          = models.CharField(max_length=100, verbose_name='featured_types')
    price          = models.IntegerField(default=0)
    slug           = models.SlugField(max_length=200, default='property')
    area           = models.CharField(max_length=100, verbose_name='featured_area')
    bedrooms       = models.CharField(max_length=20, verbose_name='featured_bedrooms')
    bathrooms      = models.CharField(max_length=20, verbose_name='featured_bathrooms')
    image_one      = CloudinaryField(blank='true', null='true')
    image_two      = CloudinaryField(blank='true', null='true')
    image_three    = CloudinaryField(blank='true', null='true')
    image_four     = CloudinaryField(blank='true', null='true')
    image_five     = CloudinaryField(blank='true', null='true')
    location       = models.CharField(max_length=100, verbose_name='featured_location')
    description    = models.TextField(max_length=100, verbose_name='featured_description')
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


