import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import commonteamroster, teamgamelog, playergamelog


def get_player_name_by_id(player_id):
    try:
        player = players.find_player_by_id(player_id)
        return player[3]
    except Exception as e:
        print(f"Error getting player name: {e}")
        return "player name not found"

# Function to get team ID by team name
def get_team_id(team_name):
    nba_teams = teams.get_teams()
    team = [team for team in nba_teams if team['full_name'].lower() == team_name.lower()]
    return team[0]['id'] if team else None


def update_player_listbox(event):  # Accept the event argument
    team_name = combo_team.get()
    team_id = get_team_id(team_name)
    if team_id:
        try:
            roster = commonteamroster.CommonTeamRoster(team_id).get_data_frames()[0]
            player_names = roster['PLAYER'].tolist()
            listbox_players.delete(0, tk.END)
            for name in player_names:
                listbox_players.insert(tk.END, name)
        except Exception as e:
            print(f"Error updating player listbox: {e}")
    else:
        listbox_players.delete(0, tk.END)

def select_all_players():
    listbox_players.select_set(0, tk.END)

def display_stats():
    global data_df
    try:
        if var_choice.get() == 'Team Stats':
                # allow user to enter season and matchup (optional) also allow user to select team from dropdown if no season or matchup entered show all games for team
            team_name = combo_team.get()
            team_id = get_team_id(team_name)
            season = entry_season.get()
            matchup = entry_matchup.get()
            if not team_id:
                return
            if not season:
                season = '2021-22'
                data_df = teamgamelog.TeamGameLog(team_id=team_id, season=season, season_type_all_star='Regular Season').get_data_frames()[0]
                data_df['TEAM_NAME'] = team_name
                data_df['PLAYER_NAME'] = data_df['TEAM_NAME'].apply(lambda x: get_player_name_by_id(x))
            if matchup:
                team_games = teamgamelog.TeamGameLog(team_id=team_id, season=season, season_type_all_star='Regular Season', date_from_nullable=matchup).get_data_frames()[0]
                data_df = team_games
                data_df['TEAM_NAME'] = team_name
                data_df['PLAYER_NAME'] = data_df['TEAM_NAME'].apply(lambda x: get_player_name_by_id(x))
            else:
                team_games = teamgamelog.TeamGameLog(team_id=team_id, season=season, season_type_all_star='Regular Season').get_data_frames()[0]
                data_df = team_games
                data_df['TEAM_NAME'] = team_name
                data_df['PLAYER_NAME'] = data_df['TEAM_NAME'].apply(lambda x: get_player_name_by_id(x))
            text_output.delete('1.0', tk.END)
            text_output.insert(tk.END, team_games.to_string())

        elif var_choice.get() == 'Player Stats':
    #        show player stats for selected players only allow user to select players from listbox if no players selected show all players for team also allow user to enter season and matchup (optional) if no season or matchup entered show all games for team also allow user to select plaeer stats for all previous teams
            player_name = listbox_players.get(tk.ACTIVE)
            player_id = players.find_players_by_full_name(player_name)[0]['id']
            print(player_id)
            season = entry_season.get()
            matchup = entry_matchup.get()
            if not player_id:
                return
            if not season:
                season = '2021-22'
                data_df = playergamelog.PlayerGameLog(player_id=player_id, season=season, season_type_all_star='Regular Season').get_data_frames()[0]
                data_df['PLAYER_NAME'] = player_name
            if matchup:
                player_games = playergamelog.PlayerGameLog(player_id=player_id, season=season, season_type_all_star='Regular Season', date_from_nullable=matchup).get_data_frames()[0]
                data_df = player_games
                data_df['PLAYER_NAME'] = player_name
            else:
                player_games = playergamelog.PlayerGameLog(player_id=player_id, season=season, season_type_all_star='Regular Season').get_data_frames()[0]
                data_df = player_games
                data_df['PLAYER_NAME'] = player_name
            text_output.delete('1.0', tk.END)
            text_output.insert(tk.END, player_games.to_string())
            text_output.insert(tk.END, f"\nPlayer Name: {player_name}\n")
    except Exception as e:
        text_output.delete('1.0', tk.END)
        text_output.insert(tk.END, f"Error fetching data: {e}\n")

# Function to save data as CSV
def save_as_csv():
    if 'data_df' in globals():
        file_path = filedialog.asksaveasfilename(defaultextension='.csv',
                                                 filetypes=[("CSV files", '*.csv')])
        if file_path:
            data_df.to_csv(file_path, index=False)
            print(f"Data saved to {file_path}")
    else:
        print("No data to save.")

root = tk.Tk()
root.title("NBA Stats Viewer")

var_choice = tk.StringVar(value="Team Stats")

# Widgets
label_choice = ttk.Label(root, text="Select Type:")
radio_team = ttk.Radiobutton(root, text="Team Stats", variable=var_choice, value="Team Stats")
radio_player = ttk.Radiobutton(root, text="Player Stats", variable=var_choice, value="Player Stats")

label_team = ttk.Label(root, text="Select Team:")
combo_team = ttk.Combobox(root, values=[team['full_name'] for team in teams.get_teams()])
combo_team.bind('<<ComboboxSelected>>', update_player_listbox)

label_season = ttk.Label(root, text="Enter Season (e.g., 2021-22):")
entry_season = tk.Entry(root)

label_matchup = ttk.Label(root, text="Enter Matchup (optional, e.g., 'LAL @ BOS'):")
entry_matchup = tk.Entry(root)

label_player = ttk.Label(root, text="Select Player(s):")
listbox_players = tk.Listbox(root, selectmode='extended', height=10)
button_select_all = tk.Button(root, text="Select All Players", command=select_all_players)

button_fetch = tk.Button(root, text="Fetch Data", command=display_stats)
button_save = tk.Button(root, text="Save as CSV", command=save_as_csv)

text_output = tk.Text(root, height=20, width=100)

# Layout
label_choice.grid(row=0, column=0, padx=10, pady=5)
radio_team.grid(row=0, column=1, padx=10, pady=5)
radio_player.grid(row=0, column=2, padx=10, pady=5)

label_team.grid(row=1, column=0, padx=10, pady=5)
combo_team.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

label_season.grid(row=2, column=0, padx=10, pady=5)
entry_season.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

label_matchup.grid(row=3, column=0, padx=10, pady=5)
entry_matchup.grid(row=3, column=1, columnspan=2, padx=10, pady=5)

label_player.grid(row=4, column=0, padx=10, pady=5)
listbox_players.grid(row=4, column=1, columnspan=2, sticky="ew", padx=10, pady=5)
button_select_all.grid(row=5, column=1, columnspan=2, padx=10, pady=5)

button_fetch.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
button_save.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

text_output.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

# Run the application
root.mainloop()
