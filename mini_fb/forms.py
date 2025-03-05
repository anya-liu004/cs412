# Author: Anya Liu
# Email: anyaliu@bu.edu
# This is the forms.py file for the mini facebook app and defines the forms for the mini_fb app.

from django import forms
from .models import Profile, StatusMessage

# define the forms that we use to create/update/delete operations
class CreateProfileForm(forms.ModelForm):
    '''A form to add an Article to the database.'''
    class Meta:
        '''associate this form with a model from our database.'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'image_url']

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a StatusMessage to the database.'''
    class Meta:
        '''associate this form with the StatusMessage model; select fields.'''
        model = StatusMessage
        fields = ['message' ]  # which fields from model should we use

class UpdateProfileForm(forms.ModelForm):
    '''A form to update a Profile in the database.'''

    class Meta:
        '''associate this form with the Article model.'''
        model = Profile
        fields = ['city', 'email_address', 'image_url']  # which fields from model should update