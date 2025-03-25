# Anya Liu ; anyaliu@bu.edu
# This is the urls.py file for the mini_fb app.
# It maps URLs to the views in the mini_fb app.

from django.urls import path
from .views import * # our view class definition 
from django.contrib.auth import views as auth_views

urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'), 
    path('show_all_profiles', ShowAllProfilesView.as_view(), name='show_all_profiles'), 
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'), # show one profile
    # create
    path('profile/create_profile', CreateProfileView.as_view(), name='create_profile'), 
    path('profile/create_status', CreateStatusMessageView.as_view(), name='create_status'), 
    # update
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"), 
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name="update_status"),
    # delete
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name="delete_status"),
    # friend
    path('profile/add_friend/<int:other_pk>', AddFriendView.as_view(), name="add_friend"),
    path('profile/friend_suggestions', ShowFriendSuggestionsView.as_view(), name="friend_suggestions"),
    # newsfeed
    path('profile/news_feed', ShowNewsFeedView.as_view(), name="news_feed"),
    # authentication views
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'), ## NEW
	path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'), ## NEW
    # path('register/', RegistrationView.as_view(), name='register'),
]