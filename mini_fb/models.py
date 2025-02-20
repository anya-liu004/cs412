# Anya Liu ; anyaliu@bu.edu
# This is the model for the mini_fb app.
# It defines the data structure for the mini Facebook application.

from django.db import models

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

