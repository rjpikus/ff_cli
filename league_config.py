import re
from espn_api.football import League

# Your league connection and teams mapping
league = League(league_id=377713, year=2023, espn_s2='', swid='')
team = league.teams[2]

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
