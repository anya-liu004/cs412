from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter
import plotly
import plotly.graph_objs as go
from datetime import datetime

# # Create your views here.
class VotersListView(ListView):
    '''View to display voter analytics'''

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        '''Filters the queryset based on the request parameters.'''
        # Start with the full queryset
        voters = super().get_queryset().order_by('date_of_birth')

        # Get query parameters from the request
        party_affiliation = self.request.GET.get('party_affiliation', '')
        min_dob = self.request.GET.get('min_dob', '')
        max_dob = self.request.GET.get('max_dob', '')
        voter_score = self.request.GET.get('voter_score', '')
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']

        if party_affiliation:
            voters = voters.filter(party_affiliation=party_affiliation)

        if min_dob:
            voters = voters.filter(date_of_birth__gte=f"{min_dob}-01-01")

        if max_dob:
            voters = voters.filter(date_of_birth__lte=f"{max_dob}-12-31")

        if voter_score:
            voters = voters.filter(voter_score=voter_score)

        # Check which election checkboxes are checked
        for election in elections:
            if self.request.GET.get(election):
                voters = voters.filter(**{election: True})

        return voters

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)
        
        # Generate a list of years from 1900 to 2023
        context['years'] = list(range(1900, 2024))  # 2024 is exclusive
        party_affiliations = sorted(Voter.objects.values_list('party_affiliation', flat=True).distinct())
        context['party_affiliations'] = party_affiliations

        return context

class VoterDetailView(DetailView):
    '''View to show detail page for one voter.'''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'v' # short for voter