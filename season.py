from game import Game
from generators.league_generator import LeagueGenerator
from generators.calendar_generator import CalendarGenerator
from awards.stat_leaders import StatLeadersProvider
from awards.mvp import Mvp


class SeasonSimulation:
    def __init__(self):
        self._teams = LeagueGenerator.generate_league()
        self._calendar = CalendarGenerator.create_calendar()
        self._games = [Game(self._teams[tms[1][0]], self._teams[tms[1][1]], tms[0]) for tms in self._calendar]
        self._scores = []  # list of strings with all of the match scores prepared to be printed in gui

    @property
    def teams(self):
        return self._teams

    @property
    def scores(self):
        return self._scores

    def sum_team_player_season_stats(self):
        for team in self._teams:
            team.team_player_sum_season_stats()

    def find_team_by_name(self, team_name):
        for team in self._teams:
            if team.name == team_name:
                return team

    def create_team_ranking(self):
        ranked_teams = sorted(self._teams, key=lambda t: t.calculate_team_record()[0], reverse=True)
        return [[standing + 1, team.city, team.name, team.calculate_team_record()] for standing, team in zip(list(range(len(self._teams))), ranked_teams)]

    def print_season_team_ranking(self):
        standings = []
        for team in self.create_team_ranking():
            team_standing = ''
            for item in team:
                team_standing += ' ' + str(item)
            standings.append(team_standing)
        return standings

    def print_season_stat_leaders(self, season_num=0):
        ppg_leader, apg_leader, bpg_leader, spg_leader = StatLeadersProvider.get_stat_leaders(self._teams)

        ppg = f'PPG Leader: {ppg_leader.name} {ppg_leader.season_avg[season_num]["ppg"]} PPG Team : {ppg_leader.team}'
        apg = f'APG Leader: {apg_leader.name} {apg_leader.season_avg[season_num]["apg"]} APG Team : {apg_leader.team}'
        bpg = f'BPG Leader: {bpg_leader.name} {bpg_leader.season_avg[season_num]["bpg"]} BPG Team : {bpg_leader.team}'
        spg = f'SPG Leader: {spg_leader.name} {spg_leader.season_avg[season_num]["spg"]} SPG Team : {spg_leader.team}'

        return [ppg, apg, bpg, spg]

    def print_mvp(self, season_num=0):
        mvp = Mvp.find_mvp(self._teams)
        return f'Most Valuable Player: {mvp.name} {mvp.season_avg[season_num]} Team : {mvp.team}'

    def season_sim(self):
        for game in self._games:
            self._scores.append(game.match_sim() + '\n')
        self.sum_team_player_season_stats()