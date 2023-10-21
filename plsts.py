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



# private league with cookies
league = League(league_id=377713, year=2023, espn_s2=' ', swid='{  }')


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
    projected_points = "{:2}".format(round(pla.projected_points))
    points = "{:2}".format(round(pla.points))

    name_parts = pla.name.split()
    first_name = name_parts[0]
    last_name = name_parts[-1]
    name = f"{first_name[0]}.{last_name}"
    name = name[:6].ljust(6)  # Limit the name to 6 characters and pad with spaces if shorter

    return (name, points, projected_points)

players_data = []

# Fetch Free Agents
free_agents = league.free_agents(size=50)  # you might need to adjust the size based on the league's number of players

# Concatenate rosters of all teams and free agents
all_players = free_agents
for team in league.teams:
    all_players.extend(team.roster)

# Process each player's data
for player in all_players:
    player_name = player.name
    for week, (proj, points) in enumerate(zip(player.projected_points, player.points), start=1):
        diff = points - proj
        players_data.append({
            'Name': player_name,
            'Week': week,
            'Projected': proj,
            'Actual': points,
            'Difference': diff
        })

# Your data is now organized in the players_data list

from collections import defaultdict

organized_data = defaultdict(lambda: defaultdict(dict))
for p in players_data:
    short_name = f"{p['Name'].split()[0][0]}.{p['Name'].split()[1][:3]}"
    organized_data[short_name][p['Week']] = {'Projected': p['Projected'], 'Actual': p['Actual'], 'Difference': p['Difference']}

# Define and print headers
header = "Player".ljust(12)
number_of_weeks = max([p['Week'] for p in players_data])

for week in range(1, number_of_weeks + 1):
    header += f"Week {week}".center(20)
print(header)
print('-' * len(header))

# Print player data
for name, weeks_data in organized_data.items():
    row = name.ljust(12)
    for week in range(1, number_of_weeks + 1):
        if week in weeks_data:
            proj = weeks_data[week]['Projected']
            actual = weeks_data[week]['Actual']
            diff = weeks_data[week]['Difference']
            row += f"{actual} | {proj} | {diff}".center(20)
        else:
            row += "".center(20)  # Empty space for weeks without data
    print(row)
