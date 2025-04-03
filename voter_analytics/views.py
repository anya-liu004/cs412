# Author: Anya Liu
# Email: anyaliu@bu.edu
# This file contains the views for the Voter Analytics project.
# It defines the views for displaying voter data and graphs.

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter
import plotly
import plotly.graph_objs as go
from collections import Counter

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
        # Generate a list of party affiliations
        context['party_affiliations'] = sorted(Voter.objects.values_list('party_affiliation', flat=True).distinct())

        # Preserve GET parameters for pagination (excluding 'page')
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['query_string'] = query_params.urlencode()

        return context

class VoterDetailView(DetailView):
    '''View to show detail page for one voter.'''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'v' # short for voter

class VoterGraphView(ListView):
    '''View to show graph of voter analytics.'''
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

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

    def get_context_data(self, **kwargs) :
        '''
        Provide context variables for use in template
        '''
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        context['years'] = list(range(1900, 2024))
        context['party_affiliations'] = sorted(Voter.objects.values_list('party_affiliation', flat=True).distinct())

        context['graph_div_birth'] = self.get_birth_year_histogram(voters)
        context['graph_div_party'] = self.get_party_affiliation_pie_chart(voters)
        context['graph_div_elections'] = self.get_election_participation_histogram(voters)

        return context
    
    def get_birth_year_histogram(self, voters):
        '''Creates a histogram of voters by year of birth'''
        birth_years = [v.date_of_birth.year for v in voters]
        year_counts = Counter(birth_years)

        # Define bins for grouping (decades)
        min_year = 1910
        max_year = max(birth_years, default=2023)
        bins = list(range(min_year, max_year + 10, 10))

        # Count voters in each decade bin
        binned_counts = [sum(year_counts[year] for year in range(start, start + 10)) for start in bins]

        # Create a bar chart
        fig = go.Bar(x=[f"{start}s" for start in bins], y=binned_counts)
        title_text = "Voter Distribution by Year of Birth (Grouped by Decades)"

        return plotly.offline.plot(
            {"data": [fig], "layout": {"title": title_text, "xaxis": {"title": "Decade"}, "yaxis": {"title": "Number of Voters"}}},
            auto_open=False,
            output_type="div",
        )
    
    def get_party_affiliation_pie_chart(self, voters):
        '''Creates a pie chart of voters by party affiliation'''
        from collections import Counter

        party_counts = Counter(v.party_affiliation for v in voters)
        labels = list(party_counts.keys())
        values = list(party_counts.values())

        # Create a pie chart
        fig = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values, 
            textinfo='percent',
            insidetextorientation='radial',  
        )])

        fig.update_layout(
            title="Voter Distribution by Party Affiliation",
            legend=dict(orientation="h", x=1, y=1)  
        )

        return plotly.offline.plot(
            fig, auto_open=False, output_type="div"
        )
    
    def get_election_participation_histogram(self, voters):
        '''Creates a bar chart of voter participation in each election'''
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        
        # Count voters who participated in each election
        participation_counts = [voters.filter(**{election: True}).count() for election in elections]

        fig = go.Bar(x=elections, y=participation_counts)

        title_text = "Vote Count by Election"

        return plotly.offline.plot(
            {"data": [fig], "layout": {"title": title_text, "xaxis": {"title": "Election"}, "yaxis": {"title": "Number of Voters"}}},
            auto_open=False,
            output_type="div",
        )