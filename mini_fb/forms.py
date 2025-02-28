from django import forms
from .models import Profile, StatusMessage

# define the forms that we use to create/update/delete operations
class CreateProfileForm(forms.ModelForm):
    '''A form to add an Article to the database.'''
    class Meta:
        '''associate this form with a model from our database.'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'image_url']

# class CreateArticleForm(forms.ModelForm):
#     '''A form to add an Article to the database.'''

#     class Meta:
#         '''associate this form with a model from our database.'''
#         model = Article
#         fields = ['author', 'title', 'text', 'image_url']

# class CreateCommentForm(forms.ModelForm):
#     '''A form to add a Comment to the database.'''

#     class Meta:
#         '''associate this form with the Comment model; select fields.'''
#         model = Comment
#         # fields = ['article', 'author', 'text', ]  # which fields from model should we use
#         fields = ['author', 'text', ]  # which fields from model should we use
