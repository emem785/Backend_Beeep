from django.contrib import admin
from .models import *

class CivilianAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'twitter_handle', 'user', 'is_verified')

class LawyerAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'twitter_handle', 'user', 'is_verified')

class BuddyAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'phonenumber')

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('plan',)

class PlanAdmin(admin.ModelAdmin):
    list_display = ('name',)

class TokenAdmin(admin.ModelAdmin):
    list_display = ('token','user', 'is_active', 'device_id')

class BeeepAdmin(admin.ModelAdmin):
    list_display = ('start_lng',)

admin.site.register(Civilian, CivilianAdmin)
admin.site.register(Lawyer, LawyerAdmin)
admin.site.register(Buddy, BuddyAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(Beeep, BeeepAdmin)
