# Python modules
import os
import json

# Own modules
from platformdirs import user_data_dir
from src.helpers.utils import printRedText

_DATA_DIR = user_data_dir("serctl", appauthor=False) # Path to the user data directory where the JSON file will be stored
JSON_FILE = os.path.join(_DATA_DIR, "series_data.json") # Full path to the JSON file

# Load series data from JSON file and returns the loaded series list or an empty list if file doesn't exist.
def loadSeriesFromJSON():

    # Case when the JSON file doesn't exist, return an empty list to start with an empty database.
    if not os.path.exists(JSON_FILE):
        return []

    try:

        # Open the JSON file and load the data
        with open(JSON_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file) # Load the JSON data into a Python object (list of series)

            loaded_series = [] # List to store the loaded series data in the correct format

            # Iterate through each serie in the loaded data and convert season keys to integers
            for serie in data:
                serie_name = serie[0] # Get the serie name from the loaded data
                seasons_dict = {} # Dictionary to store seasons with integer keys

                # Iterate through each season in the serie and convert the season key to an integer
                for season_key, episodes in serie[1].items():
                    try:
                        seasons_dict[int(season_key)] = episodes # Convert the season key to an integer and store it in the seasons_dict
                    
                    # Error case
                    except ValueError:
                        printRedText(f"Warning: Invalid season key '{season_key}' in serie '{serie_name}'. Skipping.")
                        continue

                loaded_series.append([serie_name, seasons_dict]) # Append the serie info with the converted seasons_dict to the loaded_series list

            return loaded_series
        
    # Error cases
    except json.JSONDecodeError:
        printRedText("Error: JSON file is corrupted. Starting with empty database.")
        return []
    except Exception as e:
        printRedText(f"Error loading data: {e}")
        return []

# Save current series data to JSON file and creates the data directory if it doesn't exist.
def saveSeriesToJSON(series):
    try:
        os.makedirs(_DATA_DIR, exist_ok=True) # Create the data directory if it doesn't exist

        data_to_save = [] # List to store the series data in the format suitable for JSON serialization (season keys as strings)

        # Iterate through each serie in the series list and convert season keys to strings for JSON serialization
        for serie in series:
            serie_name = serie[0] # Get the serie name from the series data
            seasons_dict = {} # Dictionary to store seasons with string keys for JSON serialization

            # Iterate through each season in the serie and convert the season key to a string for JSON serialization
            for season_num, episodes in serie[1].items():
                seasons_dict[str(season_num)] = episodes

            data_to_save.append([serie_name, seasons_dict]) # Append the serie info with the converted seasons_dict to the data_to_save list

        # Open the JSON file and save the data in a human-readable format with indentation and UTF-8 encoding
        with open(JSON_FILE, 'w', encoding='utf-8') as file:
            json.dump(data_to_save, file, indent=4, ensure_ascii=False)

        return True
    
    # Error case
    except Exception as e:
        printRedText(f"Error saving data: {e}")
        return False

# Automatically save data after operations and shows a subtle message if save fails.
def autoSave(series):
    if not saveSeriesToJSON(series):
        printRedText("Warning: Failed to save data to file.")