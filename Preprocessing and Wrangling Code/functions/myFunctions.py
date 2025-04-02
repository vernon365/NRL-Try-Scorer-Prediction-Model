import pandas as pd
import os
import numpy as np
import logging
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd


def plot_tries_comparison(df_with_nulls, df_without_nulls, player_col, tries_col, title_with_nulls, title_without_nulls):
    # Ensure the DataFrames are not None
    if df_with_nulls is None or df_without_nulls is None:
        raise ValueError("DataFrames cannot be None")

    # Ensure the specified columns exist in both DataFrames
    for df in [df_with_nulls, df_without_nulls]:
        if player_col not in df.columns or tries_col not in df.columns:
            raise ValueError(f"Columns {player_col} and {tries_col} must be present in the DataFrames")

    # Define a helper function for plotting
    def plot_tries(ax, df, player_col, tries_col, title):
        player_names = df[player_col].tolist()
        tries = df[tries_col].tolist()
        player_indices = list(range(1, len(player_names) + 1))

        ax.plot(player_indices, tries, marker='o', linestyle='-', color='skyblue')
        ax.set_xlabel('Player Number')
        ax.set_ylabel('Number of Tries')
        ax.set_title(title)
        ax.set_xticks(player_indices)
        ax.grid(True)

        # Optionally, annotate the players for clarity
        for i, txt in enumerate(tries):
            if pd.notna(txt):  # Only annotate non-null values
                ax.annotate(int(txt), (player_indices[i], tries[i]), textcoords="offset points", xytext=(0,5), ha='center')

    # Create subplots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))

    # Plot with null values
    plot_tries(axes[0], df_with_nulls, player_col, tries_col, title_with_nulls)

    # Plot without null values
    plot_tries(axes[1], df_without_nulls, player_col, tries_col, title_without_nulls)

    plt.tight_layout()
    plt.show()



def add_positions(df):
    positions = [
        "Fullback",
        "Winger",
        "Right Centre",
        "Left Centre",
        "Winger",
        "Five-Eighth",
        "Halfback",
        "Prop",
        "Hooker",
        "Prop",
        "Second Row",
        "Second Row",
        "Lock Forward"
    ]
    num_players = len(df)
    if num_players < len(positions):
        positions = positions[:num_players]  # Adjust positions list based on the number of players
    df['Position'] = positions + [''] * (len(df) - len(positions))  # Fill remaining rows with empty strings
    return df


def add_previous_round_tries(table1, table2):
    # Rename the 'Tries' column in table2 to 'Previous_Tries'
    table2 = table2.rename(columns={'Tries': 'Prev_Round_Tries'})
    table2 = table2.rename(columns={'MinsPlayed': 'Prev_Round_MinsPlayed'})
    table2 = table2.rename(columns={'All RunMetres': 'Prev_Round_All_RunMeters'})
    
    # Select only the 'Player' and 'Previous_Tries' columns from table2
    table2 = table2[['Player', 'Prev_Round_Tries', 'Prev_Round_MinsPlayed', 'Prev_Round_All_RunMeters']]
    
    # Merge the tables on the 'Player' column
    merged_table = pd.merge(table1, table2, on='Player', how='left')
    
    return merged_table

def subset_dataframe(df, columns):
    """
    Returns a subset of the DataFrame with the specified columns.

    Parameters:
    df (pd.DataFrame): The original DataFrame.
    columns (list): The list of columns to subset.

    Returns:
    pd.DataFrame: A DataFrame containing only the specified columns.
    """
    return df[columns]

def get_subset_of_columns(csv_file_path, column_names):
    """
    Returns a subset of the CSV data with only the specified columns.

    Parameters:
    csv_file_path (str): The path to the CSV file.
    column_names (list): The list of column names to include in the subset.

    Returns:
    pd.DataFrame: A DataFrame containing only the specified columns.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        
        # Check if all specified columns exist in the DataFrame
        missing_columns = [col for col in column_names if col not in df.columns]
        if missing_columns:
            raise ValueError(f"These columns are not in the CSV file: {missing_columns}")
        
        # Get the subset with the specified columns
        subset_df = df[column_names]
        
        return subset_df
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at path {csv_file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError(f"The file at path {csv_file_path} is empty.")
    except Exception as e:
        raise e



def filter_folders(file_list):
    folder_list = [item for item in file_list if os.path.isdir(item) or (not '.' in item)]
    return folder_list


def get_first_sample(csv_file_path, column_names):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Extract the first sample of the specified column names
    first_sample = df[column_names].iloc[0]
    
    # Convert the sample to a list
    first_sample_list = first_sample.tolist()
    
    return first_sample_list

def is_column_present(csv_file_path, column_name):
    try:
        df = pd.read_csv(csv_file_path)
        if column_name in df.columns:
            print(f"{column_name} column is present") 
        return column_name in df.columns
    
    except FileNotFoundError:
        print("Error: File not found.")
        return False
    except Exception as e:
        print("An error occurred:", e)
        return False

#-----------check empty columns-------------------------



def get_first_13_rows(csv_file_path):
    df = pd.read_csv(csv_file_path)
    first_13_rows = df.head(13)
    return first_13_rows


def get_last_13_rows(csv_file_path):
    df = pd.read_csv(csv_file_path)
    last_13_rows = df.tail(13)
    return last_13_rows


def left_merge_df(team_list_df, player_stats_df, stats_columns):
    # Check if 'Player' column exists in both DataFrames
    if 'Player' not in team_list_df.columns or 'Player' not in player_stats_df.columns:
        raise ValueError("Both DataFrames must have a 'Player' column.")
    
    # Merge DataFrames on 'Player' column
    merged_df = pd.merge(team_list_df, player_stats_df[['Player'] + stats_columns], on='Player', how='left')
    
    return merged_df  # Return the joined DataFrame


def sum_int_column(csv_file_path, column_name):
    try:
        df = pd.read_csv(csv_file_path)
        column_sum = df[column_name].sum()
        return column_sum
    except KeyError:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame. File path: {csv_file_path}")
    except TypeError:
        raise ValueError(f"Column '{column_name}' is not of integer type.")



def add_uniform_column(existing_df, column_name, uniform_value):
    existing_df[column_name] = uniform_value
    return existing_df

def concat_dfs(table1, table2):
    # Concatenate the two tables
    concatenated_table = pd.concat([table1, table2], ignore_index=True)
    
    return concatenated_table


def concat_dfs_list(df_list):
    # Concatenate the list of DataFrames
    concatenated_table = pd.concat(df_list, ignore_index=True)
    
    return concatenated_table



def sort_folders_by_round(folders):
    # Define a function to extract the round number from the folder name
    def extract_round_number(folder_name):
        try:
            return int(folder_name.split("_")[1])
        except IndexError:
            return float('inf')  # If folder name doesn't match the format, place it at the end
    
    # Filter out only the folders
    folders = [folder for folder in folders if folder.startswith("Round_")]
    
    # Sort the folders based on the round number extracted from the folder name
    sorted_folders = sorted(folders, key=extract_round_number)
    return sorted_folders




