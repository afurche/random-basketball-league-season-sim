from generators.player_generator import PlayerGenerator
from team import Team


class TeamGenerator:

    @classmethod
    def generate_team(cls, team_name, city, arena_name):
        return Team(team_name,
                    city,
                    arena_name,
                    [PlayerGenerator.generate_player("PG", team_name),
                     PlayerGenerator.generate_player("SG", team_name),
                     PlayerGenerator.generate_player("SF", team_name),
                     PlayerGenerator.generate_player("PF", team_name),
                     PlayerGenerator.generate_player("C", team_name)])
