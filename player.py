import numpy as np


class Player:
    def __init__(self, name, surname, position, attributes, team_name):
        """
        :param name: First name of player
        :param surname: Surname of player
        :param position: Position of player (PG, SG, SF, PF, C)
        :param attributes: list of 9 int values (in the range 50:99), attributes on indexes [0:3] describe offensive attributes, [4:8] describe defensive attributes
        order of attr -> layups, mid_range, long_range, passing, ball_handling, perimeter_defence, paint_defence, stealing, blocking
        """

        self._name = name
        self._surname = surname
        self._position = position
        self._team = team_name

        self._offence_ovr = np.round((sum(attributes[0:3]) / len(attributes[0:3])), 1)
        self._defense_ovr = np.round((sum(attributes[4:8]) / len(attributes[4:8])), 1)
        self._overall = (self._offence_ovr + self._offence_ovr) / 2

        self._attribute_labels = ['layups', 'mid_range', 'long_range', 'passing', 'ball_handling', 'perimeter_defence', 'paint_defence', 'stealing', 'blocking']
        self._attributes = {label: value for label, value in zip(self._attribute_labels, attributes)}

        self.game_stats_keys = ["points", "assists", "blocks", "steals"]
        self.game_stats = dict.fromkeys(self.game_stats_keys, 0)
        self._season_stats = []  # list containing lists with stats from each game the player played in during a season
        self._season_stats_sum = []  # list containing sum of each statistic from each game the player played during a season

        self._season_avg_keys = ['ppg', 'apg', 'bpg', 'spg']
        self._season_avg = []

    def print_player(self):
        print(f'Name: {self._name} \n'
              f'Surname: {self._surname} \n'
              f'Offensive overall: {self._offence_ovr} \n'
              f'Defensive overall: {self._defense_ovr} \n')

    def clear_game_stats(self):
        for key in self.game_stats.keys():
            self.game_stats[key] = 0

    @property
    def name(self):
        return self._name + ' ' + self._surname

    @property
    def attributes(self):
        return self._attributes

    @property
    def team(self):
        return self._team

    @property
    def season_stats(self):
        return self._season_stats

    @property
    def season_stats_sum(self):
        return self._season_stats_sum

    @property
    def season_avg(self):
        return self._season_avg

    def score_stat(self, key, val):
        self.game_stats[key] += val

    def show_game_stats(self):
        print(f'{self._name} {self._surname} | PTS: {self.game_stats["points"]}, AST: {self.game_stats["assists"]}, BLK: {self.game_stats["blocks"]}, STL: {self.game_stats["steals"]}')

    def add_game_stats_to_season(self):
        self._season_stats.append({key: val for key, val in zip(self.game_stats_keys, [val for val in self.game_stats.values()])})
        self.clear_game_stats()

    def calculate_season_stats(self, season_num=0):  # when multiple seasons are introduced this value will become dynamic

        self._season_stats_sum.append({key: val for key, val in zip(self.game_stats_keys, [sum(stat) for stat in zip(*[stats_dict.values() for stats_dict in self._season_stats])])})
        self._season_avg.append({key: np.round(val / len(self._season_stats), 2) for key, val in zip(self._season_avg_keys, self._season_stats_sum[season_num].values())})

    def calculate_mvp_score(self, league, season_num=0):
        individual_performance = self.season_avg[season_num]['ppg'] * 0.4 + self.season_avg[season_num]['apg'] * 0.2 + self.season_avg[season_num]['bpg'] * 0.2 + self.season_avg[season_num]['spg'] * 0.2
        team_performance = None
        for ind, t in enumerate(league):
            if t.name == self._team:
                team_performance = league[ind].calculate_win_loss_diff() * 0.5

        return individual_performance + team_performance

    def get_season_avg_string(self, season_num=0):
        season_avg_str = f'{self._name} {self._surname} '
        for key, val in self._season_avg[season_num].items():
            season_avg_str += f'{key.upper()}: {val} '
        return season_avg_str

    def get_season_game_strings(self, season_num=0):
        season_games_strs = []
        for game_stat in self._season_stats:
            game_str = ''
            for key, val in game_stat:
                game_str += f'{key.capitalize()}: {val}'
            season_games_strs.append(game_str)
        return season_games_strs

