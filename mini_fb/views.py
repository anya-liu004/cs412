# Author: Anya Liu
# Email: anyaliu@bu.edu
# This is the views.py file for the mini facebook app and defines the views for the mini_fb app.

from django.shortcuts import render
from .models import Profile
from django.views.generic import ListView, DetailView
import random

# Views for the mini_fb app
class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all Facebook Profiles.'''

    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file

class ShowProfilePageView(DetailView):
    '''Show the details for one profile.'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class RandomArticleView(DetailView):
    '''Show the details for one article.'''
    model = Profile
    template_name = 'blog/article.html'
    context_object_name = 'article'

    # pick one article at random:
    def get_object(self):
        '''Return one Article object chosen at random.'''

        all_articles = Article.objects.all()
        return random.choice(all_articles)
