from django.contrib import admin
from accounts.models import UserRegistration, Subscription, Plan, UserPlan, UpdateProfile
from properties.models import Property, FeaturedProperty

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'firstname', 'lastname','created_on',)
    list_filter = ("email",)
    search_fields = ['email', 'created_on']
    

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user_plan', 'expires_in', 'active',)
    list_filter = ("user_plan",)
    search_fields = ['user_plan', 'expires_in']

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'types','created_on',)
    list_filter = ("title",)
    search_fields = ['title', 'created_on']
    prepopulated_fields = {'slug': ('title',)}

class FeaturedPropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'types','created_on',)
    list_filter = ("title",)
    search_fields = ['title', 'created_on']
    prepopulated_fields = {'slug': ('title',)}

class PlanAdmin(admin.ModelAdmin):
    list_display = ('plan_type', 'duration', 'duration_period',)
    list_filter = ("plan_type",)
    search_fields = ['plan_type', 'duration']
    prepopulated_fields = {'slug': ('plan_type',)}
    
admin.site.register(UserRegistration,UserAdmin)
admin.site.register(UpdateProfile)
admin.site.register(Subscription,SubscriptionAdmin)
admin.site.register(Plan)
admin.site.register(UserPlan)
admin.site.register(Property,PropertyAdmin)
admin.site.register(FeaturedProperty,FeaturedPropertyAdmin)
