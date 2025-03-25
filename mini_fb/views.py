# Author: Anya Liu
# Email: anyaliu@bu.edu
# This is the views.py file for the mini facebook app and defines the views for the mini_fb app.

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login # NEW

### Profile
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

### CREATE VIEWS
# Create Profile
class CreateProfileView(CreateView):
    '''A view to handle creation of a new Profile.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Profile object (POST)
    '''
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)
        # add UserCreationForm to context
        context['user_creation_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''
        user_form = UserCreationForm(self.request.POST)
        
        if user_form.is_valid():
            user = user_form.save()  # Save the new user
            login(self.request, user)  # Log in the newly created user
            form.instance.user = user  # Attach user to profile instance
            return super().form_valid(form)  # Save profile and redirect
        else:
            print("UserCreationForm errors:", user_form.errors)
            # If UserCreationForm is invalid, re-render the template with errors
            return self.render_to_response(self.get_context_data(form=form, user_creation_form=user_form))

# Create Status Message
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''A view to create a new status message and save it to the database.'''
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
        # calling the superclass method
        context = super().get_context_data()
        # find/add the profile to the context data
        profile = Profile.objects.get(user=self.request.user)
        # pk = self.kwargs['pk'] # retrieve the PK from the URL pattern
        # profile = Profile.objects.get(pk=pk)

        # add this profile into the context dictionary:
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Status Message
        object before saving it to the database.
        '''
        # pk = self.kwargs['pk'] # retrieve the PK from the URL pattern
        # profile = Profile.objects.get(pk=pk)
        profile = Profile.objects.get(user=self.request.user)
        form.instance.profile = profile # attach this profile to the status message
        sm = form.save() # save the status message to database

        # Process uploaded files
        files = self.request.FILES.getlist('files') # read the file from the form
        for file in files:
            # Create and save the Image object
            image = Image(profile=profile, image_file=file)
            image.save()

            # Link Image to StatusMessage
            status_image = StatusImage(status_message=sm, image=image)
            status_image.save()

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)

    ## show how the reverse function uses the urls.py to find the URL pattern
    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Status Message.'''
        # retrieve the PK from the URL pattern
        # pk = self.kwargs['pk']
        # call reverse to generate the URL for this Article
        # return reverse('show_profile', kwargs={'pk':pk})
        profile = Profile.objects.filter(user=self.request.user).first()
        return reverse('show_profile', kwargs={'pk': profile.pk})

### UPDATE VIEWS
# Update Profile 
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''A view to update an Article and save it to the database.'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_object(self):
        '''Retrieve the Profile object associated with the logged-in user.'''
        return Profile.objects.get(user=self.request.user)

    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''
        print(f'UpdateProfileView: form.cleaned_data={form.cleaned_data}')

        return super().form_valid(form)

# Update Status Message 
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''A view to update a Status message and save it to the database.'''
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"
    context_object_name = 'status_message'
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new StatusMessage object.
        '''
        print(f'UpdateStatusMessageView: form.cleaned_data={form.cleaned_data}')

        return super().form_valid(form)
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the update.'''

        # get the pk for this status message
        pk = self.kwargs.get('pk')
        status_message = StatusMessage.objects.get(pk=pk)
        
        # find the profile to which this StatusMessage is related by FK
        profile = status_message.profile
        
        # reverse to show the profile page
        return reverse('show_profile', kwargs={'pk':profile.pk})

### DELETE VIEWS
# Delete Status Message
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''A view to delete a status message and remove it from the database.'''
    template_name = "mini_fb/delete_status_form.html"
    model = StatusMessage
    context_object_name = 'status_message'

    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
        pk = self.kwargs.get('pk') # get the pk for this status message
        status_message = StatusMessage.objects.get(pk=pk)
        
        # find the profile to which this StatusMessage is related by FK
        profile = status_message.profile
        
        # reverse to show the profile page
        return reverse('show_profile', kwargs={'pk':profile.pk})

### Friends
class AddFriendView(LoginRequiredMixin, View):
    '''A view to add a friend relationship between two Profiles.'''
    
    def dispatch(self, request, *args, **kwargs):
        # Get the Profile instances
        # pk = self.kwargs.get('pk')
        other_pk = self.kwargs.get('other_pk')
        # profile = Profile.objects.get(pk=pk)
        other_profile = Profile.objects.get(pk=other_pk)
        profile = Profile.objects.get(user=request.user)

        # Call add_friend method
        profile.add_friend(other_profile)

        # Redirect back to the profile page
        return redirect('show_profile', pk=profile.pk)
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    '''Show the friend suggestions for one profile.'''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

### News Feed
class ShowNewsFeedView(LoginRequiredMixin, DetailView): 
    '''Show the news feed for one profile.'''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)