from django.db import models
import datetime
# Create your models here.


class PostResults(models.Model):
    title = models.CharField(max_length=150)
    last_read_date = models.DateTimeField(default=datetime.datetime.now())
    teams = models.JSONField(default=None)
    home_league_avarage_offence = models.FloatField(default=None)
    home_league_avarage_defence = models.FloatField(default=None)
    away_league_avarage_offence = models.FloatField(default=None)
    away_league_avarage_defence = models.FloatField(default=None)
    home_teams_avarage = models.JSONField(default=None)
    away_teams_avarage_defence = models.JSONField(default=None)
    attack_strength = models.JSONField(default=None)
    defence_strength = models.JSONField(default=None)
    games_results = models.JSONField(default=None)


class TeamsStatsAverage(models.Model):
    pass