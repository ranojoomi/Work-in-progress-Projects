from dataclasses import dataclass
from collections import OrderedDict
from prettytable import PrettyTable
import pandas as pd
import matplotlib.pyplot as plt
import time
import math


@dataclass
class team_info:
    name: str
    elo: int
    games_played: int
    historic_elo: list

starting_elo = 1500

teams = [
    "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets",
    "Charlotte Hornets", "Chicago Bulls", "Cleveland Cavaliers",
    "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons",
    "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
    "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies",
    "Miami Heat", "Milwaukee Bucks", "Minnesota Timberwolves",
    "New Orleans Pelicans", "New York Knicks", "Oklahoma City Thunder",
    "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns",
    "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs",
    "Toronto Raptors", "Utah Jazz", "Washington Wizards"
]

team = []

d = OrderedDict()
for idx, value in enumerate(teams):
    key = 'team' + str(idx)
    d[key] = team_info(value, starting_elo, 0, [])
    team.append(d[key])

df = pd.read_csv("C:\\Users\\radin\\Desktop\\Data\\data_v2.csv")

# Defining some constants
def rating_update(winner_r, loser_r, mov, k):

    exp_value = 1 / (1 + (10 ** ((loser_r - winner_r) / 400)))
    rating_diff = winner_r - loser_r

    mov_multiplier = math.log(mov + 1) * (2.2 / (rating_diff * 0.001 + 2.2))
    new_winner_r = winner_r + k * mov_multiplier * (1 - exp_value)
    new_loser_r = loser_r + k * mov_multiplier * (0 - exp_value)

    return new_winner_r, new_loser_r

for i in range(6567, len(df)):
    home_team = df["Home/Neutral"].iloc[i]
    away_team = df["Visitor/Neutral"].iloc[i]

    k = 10

    try:
        home_points = int(df["PTS.1"].iloc[i])
        away_points = int(df["PTS"].iloc[i])

    except ValueError:
        continue

    for j in range(len(team)):

        if home_team == team[j].name:

            home_team = team[j].name
            home_elo = team[j].elo
            home_index = j
            team[j].historic_elo.append(home_elo)

    for s in range(len(team)):

        if away_team == team[s].name:

            away_team = team[s].name
            away_elo = team[s].elo
            away_index = s
            team[s].historic_elo.append(away_elo)

    if home_points > away_points:

        margin = int(home_points) - int(away_points)

        team[home_index].elo = rating_update(team[home_index].elo, team[
                                             away_index].elo, margin, k)[0]
        team[away_index].elo = rating_update(team[home_index].elo, team[
                                             away_index].elo, margin, k)[1]

        team[home_index].games_played += 1
        team[away_index].games_played += 1

    elif away_points > home_points:

        margin = int(away_points) - int(home_points)

        team[away_index].elo = rating_update(team[away_index].elo, team[
                                             home_index].elo, margin, k)[0]
        team[home_index].elo = rating_update(team[away_index].elo, team[
                                             home_index].elo, margin, k)[1]

        team[home_index].games_played += 1
        team[away_index].games_played += 1


t = PrettyTable(["Team", "Elo", "Games Played"])
t.align = "l"

for i in range(len(team)):
    t.add_row([team[i].name, round(team[i].elo), team[i].games_played])

t.sortby = "Elo"
t.reversesort = True

print(t)

t_text = t.get_string()
