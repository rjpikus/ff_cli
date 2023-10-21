import re
from espn_api.football import League
from nfl_week import nfl_week
from league_config import league
import sys

def format_player_name(name):
    if "D/ST" in name :
        formatted_name = name[:7]
    else :
        name_parts = name.split()
        first_name = name_parts[0]
        name_parts = name.split()
        first_name = name_parts[0]
        last_name = name_parts[-1]
        if len(name_parts) > 2 :
            mid_name = name_parts[1]
            name = f"{first_name[0]}.{mid_name[0]}.{last_name}"
        else: 
            name = f"{first_name[0]}.{last_name}"
        name = name[:8].ljust(8)

        formatted_name = name
    return formatted_name

def calculate_total_diff():
    players_diff = {}
    for week in range(1, nfl_week() + 1):
        box_scores = league.box_scores(week)
        for box_score in box_scores:
            for player in box_score.home_lineup:
                diff = player.points - player.projected_points
                players_diff[format_player_name(player.name)] = players_diff.get(format_player_name(player.name), 0) + diff
            for player in box_score.away_lineup:
                diff = player.points - player.projected_points
                players_diff[format_player_name(player.name)] = players_diff.get(format_player_name(player.name), 0) + diff
    return players_diff

total_diff = calculate_total_diff()

# Getting all players and their stats
all_players = []
for team in league.teams:
    for pl in team.roster:
        player_data = {
            'name': format_player_name(pl.name).ljust(10)[:10],
            'playerId': str(pl.playerId).ljust(0)[:0],
            'posRank': str(pl.posRank).ljust(8),
            'eligibleSlots': '/'.join(pl.eligibleSlots).ljust(0)[:0],
            'acquisitionType': pl.acquisitionType.ljust(4)[:1],
            'proTeam': pl.proTeam.ljust(8)[:8],
            'onTeamId': str(pl.onTeamId).ljust(8),
            'position': pl.position.ljust(3)[:2],
            'injuryStatus': pl.injuryStatus[:2].ljust(4),
            'injured': 'Y' if pl.injured else 'N',
            'total_points': str(round(pl.total_points))[:3].ljust(5),
            'projected_total_points': str(round(pl.projected_total_points))[:3].ljust(5),
            'percent_owned': str(round(pl.percent_owned))[:0].ljust(0),
            'percent_started': str(round(pl.percent_started))[:0].ljust(0),
            'season_diff': str(round(pl.total_points - pl.projected_total_points)).ljust(8)[:8],
            'curr_diff': str(round(total_diff.get(format_player_name(pl.name), 0))).ljust(8)[:8]
        }
        all_players.append(player_data)

# Sorting based on provided argument
sort_key = sys.argv[1]
all_players.sort(key=lambda x: float(x[sort_key]))

# Print all players based on the sorted order
header = "Name   \t PR  \t    Acq PrT \tOwn     Pos In  Inj ToPt ProjP  SeaDif  CurDif"
print(header)
for player in all_players:
    print(f"{player['name']} {player['playerId']} {player['posRank']} {player['eligibleSlots']} {player['acquisitionType']} {player['proTeam']} {player['onTeamId']} {player['position']} {player['injuryStatus']} {player['injured']} {player['total_points']} {player['projected_total_points']} {player['percent_owned']} {player['percent_started']} {player['season_diff']} {player['curr_diff']}")

if __name__ == "__main__":
    pass
