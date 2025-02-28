# Anya Liu ; anyaliu@bu.edu
# This is the model for the mini_fb app.
# It defines the data structure for the mini Facebook application.

from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the idea of Profile which has attributes of individual Facebook users.'''

    # data attributes of a Profile:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    image_url = models.URLField(blank=True) ## new
    
    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name} {self.last_name}'
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_status_messages(self):
        '''Return all of the status messages about this profile.'''

        messages = StatusMessage.objects.filter(profile=self)
        return messages
    
class StatusMessage(models.Model):
    '''Encapsulate the idea of a Status Message on a Profile.'''
	
	# data attributes of a Status Message:
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE) # foreign key because it refers to a different kind of model
    # author = models.TextField(blank=False)
    message = models.TextField(blank=False) # the text of the status message
    timestamp = models.DateTimeField(auto_now=True) # the time at which this status message was created/saved
    
    def __str__(self):
        '''Return a string representation of this StatusMessage object.'''
        return f'{self.message}'


