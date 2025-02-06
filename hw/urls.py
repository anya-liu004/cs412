# file: hw/urls.py
from django.urls import path
from django.conf import settings
from . import views

# URL Configuration specific to the hw app 
urlpatterns = [ 
    # path(r'', views.home, name="home"), 
    path(r'', views.home, name="home"),
    path(r'about', views.about, name="about"),
] 

