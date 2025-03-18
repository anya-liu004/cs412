# Anya Liu ; anyaliu@bu.edu
# This is the admin.py file for the mini_fb app.
# It registers the Profile model with the admin site.

from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(StatusImage)
admin.site.register(Friend)