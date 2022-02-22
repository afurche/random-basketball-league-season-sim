import tkinter as tk


class Gui:

    @classmethod
    def destroy_items(cls, *args):
        for item in args:
            item.destroy()

    @classmethod
    def popup_window(cls):
        window = tk.Toplevel(bg='white')
        window_width, window_height, x_cordinate, y_cordinate = 400, 100, 350, 200
        window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        label = tk.Label(window, text="Season simulation done!", bg='white')
        label.pack(fill='x', padx=50, pady=5)

        button_close = tk.Button(window, text="Close", bg='white', command=window.destroy)
        button_close.pack(fill='x')

    @classmethod
    def season_sim(cls, season, root, sim_button):
        sim_button.destroy()
        season.season_sim()
        cls.popup_window()

        standings_button = tk.Button(root, text="Show standings", width=30, bg='white', command=lambda: cls.show_standings(season=season, root=root))
        standings_button.pack()

        scores_button = tk.Button(root, text="Show scores", width=30, bg='white', command=lambda: cls.show_scores(season=season, root=root))
        scores_button.pack()

        stat_leaders_button = tk.Button(root, text="Show season stat leaders", bg='white', width=30, command=lambda: cls.show_season_stat_leaders(season=season, root=root))
        stat_leaders_button.pack()

        mvp_button = tk.Button(root, text="Show MVP", bg='white', width=30, command=lambda: cls.show_mvp(season=season, root=root))
        mvp_button.pack()

    @classmethod
    def show_season_stat_leaders(cls, season, root):
        stat_leaders_list = tk.Listbox(root)
        for stat_leader in season.print_season_stat_leaders():
            stat_leaders_list.insert('end', stat_leader)
        stat_leaders_list.pack(fill='both')
        delete_button = tk.Button(root, text="Close", width=10, bg='white', command=lambda: cls.destroy_items(stat_leaders_list, delete_button))
        delete_button.pack()

    @classmethod
    def show_scores(cls, season, root):
        scrollbar = tk.Scrollbar(root)
        scrollbar.pack(side='right', fill='y')
        scores_list = tk.Listbox(root, yscrollcommand=scrollbar.set)
        for game_score in season.scores:
            scores_list.insert('end', game_score)
        scores_list.pack(fill='both')
        scrollbar.config(command=scores_list.yview)
        delete_button = tk.Button(root, text="Close", width=10, bg='white', command=lambda: cls.destroy_items(scores_list, delete_button, scrollbar))
        delete_button.pack()

    @classmethod
    def show_mvp(cls, season, root):
        text_label = tk.Label(root)
        text_label.pack()
        text_label.config(text=season.print_mvp(), bg='white')
        delete_button = tk.Button(root, text="Close", width=10, bg='white', command=lambda: cls.destroy_items(text_label, delete_button))
        delete_button.pack()

    @classmethod
    def get_team_season_stats_avg(cls, season, team_name, root):
        team = season.find_team_by_name(team_name)
        stats_list = tk.Listbox(root)
        for key, val in team.get_team_season_avg_stats().items():
            stats_list.insert('end', f'{key.capitalize()}: {val}')
        stats_list.pack(fill='both')
        return stats_list

    @classmethod
    def get_team_players_season_stats_avg(cls, season, team_name, root):
        team = season.find_team_by_name(team_name)
        stats_list = tk.Listbox(root)
        for player_avg_str in team.get_team_players_season_avg_str():
            stats_list.insert('end', player_avg_str)
        stats_list.pack(fill='both')
        return stats_list

    @classmethod
    def get_team_season_stats_games(cls, season, team_name, root):
        team = season.find_team_by_name(team_name)
        stats_list = tk.Listbox(root)
        for stat in team.get_team_season_game_stats_str():
            stats_list.insert('end', stat)
        stats_list.pack(fill='both')
        return stats_list

    @classmethod
    def show_standings(cls, season, root):
        team_standings_list = tk.Listbox(root)
        for team_standing in season.print_season_team_ranking():
            team_standings_list.insert('end', team_standing)
        team_standings_list.pack(fill='both')
        delete_button = tk.Button(root, text="Close", width=10, bg='white', command=lambda: cls.destroy_items(team_standings_list, delete_button))
        delete_button.pack()

        def get_team_name():
            team_standing = team_standings_list.get('anchor')
            team_city_name = team_standing[:len(team_standing) - 8]
            tmp = ''
            team_name = ''

            for let in team_city_name[::-1]:
                if let != ' ':
                    tmp += let
                else:
                    team_name = tmp[::-1]
                    break

            return team_name

        def get_player_name(stats_list):
            player = stats_list.get('anchor')
            player_name = player[:len(player) - 42]
            player_full_name = ''
            for letter in player:
                player_full_name += player_full_name + letter
            return player_full_name

        def team_not_selected_except_pop_up():
            window = tk.Toplevel(bg='white')
            window_width, window_height, x_cordinate, y_cordinate = 300, 100, 350, 200
            window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
            label = tk.Label(window, text="Please select a team !!!", bg='white')
            label.pack(fill='x', padx=50, pady=5)

            button_close = tk.Button(window, text="Close", bg='white', command=window.destroy)
            button_close.pack(fill='x')

        def show_team_game_stats(team_name, s, r, stats_list, delete_button_stats):
            cls.destroy_items(stats_list, delete_button_stats)
            game_stats_list = cls.get_team_season_stats_games(s, team_name, r)
            delete_button_game_stats = tk.Button(root, text="Close", width=10, bg='white', command=lambda: cls.destroy_items(game_stats_list, delete_button_game_stats))
            delete_button_game_stats.pack()

        def show_team_or_team_players_season_avg_stats(s, r, b1, b2, stats_type):
            team_name = get_team_name()
            try:
                if stats_type == 't':
                    stats_list = cls.get_team_season_stats_avg(s, team_name, r)
                elif stats_type == 'p':
                    stats_list = cls.get_team_players_season_stats_avg(s, team_name, r)
                cls.destroy_items(team_standings_list, delete_button, b1, b2)
                delete_button_stats = tk.Button(root, text="Close", width=10, bg='white', command=lambda: cls.destroy_items(stats_list, delete_button_stats))
                delete_button_stats.pack()
                if stats_type == 't':
                    team_game_stats_button = tk.Button(root, text="Team game stats", width=30, bg='white', command=lambda: show_team_game_stats(team_name, s, r, stats_list, delete_button_stats))
                    team_game_stats_button.pack()
            except AttributeError:
                team_not_selected_except_pop_up()

        team_stats_button = tk.Button(root, text="Team season average stats", width=40, bg='white', command=lambda: show_team_or_team_players_season_avg_stats(season, root, team_stats_button, team_players_stats_button, 't'))
        team_stats_button.pack()
        team_players_stats_button = tk.Button(root, text="Team player season average stats", width=40, bg='white', command=lambda: show_team_or_team_players_season_avg_stats(season, root, team_stats_button, team_players_stats_button, 'p'))
        team_players_stats_button.pack()

    @classmethod
    def show_gui(cls, season):
        root = tk.Tk()
        root.title('Basketball Season Sim')
        root.geometry("1000x400")

        background_image = tk.PhotoImage(file='photos/background_png.png')
        background_label = tk.Label(root, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        label = tk.Label(root, text="Welcome to fantasy league basketball season simulation !", font=45, fg="black", bg='white')
        label.pack(side="top")

        sim_button = tk.Button(root, text="Start sim", width=10, bg='white', command=lambda: cls.season_sim(season=season, root=root, sim_button=sim_button))
        sim_button.pack()

        root.mainloop()
