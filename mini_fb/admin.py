# Anya Liu ; anyaliu@bu.edu
# This is the admin.py file for the mini_fb app.
# It registers the Profile model with the admin site.

from django.contrib import admin

# Register your models here.
from .models import Profile, StatusMessage

admin.site.register(Profile)
admin.site.register(StatusMessage)