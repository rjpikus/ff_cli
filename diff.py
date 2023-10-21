# total_diff_calculator.py
import re
from espn_api.football import League
from nfl_week import nfl_week
from league_config import format_player_name

players_diff = {}

def get_diff() :
    name = format_player_name(name)
    positive_players = [(name, diff) for name, diff in total_diff.items() if diff >= 0]
    negative_players = [(name, diff) for name, diff in total_diff.items() if diff < 0]

    positive_players.sort(key=lambda x: x[1], reverse=True)
    negative_players.sort(key=lambda x: x[1])

    max_len = max(len(positive_players), len(negative_players))

    while len(positive_players) < max_len:
        positive_players.append(('N/A\t', 0))
    while len(negative_players) < max_len:
        negative_players.append(('N/A\t', 0))

    total_positive = sum([x[1] for x in positive_players])
    total_negative = sum([x[1] for x in negative_players])

    print(f"Total Positive: {total_positive:.2f}")
    print(f"Total Negative: {total_negative:.2f}\n")

    for pos, neg in zip(positive_players, negative_players):
        print(f"{pos[0]} {str(round(pos[1]))[:3]} \t|\t {str(round(neg[1]))[:3]} {neg[0]}")



def calculate_total_diff():
    for week in range(1, nfl_week()):
        box_scores = league.box_scores(week)
        for box_score in box_scores:
            for player in box_score.home_lineup:
                diff = player.points - player.projected_points
                players_diff[format_player_name(player.name)] = players_diff.get(format_player_name(player.name), 0) + diff
            for player in box_score.away_lineup:
                diff = player.points - player.projected_points
                players_diff[format_player_name(player.name)] = players_diff.get(format_player_name(player.name), 0) + diff

    return players_diff

years = [2023]
for y in years : 
    league = League(league_id=377713, year=y, espn_s2=' ', swid='{  }')
    total_diff = calculate_total_diff()

# If this script is run on its own, then print the results
if __name__ == "__main__":
    get_diff()
