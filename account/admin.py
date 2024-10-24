from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import CustomUser, UserProfile


# Register your models here.
class ProfileDisplay(ModelAdmin):
    list_display = ["uid", "user"]


admin.site.register(CustomUser)
admin.site.register(UserProfile, ProfileDisplay)
