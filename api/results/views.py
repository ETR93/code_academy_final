from django.shortcuts import render
from rest_framework import generics, permissions
from .models import PostResults
from .serializers import ResultsSerializer, GetResultsSerializer
from .helpers import get_league_data, calculate_koef, get_scheduled_games, calculate_potencial_result, \
    parse_game_attack_defence_strength
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
import os
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


class GetResults(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'templates/get_results.html'
    data = {}
    teams = []
    home_teams_avarage = []
    away_teams_avarage_defence = []
    leagues_average_stats = {}

    def get(self, request):
        queryset = PostResults.objects.all()[:1]
        for row in queryset:
            print(row.attack_strength, row.defence_strength)
            for game in row.games_results:
                self.data[game] = {}
                self.data[game] = {
                    'game': game,
                    'scores': row.games_results[game],
                    'attack_strength': parse_game_attack_defence_strength(row.attack_strength, game),
                    'defence_strength': parse_game_attack_defence_strength(row.defence_strength, game),
                    'last_read_date': row.last_read_date,
                }
            self.teams = row.teams
            self.teams.insert(0, 'Column')
            self.home_teams_avarage = row.home_teams_avarage
            self.home_teams_avarage.insert(0, 'Home teams average offence')
            self.away_teams_avarage_defence = row.away_teams_avarage_defence
            self.away_teams_avarage_defence.insert(0, 'Away teams average defence')
            self.leagues_average_stats = {
                'home_league_avarage_offence': row.home_league_avarage_offence,
                'home_league_avarage_defence': row.home_league_avarage_defence,
                'away_league_avarage_offence': row.away_league_avarage_offence,
                'away_league_avarage_defence': row.away_league_avarage_defence
            }
        serializer_class = GetResultsSerializer
        return Response(
            {
                'serializer': serializer_class,
                'data': self.data,
                'teams': self.teams,
                'home_league_avarage': self.home_teams_avarage,
                'away_teams_average_defence': self.away_teams_avarage_defence,
                'leagues_average_stats': self.leagues_average_stats
            }
        )

