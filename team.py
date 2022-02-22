
class Team:
    def __init__(self, name, city, arena, players):
        """
        :param name: Team name
        :param city: Team city
        :param arena: Name of local arena of the team
        :param players: List of team's players (only starting 5, full team may be added someday)
        """
        self._name = name
        self._city = city
        self._arena = arena
        self._players = players
        self._season_stats = []
        self._game_results = []  # list containing result of each game (W or L)

    @property
    def name(self):
        return self._name

    @property
    def arena(self):
        return self._arena

    @property
    def city(self):
        return self._city

    @property
    def season_stats(self):
        return self._season_stats

    @property
    def players(self):
        return self._players

    @property
    def game_results(self):
        return self._game_results

    def team_player_get_attribute(self, ind, key):
        return self._players[ind].attributes[key]

    def team_player_score_stat(self, ind, key, val=1):
        self._players[ind].score_stat(key, val)

    def team_players_show_game_stats(self):
        for p in self._players:
            p.show_game_stats()

    def add_game_to_season_stats(self, game_stats):
        self._game_results.append(game_stats['w/l'])
        self._season_stats.append(game_stats)

    def team_player_add_game_to_season_stats(self):
        for p in self._players:
            p.add_game_stats_to_season()

    def team_player_sum_season_stats(self):
        for p in self._players:
            p.calculate_season_stats()

    def calculate_team_record(self):
        return [self._game_results.count('W'), self._game_results.count('L')]

    def calculate_win_loss_diff(self):
        return self._game_results.count('W') - self._game_results.count('L')

    def get_team_players_season_avg_str(self):
        players_avg_strs = []
        for player in self._players:
            players_avg_strs.append(player.get_season_avg_string())
        return players_avg_strs

    def get_team_season_avg_stats(self):
        avg_stats_keys = ['score', "2pt_made", "2pt_attempt", "3pt_made", "3pt_attempt", 'fg%', '2pt_fg%', '3pt_fg%']
        sum_stats = [0 for _ in range(len(avg_stats_keys))]
        for game_stat in self._season_stats:
            gs = game_stat.copy()
            gs.pop('opponent')
            gs.pop('w/l')
            for i, stat in enumerate(gs.values()):
                sum_stats[i] += int(stat)
        return {key: round(stat/len(self._season_stats), 2) for key, stat in zip(avg_stats_keys, sum_stats)}

    def get_team_season_game_stats_str(self):
        season_game_stats_strs = []
        for game_stat in self._season_stats:
            game_stat_str = ''
            for key, val in game_stat.items():
                if key == 'w/l':
                    game_stat_str += f'W/L: {val}   '
                else:
                    try:
                        val_int = int(val)
                        game_stat_str += f'{key.capitalize()}: {round(val_int, 4)}   '
                    except ValueError:
                        game_stat_str += f'{key.capitalize()}: {val}   '

            season_game_stats_strs.append(game_stat_str)
        return season_game_stats_strs

    def get_player_season_game_stats_by_name_and_surname(self, name):
        for player in self._players:
            if player.name == name:
                return player





