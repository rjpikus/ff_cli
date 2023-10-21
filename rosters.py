# NFL Import
import re
from espn_api.football import League
from datetime import datetime, timedelta
from nfl_week import nfl_week
from league_config import league, get_owner


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

for i in range(10) : 
    team = league.teams[i]
    owner = get_owner(team.team_name)
    print("\n", owner)
    for pl in team.roster :
        print(pl.position,pl.posRank,pl.proTeam,pl.name)













