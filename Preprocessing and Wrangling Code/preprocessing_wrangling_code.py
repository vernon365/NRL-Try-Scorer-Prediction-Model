import os
import pandas as pd
from functions.myFunctions import (
    get_first_13_rows, get_first_sample, filter_folders, subset_dataframe, add_previous_round_tries, plot_tries_comparison,
    get_last_13_rows, concat_dfs_list, sum_int_column, add_uniform_column, sort_folders_by_round, add_positions
)

# Get the current working directory
current_dir = os.getcwd()
print(current_dir)

# Define the directories for raw data and processed data
nrlstats_dir = os.path.join(current_dir, 'NRLSTATS_RAW_DATA')
processed_data_dir = os.path.join(current_dir, 'Cleanned Data')

# Get the list of years available in the raw data directory
years = os.listdir(nrlstats_dir)

# Initialize a list to store the concatenated DataFrames for each game and round
all_concatenated_dfs = []

# Iterate through each year
for year in years:
    year_path = os.path.join(nrlstats_dir, year)
    
    # Check if the path is a directory
    if os.path.isdir(year_path):
        rounds = os.listdir(year_path)
        sorted_rounds = sort_folders_by_round(rounds)[::-1]  # Sort rounds and reverse the order
        
        # Initialize a list to store the DataFrames for each year
        year_stats_list = []

        # Iterate through each round (excluding the last round)
        for current_round_index in range(len(sorted_rounds) - 1):
            current_round_path = os.path.join(year_path, sorted_rounds[current_round_index])
            previous_round_path = os.path.join(year_path, sorted_rounds[current_round_index + 1])
            current_round_games = filter_folders(os.listdir(current_round_path))

            # Iterate through each game in the current round
            for game in current_round_games:
                current_game_path = os.path.join(current_round_path, game)
                sub_directories = filter_folders(os.listdir(current_game_path))

                # Process the 'team_list' sub-directory
                for sub_dir in sub_directories:
                    if sub_dir == 'team_list':
                        team_list_path = os.path.join(current_game_path, sub_dir)
                        team_list_csv_filename = os.listdir(team_list_path)[0]
                        team_list_csv_filepath = os.path.join(team_list_path, team_list_csv_filename)

                        # Get the first 13 rows and last 13 rows of the current team list CSV file
                        home_team_df = add_positions(subset_dataframe(get_first_13_rows(team_list_csv_filepath), ['Home_Team', 'Away_Team', 'Player', 'Tries']))
                        away_team_df = add_positions(subset_dataframe(get_last_13_rows(team_list_csv_filepath), ['Home_Team', 'Away_Team', 'Player', 'Tries']))

                        # Add a column indicating whether the player is a home player
                        add_uniform_column(home_team_df, 'isHomePlayer', 'Yes')
                        add_uniform_column(away_team_df, 'isHomePlayer', 'No')

                        # Get the list of current home and away teams
                        current_teams = get_first_sample(team_list_csv_filepath, ['Home_Team', 'Away_Team'])
                        previous_round_games = filter_folders(os.listdir(previous_round_path))

                        print(current_teams)  # Print the current teams
                        
                        # Initialize a list to store DataFrames for the current game
                        current_game_dfs = []
                        
                        # Iterate through each game in the previous round
                        for prev_game in previous_round_games:
                            previous_game_path = os.path.join(previous_round_path, prev_game)
                            prev_sub_directories = filter_folders(os.listdir(previous_game_path))

                            # Process the 'team_list' sub-directory in the previous round
                            for prev_sub_dir in prev_sub_directories:
                                if prev_sub_dir == 'team_list':
                                    prev_team_list_path = os.path.join(previous_game_path, 'team_list')
                                    prev_team_files = os.listdir(prev_team_list_path)

                                    # Iterate through each file in the 'team_list' directory
                                    for prev_file in prev_team_files:
                                        prev_file_path = os.path.join(prev_team_list_path, prev_file)
                                        prev_teams = get_first_sample(prev_file_path, ['Home_Team', 'Away_Team'])

                                        # Check for matching teams between current and previous rounds
                                        for current_team in current_teams:
                                            if current_team in prev_teams:
                                                print("Found!")  # Print when a match is found

                                                player_stats_path = os.path.join(previous_game_path, 'team_players')
                                                player_stats_files = os.listdir(player_stats_path)

                                                # Determine if the team is home or away and set the appropriate file index and DataFrame
                                                if current_teams[0] == current_team:
                                                    file_index = 1
                                                    team_type = "home"
                                                    team_df = home_team_df
                                                else:
                                                    file_index = 0
                                                    team_type = "away"
                                                    team_df = away_team_df

                                                # Construct the file path for the team stats
                                                player_stats_file_path = os.path.join(player_stats_path, player_stats_files[file_index])
                                                print(f"{current_team} {team_type} team file has played stats > {player_stats_file_path}")

                                                # Read the team stats and add previous round tries
                                                team_stats = pd.read_csv(player_stats_file_path)
                                                new_df = add_previous_round_tries(team_df, team_stats)

                                                # Calculate total tackles and tackle efficiency for the opponent
                                                opponent_file_index = 1 - file_index
                                                opponent_total_tackles = sum_int_column(
                                                    os.path.join(player_stats_path, player_stats_files[opponent_file_index]),
                                                    'TacklesMade'
                                                )
                                                opponent_tackle_efficiency = sum_int_column(
                                                    os.path.join(player_stats_path, player_stats_files[opponent_file_index]),
                                                    'Tackle Efficiency'
                                                )

                                                # Add uniform columns for the opponent's total tackles and tackle efficiency
                                                add_uniform_column(new_df, 'Prev_OpponentTotalTackles', opponent_total_tackles)
                                                add_uniform_column(new_df, 'Prev_OpponentTeamTackleEfficiency', opponent_tackle_efficiency)

                                                # Add the new DataFrame to the list for the current game
                                                current_game_dfs.append(new_df)

                        # Concatenate the DataFrames for the current game and append to the list
                        if current_game_dfs:
                            concatenated_df = concat_dfs_list(current_game_dfs)
                            all_concatenated_dfs.append(concatenated_df)

# Concatenate all the DataFrames for all games and rounds
final_df_with_na = concat_dfs_list(all_concatenated_dfs)

final_df_without_na = final_df_with_na.dropna()
final_df_without_na.to_csv(os.path.join(processed_data_dir, 'processed_data.csv'), index=False)
plot_tries_comparison(final_df_with_na, final_df_without_na, 'Player', 'Tries', 'Player Number of Tries (before cleaning)', 'Player Number of Tries (after cleaning)')