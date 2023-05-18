from django.shortcuts import render
from rest_framework import generics, permissions
from .models import PostResults
from .serializers import ResultsSerializer
from .helpers import get_league_data, calculate_koef, get_scheduled_games, calculate_potencial_result
import datetime
from .testing_data import *


class Results(generics.ListCreateAPIView):
    res_league = get_league_data()
    scheduled_games = get_scheduled_games(res_league)
    res = calculate_koef(scheduled_games,
                         res_league)
    final_data = calculate_potencial_result(scheduled_games, res)
    queryset = PostResults.objects.all()
    serializer_class = ResultsSerializer

    def perform_create(self, serializer):
        serializer.save(
                            title='Data'+str(datetime.datetime.now()),
                            last_read_date=datetime.datetime.now(),
                            teams=self.final_data['teams'],
                            home_league_avarage_offence=self.final_data['home_league_avarage_offence'],
                            home_league_avarage_defence=self.final_data['home_league_avarage_defence'],
                            away_league_avarage_offence=self.final_data['away_league_avarage_offence'],
                            away_league_avarage_defence=self.final_data['away_league_avarage_defence'],
                            home_teams_avarage=self.final_data['home_teams_avarage'],
                            away_teams_avarage_defence=self.final_data['away_teams_avarage_defence'],
                            attack_strength=self.final_data['attack_strength'],
                            defence_strength=self.final_data['defence_strength'],
                            games_results=self.final_data['potencial_results']
                        )