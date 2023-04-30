import time

import requests
from bs4 import BeautifulSoup as bs
from lxml import html
import numpy as np

AWAY_URL = "https://statsdream.com/xml/table/?id=35206&lang_id=2&type=away&conf="
HOME_URL = "https://statsdream.com/xml/table/?id=35206&lang_id=2&type=home&conf="
TEAMS_NAMES_XPATH = "//table[@class='table']//tbody//tr//td//a//text()"
LEAGUE_AVERAGE = "//table[@class='table']//tbody//tr//td[not(@class)]//text()"
SCHEDULE_URL = "https://www.euroleaguebasketball.net/euroleague/game-center/"
SCHEDULED_GAMES_XPATH = "//span[contains(@class, 'visually-hidden_wrap__1CCX0') and contains(text(),'game')]//text()"


def get_league_data():
    results = {}
    get_data_home = requests.get(HOME_URL)
    get_data_away = requests.get(AWAY_URL)
    tree_home = html.fromstring(get_data_home.content)
    tree_away = html.fromstring(get_data_away.content)
    teams = tree_home.xpath(TEAMS_NAMES_XPATH)
    home_avarage = tree_home.xpath(LEAGUE_AVERAGE)
    away_avarage = tree_away.xpath(LEAGUE_AVERAGE)
    results['teams'] = teams
    results['home_league_avarage_offence'] = round(np.mean([float(val) for val in home_avarage[5::9]]), 2)
    results['home_league_avarage_defence'] = round(np.mean([float(val) for val in home_avarage[6::9]]), 2)
    results['away_league_avarage_offence'] = round(np.mean([float(val) for val in away_avarage[5::9]]), 2)
    results['away_league_avarage_defence'] = round(np.mean([float(val) for val in away_avarage[6::9]]), 2)
    results['home_teams_avarage'] = [float(val) for val in home_avarage[5::9]]
    results['away_teams_avarage'] = [float(val) for val in away_avarage[5::9]]
    results['home_teams_avarage_defence'] = [float(val) for val in home_avarage[6::9]]
    results['away_teams_avarage_defence'] = [float(val) for val in away_avarage[6::9]]
    return results


def get_scheduled_games(results):
    request_data = requests.get(SCHEDULE_URL)
    tree_request_data = html.fromstring(request_data.content)
    games = [val.split(" vs ") for val in list(set(tree_request_data.xpath(SCHEDULED_GAMES_XPATH)))]
    games = [[team.replace('game ', '') for team in game] for game in games]
    games_count = 0
    # this loop is needed to make equal names for statistics source and schedule source
    # thats because in those sources names are different for some teams
    # and because of that it needs to be made equal as it is in statistics source
    for game in games:
        team_count = 0
        for team in game:
            team = team.split()
            for t in results['teams']:
                t = t.split()
                if len(set(team) & set(t)) > 1:
                    games[games_count][team_count] = ' '.join(t)
                else: # else condition is needed if there only one word equal but it is not like FC, AS BC or etc...
                      # but it is full name like for e.x. Olympiacos
                    for a, b in zip(team, t):
                        if a == b and len(a) > 2 and len(b) > 2 or (a == 'AS' and b == 'Monaco') or (
                                a == 'FC' and b == 'Barcelona'): # dirty work around
                            games[games_count][team_count] = ' '.join(t)
            team_count += 1
        games_count += 1
    filter_games = []
    for game in games:
        if [game[1], game[0]] not in filter_games:
            filter_games.append(game)
    return filter_games


def calculate_koef(games_list, results):
    results['attack_strength'] = {}
    results['defence_strength'] = {}
    for game in games_list:
        home_team_index = results['teams'].index(game[0])
        away_team_index = results['teams'].index(game[1])
        attack_strength_home_koef = round((float)(results['home_teams_avarage'][
                                                 home_team_index] / results['home_league_avarage_offence']), 2)
        defense_strength_home_koef = round((float)(results['home_teams_avarage_defence'][
                                                 home_team_index] / results['home_league_avarage_defence']), 2)
        results['attack_strength'][game[0]] = attack_strength_home_koef
        results['defence_strength'][game[0]] = defense_strength_home_koef
        attack_strength_away_koef = round((float)(results['away_teams_avarage'][
                                                 away_team_index] / results['away_league_avarage_offence']), 2)
        defense_strength_away_koef = round((float)(results['away_teams_avarage_defence'][
                                                 away_team_index] / results['away_league_avarage_defence']), 2)
        results['attack_strength'][game[1]] = attack_strength_away_koef
        results['defence_strength'][game[1]] = defense_strength_away_koef
    return results


def calculate_potencial_result(games_list, results):
    results['potencial_results'] = {}
    for game in games_list:
        potencial_result_home = round(results['attack_strength'][game[0]
                                      ] * results['defence_strength'][game[1]
        ] * results['home_league_avarage_offence'], 0)
        potencial_result_away = round(results['attack_strength'][game[1]
                                      ] * results['defence_strength'][game[0]
        ] * results['away_league_avarage_offence'], 0)
        results['potencial_results'][' vs '.join([game[0], game[1]])] = {potencial_result_home: potencial_result_away}
    return results
