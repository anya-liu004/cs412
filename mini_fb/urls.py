# Anya Liu ; anyaliu@bu.edu
# This is the urls.py file for the mini_fb app.
# It maps URLs to the views in the mini_fb app.

from django.urls import path
from .views import * # our view class definition 

urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'), 
    path('show_all_profiles', ShowAllProfilesView.as_view(), name='show_all_profiles'), 
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'), # show one profile
    path('profile/create_profile', CreateProfileView.as_view(), name='create_profile'), 
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name='create_status'), 
]