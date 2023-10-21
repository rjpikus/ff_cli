import re
from espn_api.football import League
from datetime import datetime, timedelta
from nfl_week import nfl_week
from league_config import league, get_owner, format_player_name

def format_opponent_name(opponent_name):
    """Format the opponent's name to be exactly 3 characters."""
    return (opponent_name[:3]).upper()

for i in range(10): 
    team = league.teams[i]
    owner = get_owner(team.team_name)
    print("\n", owner)
    
    for pl in team.roster:
        # Create a string of the player's schedule with each opponent name formatted
        formatted_schedule = ', '.join([format_opponent_name(opp) for opp in pl.schedule[0:18]])
        print(pl.position, pl.posRank, pl.proTeam, format_player_name(pl.name), formatted_schedule)
