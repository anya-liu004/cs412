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
    # create
    path('profile/create_profile', CreateProfileView.as_view(), name='create_profile'), 
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name='create_status'), 
    # update
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"), 
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name="update_status"),
    # delete
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name="delete_status"),
    # friend
    path('profile/<int:pk>/add_friend/<int:other_pk>', AddFriendView.as_view(), name="add_friend"),
    path('profile/<int:pk>/friend_suggestions', ShowFriendSuggestionsView.as_view(), name="friend_suggestions"),
    # newsfeed
    path('profile/<int:pk>/news_feed', ShowNewsFeedView.as_view(), name="news_feed"),
]