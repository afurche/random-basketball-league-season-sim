

class StatLeadersProvider:

    @classmethod
    def get_stat_leaders(cls, league, season_number=0):  # season_number will be changing when multiple seasons are implemented
        all_players = [player for team_players in [team.players for team in league] for player in team_players]   # flattened list of all players
        ppg_leader = sorted(all_players, key=lambda p: p.season_avg[season_number]['ppg'], reverse=True)[0]
        apg_leader = sorted(all_players, key=lambda p: p.season_avg[season_number]['apg'], reverse=True)[0]
        bpg_leader = sorted(all_players, key=lambda p: p.season_avg[season_number]['bpg'], reverse=True)[0]
        spg_leader = sorted(all_players, key=lambda p: p.season_avg[season_number]['spg'], reverse=True)[0]

        return ppg_leader, apg_leader, bpg_leader, spg_leader
