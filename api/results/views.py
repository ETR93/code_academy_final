from django.shortcuts import render
from rest_framework import generics, permissions
from .models import PostResults
from .serializers import ResultsSerializer
from .helpers import get_league_data, calculate_koef, get_scheduled_games, calculate_potencial_result
from .testing_data import *


class Results(generics.ListAPIView):
    # res_league = get_league_data()
    # scheduled_games = get_scheduled_games(res_league)
    # res = calculate_koef(scheduled_games,
    #                      res_league)
    # calculate_potencial_result(scheduled_games, res)
    # print(calculate_potencial_result(scheduled_games, res))
    queryset = PostResults.objects.all()
    serializer_class = ResultsSerializer
