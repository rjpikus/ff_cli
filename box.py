# NFL Import
import re
from espn_api.football import League
from datetime import datetime, timedelta

def nfl_week(week=None):
    # Define the start date of the NFL season for week 1
    start_date = datetime(2023, 9, 5)  # Adjust this date to the actual starting date for Week 1 each year

    if week :
        return week
        
    today = datetime.now()

    # Calculate the number of days since the start
    days_since_start = (today - start_date).days

    # Adjust for the week starting on Tuesday
    days_since_start = days_since_start + 1 if days_since_start >= 0 else days_since_start

    # Calculate current week
    current_week = (days_since_start // 7) + 1

    return current_week

week = nfl_week(6)


# private league with cookies
league = League(league_id=377713, year=2023, espn_s2='AEBo%2FDSghEyopRom%2B%2FtMgQCVgob4m4CHfgKjaZuQQ1qMfA0q4%2Bl96vz8GqY3A47mEjQRyNvkbpZUHLH4o%2FihdFf30ziCTDW42NN5LadgbWMYF6MIHoMf%2FQmYESVDZM4WyOIesWzu%2FEm57BCXy8lLTj31%2B1LHkyEb5GUzAWEFLD70hZ8evjJvKG6X11wKl7CHlAnBMTfK7doJpgBV4LDWZobIaTLYM4xGJk46ab6wcxgSa258nFGbbxkqtuMZnvogmxBGDGiw7L0c4TxUnkbPqmiu', swid='{05B48DDE-7249-4D88-B48D-DE72494D88D4}')


teams_to_owners = {
    'Dark Horses': 'Brandon',
    '2 Time Procreator': 'Shaker',
    'Players Team': 'RJ',
    'King Henry\'s Kingdom': 'Mason',
    'TY RPenny': 'Brett',
    'Big Booty Mix 28': 'Kyle',
    'RIP My Chubby': 'Ben',
    'Mixon Gin and JuJuice': 'Adam',
    'Double Reeked Up': 'Roger',
    'columbus im the winner': 'Tom'
}

def get_owner(team_string):

    if team_string in teams_to_owners:
        return teams_to_owners[team_string]
    else:
        # Extract team name from the input string
        match = re.search(r"Team\((.*?)\)", team_string)
        if match:
            team_name = match.group(1)

    # If team name is in dictionary, return the corresponding owner
    if team_name in teams_to_owners:
        return teams_to_owners[team_name]
    else:
        # If team name is not found, look for a missing owner
        for owner in teams_to_owners.values():
            if owner not in [teams_to_owners[team] for team in teams_to_owners]:
                # Update the team name for this owner
                for key in teams_to_owners:
                    if teams_to_owners[key] == owner:
                        teams_to_owners[team_name] = teams_to_owners.pop(key)
                        return owner
        return "Owner not found"



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
