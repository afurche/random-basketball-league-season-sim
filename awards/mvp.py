

class Mvp:

    @classmethod
    def find_mvp(cls, league):
        all_players = [player for team_players in [team.players for team in league] for player in team_players]  # flattened list of all players
        return sorted(all_players, key=lambda p: p.calculate_mvp_score(league), reverse=True)[0]  # player with highest mvp_score wins mvp award



