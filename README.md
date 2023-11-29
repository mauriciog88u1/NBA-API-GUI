# NBA Stats Viewer

This Python application provides an interface to view NBA statistics, including both team and player stats. It utilizes the `tkinter` library for the graphical user interface (GUI) and the `nba_api` library to fetch NBA data.

## Team Stats

### Select Type
- You can choose to view either "Team Stats" or "Player Stats" by selecting the respective radio button.

### Select Team
- Use the dropdown menu to select an NBA team from the list of available teams.

### Enter Season
- Optionally, you can enter an NBA season in the format "YYYY-YY" (e.g., "2021-22"). If left blank, the default season is set to "2021-22".

### Enter Matchup (Optional)
- If you want to filter the data by a specific matchup (e.g., 'LAL @ BOS'), you can enter it in this field.

### Fetch Data
- Click the "Fetch Data" button to retrieve and display the team's game log data based on your selections.

### Save as CSV
- After fetching the data, you have the option to save it as a CSV file by clicking the "Save as CSV" button.

## Player Stats

### Select Player(s)
- In the "Select Player(s)" section, you can choose one or more players from the list. You can select multiple players by holding down the Ctrl key while clicking.

### Fetch Data
- Clicking the "Fetch Data" button will retrieve and display the selected player(s)' game log data based on your selections.

### Save as CSV
- Just like in the team stats section, you can save the player(s)' data as a CSV file by clicking the "Save as CSV" button.

## Output
- The fetched data will be displayed in a text box below the buttons. For team stats, it will show the game log for the selected team. For player stats, it will display the game log for the selected player(s) along with their names.

Please note that this application relies on the NBA API to fetch data, so ensure that you have the necessary packages installed and an internet connection to use it.

Feel free to explore NBA statistics using this user-friendly GUI!
