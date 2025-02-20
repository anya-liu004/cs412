# Anya Liu ; anyaliu@bu.edu
# This is the urls.py file for the mini_fb app.
# It maps URLs to the views in the mini_fb app.

from django.urls import path
from .views import ShowAllProfilesView, ArticleView, RandomArticleView # our view class definition 

urlpatterns = [
    # map the URL (empty string) to the view
    # path('', RandomArticleView.as_view(), name='random'), 
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'), 
    path('show_all_profiles', ShowAllProfilesView.as_view(), name='show_all_profiles'), 
    # path('article/<int:pk>', ArticleView.as_view(), name='article'), # show one article ### NEW

]