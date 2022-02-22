from pandas import read_csv
from generators.team_generator import TeamGenerator


class LeagueGenerator:
    cities = read_csv("generators/cities.txt", sep="\n", header=None)[0]
    team_names = read_csv("generators/team_names.txt", sep="\n", header=None)[0]
    arena_names = read_csv("generators/arena_names.txt", sep="\n", header=None)[0]

    @classmethod
    def generate_league(cls):
        league = []
        for team_name, city, arena_name in zip(cls.team_names[:10], cls.cities[:10], cls.arena_names[:10]):
            league.append(TeamGenerator.generate_team(team_name, city, arena_name))
        return league

