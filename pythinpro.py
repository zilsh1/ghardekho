import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
from collections import defaultdict
from operator import itemgetter

class CricketMatch:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.team1_score = 0
        self.team2_score = 0
        self.team1_players = defaultdict(dict)
        self.team2_players = defaultdict(dict)
        self.man_of_the_match = None

    def update_score(self, team1_score, team2_score):
        self.team1_score += team1_score
        self.team2_score += team2_score

    def add_player_score(self, team, player_name, runs, wickets):
        team_players = self.team1_players if team == self.team1 else self.team2_players
        player_stats = team_players.get(player_name, {"runs": 0, "wickets": 0})
        player_stats["runs"] += runs
        player_stats["wickets"] += wickets
        team_players[player_name] = player_stats

    def get_winner(self):
        if self.team1_score > self.team2_score:
            return self.team1
        elif self.team2_score > self.team1_score:
            return self.team2
        else:
            return "Draw"

def save_matches(matches):
    with open("matches.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        for match_key, match in matches.items():
            writer.writerow([match_key, match.team1, match.team2, match.team1_score, match.team2_score, match.man_of_the_match])

def add_match_score_logic(matches, ipl_teams, treeview, add_window, team1, team2, team1_score, team2_score):
    try:
        team1_score = int(team1_score)
        team2_score = int(team2_score)

        match_key = f"{team1} vs {team2}"
        match = matches.get(match_key, CricketMatch(team1, team2))
        match.update_score(team1_score, team2_score)

        # Additional functionality to add player details
        add_player_details(match, team1, team2)

        matches[match_key] = match

        # Update the treeview with existing matches
        update_treeview(treeview, matches)

        add_window.destroy()
        save_matches(matches)
        messagebox.showinfo("Success", "Score updated!")

    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please enter numeric values.")

def add_player_details(match, team1, team2):
    # Assuming each team has 11 players
    for i in range(1, 12):
        player_name = f"Player{i}"
        runs = int(input(f"Enter runs scored by {player_name} for {team1} in the match: "))
        wickets = int(input(f"Enter wickets taken by {player_name} for {team2} in the match: "))
        match.add_player_score(team1, player_name, runs, 0)  # Update runs for team1
        match.add_player_score(team2, player_name, 0, wickets)  # Update wickets for team2

def display_match_scores(matches):
    display_window = tk.Toplevel()
    display_window.title("Match Scores")

    treeview = ttk.Treeview(display_window, columns=("Team 1", "Score 1", "Team 2", "Score 2", "Winner", "Man of the Match"), show="headings", height=10)
    treeview.heading("Team 1", text="Team 1")
    treeview.heading("Score 1", text="Score 1")
    treeview.heading("Team 2", text="Team 2")
    treeview.heading("Score 2", text="Score 2")
    treeview.heading("Winner", text="Winner")
    treeview.heading("Man of the Match", text="Man of the Match")

    for match_key, match in matches.items():
        winner = match.team1 if match.team1_score > match.team2_score else (match.team2 if match.team2_score > match.team1_score else "Draw")
        treeview.insert("", "end", values=(match.team1, match.team1_score, match.team2, match.team2_score, winner, match.man_of_the_match))

    treeview.grid(row=0, column=0, columnspan=2, pady=10)

def set_man_of_the_match(matches, ipl_teams, treeview, display_window, team1, team2):
    try:
        match_key = f"{team1} vs {team2}"

        if match_key in matches:
            match = matches[match_key]
            man_of_the_match = input("Enter the Man of the Match: ")
            match.man_of_the_match = man_of_the_match

            # Update the treeview with existing matches
            update_treeview(treeview, matches)

            save_matches(matches)
            display_window.destroy()
            messagebox.showinfo("Success", "Man of the Match set successfully.")
        else:
            messagebox.showerror("Error", "No match found for the specified teams.")

    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please enter the Man of the Match.")

def main():
    ipl_teams = [
        "Chennai Super Kings", "Gujarat Titans", "Mumbai Indians", "Kolkata Knight Riders",
        "Royal Challengers Bangalore", "Delhi Capitals", "Lucknow Super Giants", "Punjab Kings",
        "Rajasthan Royals", "Sunrisers Hyderabad"
    ]

    matches = load_matches()

    root = tk.Tk()
    root.title("Cricket Match Tracker")

    treeview = ttk.Treeview(root, columns=("Team 1", "Score 1", "Team 2", "Score 2", "Winner", "Man of the Match"), show="headings", height=10)
    treeview.heading("Team 1", text="Team 1")
    treeview.heading("Score 1", text="Score 1")
    treeview.heading("Team 2", text="Team 2")
    treeview.heading("Score 2", text="Score 2")
    treeview.heading("Winner", text="Winner")
    treeview.heading("Man of the Match", text="Man of the Match")

    update_treeview(treeview, matches)

    treeview.grid(row=0, column=0, columnspan=2, pady=10)

    add_button = ttk.Button(root, text="Add Match Score", command=lambda: add_match_score(matches, ipl_teams, treeview))
    add_button.grid(row=1, column=0, padx=10, pady=10)

    delete_button = ttk.Button(root, text="Delete Match Score", command=lambda: delete_match_score(matches, ipl_teams, treeview))
    delete_button.grid(row=1, column=1, padx=10, pady=10)

    display_button = ttk.Button(root, text="Display Match Scores", command=lambda: display_match_scores(matches))
    display_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Add the buttons for new functionalities
    search_button = ttk.Button(root, text="Search Match Score", command=lambda: search_match_score_gui(matches, ipl_teams))
    search_button.grid(row=4, column=0, padx=10, pady=10)

    stats_button = ttk.Button(root, text="Team Statistics", command=lambda: team_statistics_gui(matches, ipl_teams))
    stats_button.grid(row=4, column=1, padx=10, pady=10)

    leaderboard_button = ttk.Button(root, text="Leaderboard", command=lambda: leaderboard_gui(matches))
    leaderboard_button.grid(row=5, column=0, columnspan=2, pady=10)

    man_of_the_match_button = ttk.Button(root, text="Set Man of the Match", command=lambda: set_man_of_the_match(matches, ipl_teams, treeview, display_window, team1, team2))
    man_of_the_match_button.grid(row=6, column=0, columnspan=2, pady=10)

    exit_button = ttk.Button(root, text="Exit", command=root.destroy)
    exit_button.grid(row=7, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()