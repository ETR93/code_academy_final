from rest_framework import serializers
from .models import PostResults
from rest_framework import generics


class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostResults
        fields = ['title', 'last_read_date', 'teams', 'home_league_avarage_offence', 'home_league_avarage_defence',
                  'home_league_avarage_defence', 'away_league_avarage_offence', 'away_league_avarage_defence',
                  'home_teams_avarage', 'away_teams_avarage_defence', 'defence_strength', 'games_results']


class GetResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostResults
        fields = ['games_results', 'last_read_date']