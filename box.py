# NFL Import
import re
from espn_api.football import League
from datetime import datetime, timedelta
from nfl_week import nfl_week
from league_config import league, format_player_name, get_owner

#specif format for boxes
def format_player(pla):
    """Format player data for printing."""
    diff = "{:3}".format(round(pla.points - pla.projected_points))
    projected_points = "{:2}".format(round(pla.projected_points))
    points = "{:2}".format(round(pla.points))
    

    name_parts = pla.name.split()
    first_name = name_parts[0]
    last_name = name_parts[-1]
    name = f"{first_name[0]}.{last_name}"
    name = name[:6].ljust(6)  # Limit the name to 6 characters and pad with spaces if shorter

    return (name, points, projected_points, diff)

def get_sorted_lineup(box_score, home=True):
    """Retrieve sorted lineup for home/away."""
    lineup = box_score.home_lineup if home else box_score.away_lineup
    return sorted(lineup, key=lambda pla: pla.projected_points, reverse=True)

def box_scores(week) :
    all_scores = []
    for box_scores in league.box_scores(week):
        home_data = [format_player(pla) for pla in get_sorted_lineup(box_scores)]
        away_data = [format_player(pla) for pla in get_sorted_lineup(box_scores, home=False)]
        all_scores.append((home_data, away_data, box_scores.home_team, box_scores.away_team))



    onr = []
    for box_scores in league.box_scores(week):
        ht = box_scores.home_team
        at = box_scores.away_team
        ho = get_owner(str(ht))[:7].rjust(7) + str(format(round(box_scores.home_score)))[:4].rjust(4)
        onr.append(ho)
        ao = str(format(round(box_scores.away_score)))[:3].ljust(4) + get_owner(str(at))[:7].ljust(7)
        onr.append(ao)



    print("\n WEEK " + str(week))
    print()

    print("    ", onr[0], onr[1], "\t\t", onr[2], "", onr[3], "\t\t", onr[4], "", onr[5], "\t\t", onr[6], "", onr[7], "\t\t", onr[8], "", onr[9])


    # Now, print out player rows
    max_lineup_length = max(len(home_data) for home_data, _, _, _ in all_scores)
    for i in range(16):
        for home_data, away_data, _, _ in all_scores:
            home_player = home_data[i] if i < len(home_data) else ("", "", "")
            away_player = away_data[i] if i < len(away_data) else ("", "", "")
            print(f"{home_player[3]}|{home_player[0]}|{home_player[2]}|{home_player[1]} {away_player[1]}|{away_player[2]}|{away_player[0]}|{away_player[3]}", end="  ")
        print()

    print()

for week in range(1, nfl_week(18) + 1):
    box_scores(week)