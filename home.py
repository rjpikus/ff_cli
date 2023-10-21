# NFL Import
import re
import time
from espn_api.football import League
from datetime import datetime, timedelta
from nfl_week import nfl_week
from league_config import league, get_owner

print("")
print("\nPOWER RANKINGS")
for te in league.power_rankings(week=7) :
    print(te[0], get_owner(str(te[1])))

print("")
print("\nBUDGET")
budgets = {}
for te in league.teams:
    cash = 1000 - te.acquisition_budget_spent
    budgets[te.team_name] = (cash)  # Store team name as key and cash as value

# Convert dictionary to a list of tuples and sort by budget
sorted_budgets = sorted(budgets.items(), key=lambda x: x[1], reverse=True)

# Print the sorted budgets
for team, budget in sorted_budgets:
    budgets[te.team_name] = "{:4}".format(budget) 
    print(f"${budget} {get_owner(team)} ")
 
print("\nRJ")
team = league.teams[2]
for pl in team.roster :
    print(pl.position,pl.posRank,pl.proTeam,pl.name)

print("\nACTIVITY")
    # Removing the "Activity(" prefix and the trailing ")"
moves = {}

data_string = str(league.recent_activity())

def extract_data(data_string):
    # Extract all the relevant parts using regex
    patterns = re.findall(r"Team\((.*?)\),(DROPPED|WAIVER ADDED|TRADED),Player\((.*?)\)", data_string)

    # Organize the data
    data = {}
    for team, action, player in patterns:
        if team not in data:
            data[team] = []

        # add the action and player
        data[team].append((action, player))
        
    return data

 # Your provided string goes here
extracted_data = extract_data(data_string)

data = extracted_data
# Let's replace "WAIVER ADDED" with "ADDED" for simplicity
for team, actions in data.items():
    data[team] = [(action.replace("WAIVER ADDED", "ADDED"), player) for action, player in actions]

# Organize the data for each team
organized_data = {}
for team, actions in data.items():
    team_data = {}
    for action, player in actions:
        if action not in team_data:
            team_data[action] = []
        team_data[action].append(player)
    organized_data[team] = team_data

# Print the data in the desired format
for team, actions in organized_data.items():
    print(get_owner(str(team)))
    for action, players in actions.items():
        print(action)
        for player in players:
            print(player)
    print()











