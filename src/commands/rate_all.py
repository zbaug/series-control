from src.helpers.utils import clear, inputCyan, printRedText, printVioletText, returnToCommandBox, validateInput, selectSerie, _validateRating
from src.db.storage import autoSave

def rateAll(series):
    clear()

    # Show all the series
    serieFound = selectSerie(series)

    # If the user choses the < return option > 
    if serieFound is None:
        return

    # SerieName gets the name of the serie
    serieName = serieFound[0]

    # Get the seasons and episode information of the selected serie
    seasons = serieFound[1]

    # If there are no seasons added to the serie, show a message and return to the command box
    if not seasons:
        printRedText("This serie has no seasons added.")
        return

    # Gets the season numbers and sort them in ascending order
    seasonNumbers = sorted(seasons.keys())

    # Calculate the total number of episodes across all seasons
    totalEpisodes = sum(len(seasons[s]) for s in seasonNumbers)

    print(f"\n You are about to rate {serieName.upper()}")
    print(f" Total seasons: {len(seasonNumbers)} | Total episodes: {totalEpisodes}")
    print(" Type < - > at any rating prompt to finish and save.\n")

    episodesRated = 0 # Counter for the number of episodes rated

    # Loop through each season and episode to get the ratings from the user
    for seasonNumber in seasonNumbers:
        episodes = seasons[seasonNumber] # Get the list of episodes for the current season

        print(f"\n --- SEASON {seasonNumber} ({len(episodes)} episodes) ---\n")

        # Loop through each episode in the current season
        for episodeNumber in range(1, len(episodes) + 1):
            currentRating = episodes[episodeNumber - 1]

            # Case the episode is already rated, show the current rating next to the episode number
            if currentRating is not None:
                currentRatingStr = f" [Current: {currentRating}]"
            else:
                currentRatingStr = ""

            # Input loop for the episode rating
            while True:
                ratingInput = inputCyan(
                    f"S{seasonNumber} E{episodeNumber}{currentRatingStr}: "
                )

                # Case the user wants to return to the command box
                if returnToCommandBox(ratingInput):
                    autoSave(series)
                    printVioletText(f"\n{episodesRated} episode(s) rated successfully\n")
                    return

                # Verify the input is not empty
                if validateInput(ratingInput) is None:
                    continue

                episodeRating = _validateRating(ratingInput) # Validate the rating input and convert it to a float, if the input is invalid it returns None

                # Verify the rating is between 0 and 10
                if episodeRating is None:
                    continue

                break

            episodes[episodeNumber - 1] = episodeRating # Saves the rating in the correct position in the list of episodes
            episodesRated += 1 # Increment the counter for rated episodes

    autoSave(series)
    printVioletText(f"\nAll episodes rated! Total: {episodesRated} episodes\n")