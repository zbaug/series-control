# Python modules
from time import sleep
import os
import json
import urllib.request
import urllib.parse

# Depenedencies
from platformdirs import user_data_dir

# Own modules
from src.helpers.utils import inputCyan, printCyanText, printRedText, validateInput, returnToCommandBox, lookingForSerie

# Function to load environment variables from a .env file, checking multiple locations for it.
def _loadEnv():

    # Locations to check for .env, in order of priority
    candidates = [
        os.path.join(os.getcwd(), ".env"),
        os.path.join(user_data_dir("serctl", appauthor=False), ".env"),
        os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
    ]

    # Check each location for .env and load it if found
    for envPath in candidates:
        envPath = os.path.abspath(envPath) # Convert to absolute path for consistency

        # Case path exists, load it and stop searching
        if os.path.exists(envPath):

            # Open the .env file
            with open(envPath) as f:

                # Read each line
                for line in f:
                    line = line.strip() # Remove whitespace and newlines

                    # Only process lines that look like KEY=VALUE and ignore comments
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1) # Split on the first '=' only
                        os.environ[key.strip()] = value.strip() # Set the environment variable
            return


_loadEnv() # Load the .env file at module import, so the API key is available when needed.

# Function to get the OMDB API key from environment variables, with a fallback to reload .env if not found.
def _getApiKey():
    key = os.getenv("OMDB_API_KEY") # Try to get the key from environment variables first (First attempt)

    # Case the key is not found
    if not key:
        _loadEnv()  # Second attempt
        key = os.getenv("OMDB_API_KEY") # Try again after reloading .env, in case it was added or modified since the first load.
    return key

# Function to fetch episode ratings from OMDB API for a given series name. Returns (showName, seasonsDict) or (None, None) if not found.
def fetchOMDBEpisodes(serieName):
    apiKey = _getApiKey() # Get the API key

    # Case the API key is not set
    if not apiKey:
        printRedText("Error: OMDB_API_KEY is not set.\n")
        print(" Run < setkey > in the command box to see more information.\n")
        sleep(1)
        return None, None, "no_key"

    try:
        query = urllib.parse.quote(serieName) # URL-encode the series name to safely include it in the API request
        searchUrl = f"https://www.omdbapi.com/?t={query}&type=series&apikey={apiKey}" # Url to get the series data, including total seasons

        # Make the API request to get the series data
        with urllib.request.urlopen(searchUrl, timeout=8) as response:
            showData = json.loads(response.read().decode()) # Parse the JSON response into a Python dictionary

        # Case the series is not found or there's an error in the response
        if showData.get("Response") == "False":
            return None, None

        showName = showData["Title"] # Get the official title of the show from the API response, which may differ in formatting from the input name.
        totalSeasons = int(showData.get("totalSeasons", 1)) # Get the total number of seasons from the API response, defaulting to 1 if not provided (some shows might not have this field).

        seasonsDict = {} # Dictionary to hold season numbers as keys and lists of episode ratings as values

        # Loop through each season to fetch its episodes and ratings
        for seasonNum in range(1, totalSeasons + 1):
            seasonUrl = f"https://www.omdbapi.com/?t={query}&type=series&Season={seasonNum}&apikey={apiKey}" # Url to get the season data, including episode ratings

            # Make the API request to get the season data
            with urllib.request.urlopen(seasonUrl, timeout=8) as response:
                seasonData = json.loads(response.read().decode()) # Parse the JSON response for the season data

            # Case the season is not found or there's an error in the response, skip to the next season
            if seasonData.get("Response") == "False":
                continue

            episodes = seasonData.get("Episodes", []) # Get the list of episodes for the season, defaulting to an empty list if not provided
            ratings  = []

            # Loop through each episode to extract its IMDb rating
            for ep in episodes:
                rawRating = ep.get("imdbRating", "N/A") # Get the IMDb rating for the episode, defaulting to "N/A" if not provided
                try:
                    ratings.append(float(rawRating)) # Converts the rating to a float and add it to the ratings list for the season
                
                # Case the rating is "N/A" or cannot be converted to a float, append None to indicate a missing rating
                except (ValueError, TypeError):
                    ratings.append(None)

            seasonsDict[seasonNum] = ratings # Add the list of episode ratings to the seasons dictionary under the current season number

        return showName, seasonsDict, None

    except Exception:
        return None, None, None

# # Fetches serie data from the selected source (Own ratings or IMDb) and returns the name, label and seasons
def _getSerieData(series, serieNumber, sourceType):
  
    # Case the source is the user's own ratings, get the serie name and seasons from the local data
    if sourceType == "Own ratings":
        while True:
            serieName = inputCyan(f"Enter the name of serie {serieNumber}: ")

            # Case the user wants to return to the command box
            if returnToCommandBox(serieName):
                return None, None, None

            # Verify the input is valid (not empty and not just whitespace), if not, ask again
            if validateInput(serieName) is None:
                continue

            found = lookingForSerie(series, serieName, 1) # Look for the serie in the local data, allowing for minor typos (max distance of 1)

            # Case the serie is not found or there are no seasons added for it, inform the user and ask again
            if found is None:
                printRedText("Serie not found.\n")
                continue
            
            # Case the serie is found but has no seasons added, inform the user and ask again
            if not found[1]:
                printRedText("This serie has no seasons added.\n")
                continue

            return found[0], "Own", found[1] # Return the serie name, source label and seasons dictionary
    
    # Case the source is OMDB, fetch the serie data from the API
    else: 
        while True:
            serieName = inputCyan(f"Enter the name of serie {serieNumber}: ")

            # Case the user wants to return to the command box
            if returnToCommandBox(serieName):
                return None, None, None

            # Verify the input is valid (not empty and not just whitespace), if not, ask again
            if validateInput(serieName) is None:
                continue

            printCyanText("Searching...")

            showName, seasonsDict, error = fetchOMDBEpisodes(serieName) # Fetch the serie data from the OMDb API

            # Case there was an error fetching the data, handle it accordingly
            if error == "no_key":
                return None, None, None

            # Case the serie is not found, inform the user and ask again
            if showName is None:
                printRedText("Serie not found.\n")
                continue

            return showName, "IMDb", seasonsDict # Return the show name from the API, the source label and the seasons dictionary with episode ratings