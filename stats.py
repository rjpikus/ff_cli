# NFL Import
import re
from espn_api.football import League
from datetime import datetime, timedelta
from nfl_week import nfl_week
from league_config import league, get_owner
from diff import total_diff, format_player_name  # Import the total_diff from the first script


team = league.teams[2]

print("\nRJ")
for pl in team.roster :
    print(pl.position,pl.posRank,pl.proTeam,pl.name)

for i in range(10):
    team = league.teams[i]
    owner = get_owner(team.team_name)
    print("\n", owner)

    # Defining the header
    header = "Name   PlayerId PosRank EligSlots  AcqType ProTeam OnTeamId Position InjuryStatus Injured TotalPts ProjPts %Owned %Started"
    print(header)

    for pl in team.roster:
        # Extracting and formatting the data
        name = pl.name.ljust(7)[:7]  # Assuming player names can be long, truncating to 7 characters
        playerId = str(pl.playerId).ljust(8)
        posRank = str(pl.posRank).ljust(8)
        eligibleSlots = '/'.join(pl.eligibleSlots).ljust(11)[:11]  # Using the first two eligible slots, truncating for space
        acquisitionType = pl.acquisitionType.ljust(4)[:4]
        proTeam = pl.proTeam.ljust(8)[:8]
        onTeamId = str(pl.onTeamId).ljust(8)
        position = pl.position.ljust(8)
        injuryStatus = pl.injuryStatus.ljust(12)[:12]
        injured = 'Yes' if pl.injured else 'No'
        injured = injured.ljust(8)
        total_points = str(pl.total_points).ljust(8)
        projected_total_points = str(pl.projected_total_points).ljust(8)
        percent_owned = str(pl.percent_owned).ljust(8)
        percent_started = str(pl.percent_started).ljust(8)
        season_diff = str(round(pl.total_points - pl.projected_total_points)).ljust(8)[:8]
        diff_value = total_diff.get(format_player_name(pl.name), 0)
        curr_diff = str(round(diff_value)).ljust(8)[:8]

        # Printing out the formatted data for each player
        print(f"{name} {playerId} {posRank} {eligibleSlots} {acquisitionType} {proTeam} {onTeamId} {position} {injuryStatus} {injured} {total_points} {projected_total_points} {percent_owned} {percent_started} {season_diff[:4]} {curr_diff[:4]}")














