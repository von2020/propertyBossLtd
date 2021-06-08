from django.contrib import admin
from accounts.models import UserRegistration, Subscription, Plan
from properties.models import Property, FeaturedProperty

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'firstname', 'lastname','created_on',)
    list_filter = ("email",)
    search_fields = ['email', 'created_on']

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'payment_date', 'duration','amount','listings',)
    list_filter = ("customer",)
    search_fields = ['customer', 'duration']

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'types','created_on',)
    list_filter = ("title",)
    search_fields = ['title', 'created_on']

class FeaturedPropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'types','created_on',)
    list_filter = ("title",)
    search_fields = ['title', 'created_on']
    
admin.site.register(UserRegistration,UserAdmin)
admin.site.register(Subscription,SubscriptionAdmin)
admin.site.register(Plan)
admin.site.register(Property,PropertyAdmin)
admin.site.register(FeaturedProperty,FeaturedPropertyAdmin)
