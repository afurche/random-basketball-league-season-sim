import numpy as np
import random


class Game:
    def __init__(self, t1, t2, date):
        self._t1 = t1
        self._t2 = t2
        self._stats_labels = ["score", "2pt_made", "2pt_attempt", "3pt_made", "3pt_attempt"]
        self._t1_stats = dict.fromkeys(self._stats_labels, 0)
        self._t2_stats = dict.fromkeys(self._stats_labels, 0)
        self._date = date

    def choose_home(self):
        return self._t1.city

    def return_score(self):
        return f'Date: {self._date}  {self._t1.name} {self._t1_stats["score"]} : {self._t2_stats["score"]} {self._t2.name}'

    def team_score(self, team, val):
        if team == self._t1:
            if val == 2:
                self._t1_stats["score"] += 2
                self._t1_stats["2pt_made"] += 1
            elif val == 3:
                self._t1_stats["score"] += 3
                self._t1_stats["3pt_made"] += 1

        elif team == self._t2:
            if val == 2:
                self._t2_stats["score"] += 2
                self._t2_stats["2pt_made"] += 1
            elif val == 3:
                self._t2_stats["score"] += 3
                self._t2_stats["3pt_made"] += 1

    def team_attempt(self, team, val):
        if team == self._t1:
            if val == 2:
                self._t1_stats["2pt_attempt"] += 1
            elif val == 3:
                self._t1_stats["3pt_attempt"] += 1

        elif team == self._t2:
            if val == 2:
                self._t2_stats["2pt_attempt"] += 1
            elif val == 3:
                self._t2_stats["3pt_attempt"] += 1

    def playmaking(self, player, t_off, t_def):
        if np.random.random() < (0.01 - (t_off.team_player_get_attribute(player, "ball_handling") - t_def.team_player_get_attribute(player, "stealing")) / 5000):
            t_def.team_player_score_stat(player, "steals")
            self.team_attempt(t_def, 2)
            if np.random.random() < 0.95:
                self.team_score(t_def, 2)
                t_def.team_player_score_stat(player, "points", 2)
        return player

    def passing(self, player, t_off, t_def):
        number_of_passes = random.randint(1, 8)  # passing
        passer = None
        while number_of_passes != 0:
            if np.random.random() < (0.01 - (t_off.team_player_get_attribute(player, "passing") - t_def.team_player_get_attribute(player, "stealing")) / 5000):
                t_def.team_player_score_stat(player, "steals")
                self.team_attempt(t_def, 2)
                if np.random.random() < 0.95:
                    self.team_score(t_def, 2)
                    t_def.team_player_score_stat(player, "points", 2)
                    break
            else:
                tmp = [1, 1, 1, 1, 1]
                tmp[player] = 0
                passer = player
                player = random.choices([0, 1, 2, 3, 4], tmp, k=1)[0]
                number_of_passes -= 1

        return player, passer

    def scoring(self, player, passer, t_off, t_def):
        if np.random.random() < 0.65:  # 2 point mid range shot
            if np.random.random() < 0.5 + t_off.team_player_get_attribute(player, "mid_range") / 500:  # mid_range
                self.team_attempt(t_off, 2)
                if np.random.random() > (0.5 - ((t_off.team_player_get_attribute(player, "mid_range") - t_def.team_player_get_attribute(player, "perimeter_defence")) / 500)):
                    self.team_score(t_off, 2)
                    t_off.team_player_score_stat(player, "points", 2)
                    if passer is not None and np.random.random() < 0.65:
                        t_off.team_player_score_stat(passer, "assists")
                elif np.random.random() < 0.01 + (t_def.team_player_get_attribute(player, "blocking") / 1000):
                    t_def.team_player_score_stat(player, "blocks")

            else:  # layup
                self.team_attempt(t_off, 2)
                if np.random.random() > (0.35 - ((t_off.team_player_get_attribute(player, "layups") - t_def.team_player_get_attribute(player, "paint_defence")) / 500)):
                    self.team_score(t_off, 2)
                    t_off.team_player_score_stat(player, "points", 2)
                    if passer is not None and np.random.random() < 0.65:
                        t_off.team_player_score_stat(passer, "assists")
                elif np.random.random() < 0.01 + (t_def.team_player_get_attribute(player, "blocking") / 500):
                    t_def.team_player_score_stat(player, "blocks")

        else:  # 3 point shot
            self.team_attempt(t_off, 3)
            if np.random.random() > (0.65 - ((t_off.team_player_get_attribute(player, "long_range") - t_def.team_player_get_attribute(player, "perimeter_defence")) / 500)):
                self.team_score(t_off, 3)
                t_off.team_player_score_stat(player, "points", 3)
                if passer is not None and np.random.random() < 0.65:
                    t_off.team_player_score_stat(passer, "assists")
            elif np.random.random() < 0.01 + (t_def.team_player_get_attribute(player, "blocking") / 10000):
                t_def.team_player_score_stat(player, "blocks")

    def quarter_sim(self):  # index in the array should describe position as well

        for i in range(20):  # assumption that each team might have 20 possesions in a single quarter

            # TEAM 1 BALL POSSESSION

            player = random.choices([0, 1, 2], [8, 1, 1], k=1)[0]  # playmaking (either pg/sg/sf start with the ball)

            player = self.playmaking(player, self._t1, self._t2)

            player, passer = self.passing(player, self._t1, self._t2)

            self.scoring(player, passer, self._t1, self._t2)

            # TEAM 2 BALL POSSESSION

            player = random.choices([0, 1, 2], [8, 1, 1], k=1)[0]  # playmaking (either pg/sg/sf start with the ball)

            player = self.playmaking(player, self._t2, self._t1)

            player, passer = self.passing(player, self._t2, self._t1)

            self.scoring(player, passer, self._t2, self._t1)

    def field_goal_percentage(self):
        t1_arr = [
            np.round(((self._t1_stats["2pt_made"] + self._t1_stats["3pt_made"]) / (self._t1_stats["2pt_attempt"] + self._t1_stats["3pt_attempt"])), 2) * 100,
            np.round((self._t1_stats["2pt_made"] / self._t1_stats["2pt_attempt"]), 2) * 100,
            np.round((self._t1_stats["3pt_made"] / self._t1_stats["3pt_attempt"]), 2) * 100
        ]

        t2_arr = [
            np.round(((self._t2_stats["2pt_made"] + self._t2_stats["3pt_made"]) / (self._t2_stats["2pt_attempt"] + self._t2_stats["3pt_attempt"])), 2) * 100,
            np.round((self._t2_stats["2pt_made"] / self._t2_stats["2pt_attempt"]), 2) * 100,
            np.round((self._t2_stats["3pt_made"] / self._t2_stats["3pt_attempt"]), 2) * 100
        ]

        return t1_arr, t2_arr

    def show_game_stats(self, quarter):

        t1_arr, t2_arr = self.field_goal_percentage()
        # stats team 1
        fg1, fg2pt1, fg3pt1 = t1_arr[0], t1_arr[1], t1_arr[2]
        # stats team 2
        fg2, fg2pt2, fg3pt2 = t2_arr[0], t2_arr[1], t2_arr[2]

        if quarter == 2:
            print("Halftime stats")
        elif quarter == 4:
            print("End game stats")
        # team 1 stats
        print(self._t1.city, self._t1.name)
        print(f'FG% : {self._t1_stats["2pt_made"] + self._t1_stats["3pt_made"]} / {self._t1_stats["2pt_attempt"] + self._t1_stats["3pt_attempt"]} {fg1} %')
        print(f'2ptFG% {self._t1_stats["2pt_made"] / self._t1_stats["2pt_attempt"]} {fg2pt1} %')
        print(f'3ptFG% {self._t1_stats["3pt_made"]} / {self._t1_stats["3pt_attempt"]}, {fg3pt1}, %')
        # team 2 stats
        print(self._t2.city, self._t2.name)
        print(f'FG% : {self._t2_stats["2pt_made"] + self._t2_stats["3pt_made"]} / {self._t2_stats["2pt_attempt"] + self._t2_stats["3pt_attempt"]} {fg2} %')
        print(f'2ptFG% {self._t2_stats["2pt_made"] / self._t2_stats["2pt_attempt"]} {fg2pt2} %')
        print(f'3ptFG% {self._t2_stats["3pt_made"]} / {self._t2_stats["3pt_attempt"]}, {fg3pt2}, %')

    def compile_teams_game_stats(self):
        fg_t1, fg_t2 = self.field_goal_percentage()
        win_loss_t1 = 'W' if self._t1_stats['score'] > self._t2_stats['score'] else 'L'
        win_loss_t2 = 'W' if self._t2_stats['score'] > self._t1_stats['score'] else 'L'

        stats_labels = ['opponent', 'w/l', 'score', "2pt_made", "2pt_attempt", "3pt_made", "3pt_attempt", 'fg%', '2pt_fg%', '3pt_fg%']

        t1_stats_list = [self._t2.name, win_loss_t1] + [val for val in self._t1_stats.values()] + [item for item in fg_t1] + [self._t2_stats['score']]
        t2_stats_list = [self._t1.name, win_loss_t2] + [val for val in self._t2_stats.values()] + [item for item in fg_t2] + [self._t1_stats['score']]

        t1_stats_dict = {key: val for key, val in zip(stats_labels, t1_stats_list)}
        t2_stats_dict = {key: val for key, val in zip(stats_labels, t2_stats_list)}

        return t1_stats_dict, t2_stats_dict

    def match_sim(self):
        for i in range(1, 5):
            #  print("Quarter :", i)
            self.quarter_sim()
            # self.show_score()
            # if i in [2, 4]:
            #     self.show_game_stats(i)
        ot_counter = 0
        while self._t1_stats["score"] == self._t2_stats["score"]:
            ot_counter += 1
            #  print("OT :", ot_counter)
            self.quarter_sim()
            # self.show_score()

        score = self.return_score()
        # self._t1.team_players_show_game_stats()
        # print("############################################################")
        # self._t2.team_players_show_game_stats()

        t1_stats, t2_stats = self.compile_teams_game_stats()

        self._t1.add_game_to_season_stats(t1_stats)
        self._t2.add_game_to_season_stats(t2_stats)
        self._t1.team_player_add_game_to_season_stats()
        self._t2.team_player_add_game_to_season_stats()

        return score
