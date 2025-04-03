# Anya Liu ; anyaliu@bu.edu
# This is the urls.py file for the voter_analytics app.
# This file maps URLs to the views in the voter_analytics app.
from django.urls import path
from . import views 

urlpatterns = [
    # map the URL (empty string) to the view
	path(r'', views.VotersListView.as_view(), name='home'),
    path(r'voters', views.VotersListView.as_view(), name='voters_list'),
    path(r'voter/<int:pk>', views.VoterDetailView.as_view(), name='voter_detail'),
    path(r'graphs', views.VoterGraphView.as_view(), name='graphs'),
]