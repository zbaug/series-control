# Dependencies
from InquirerPy import inquirer

# Own modules
from src.helpers.utils import clear, inputCyan, printVioletText, returnToCommandBox, selectSerie, _validateRating
from src.db.storage import autoSave

def putRatingsToEpisodes(series):
    clear()

    # Show all the series
    serieFound = selectSerie(series)

    # Case the user choses the < return option >
    if serieFound is None:
        return

    # SerieName gets the name of the serie
    serieName = serieFound[0]

    # Get the seasons and episode information of the selected serie
    seasons = serieFound[1]

    # Gets the season numbers and sort them in ascending order
    seasonNumbers = sorted(seasons.keys())

    seasonChoice = inquirer.select(
        message=f"Select season [{len(seasonNumbers)}]:",
        choices=["S" + str(s) for s in seasonNumbers], # Prints Season + season number for each season  
        qmark=""
    ).execute()

    # seasonNumber gets the number of the season selected by the user, removing the "S" at the beginning of the string
    seasonNumber = int(seasonChoice[1:])

    # episodes gets the list of episodes of the selected season
    episodes = seasons[seasonNumber]

    episodeChoice = inquirer.select(
        message=f"Episode ({len(episodes)} episodes available):",
        # Prints E + episode number for each episode, and if the episode is already rated it adds (rated) at the end of the string
        choices = [
            "E" + str(e) + (" (rated)" if episodes[e - 1] is not None else "")
            for e in range(1, len(episodes) + 1)
        ],
        qmark=""
    ).execute()

    # episodeToRate gets the number of the episode selected by the user, removing the "E" at the beginning of the string
    episodeToRate = int(episodeChoice[1:].split()[0])

    print(f" The season {seasonNumber} of {serieName} has {len(episodes)} episodes.\n")

    while True:
        ratingInput = inputCyan(
            f"{serieName.upper()} - S{seasonNumber} E{episodeToRate}: " # SerieName - Season number - Episode number
        )

        # Case the user wants to return to the command box
        if returnToCommandBox(ratingInput):
            return

        episodeRating = _validateRating(ratingInput) # Validate the rating input and convert it to a float, if the input is invalid it returns None

        # Case the user enters an invalid rating
        if episodeRating is None:
            continue

        break

    # Saves the episode rating in the series data structure.
    serieFound[1][seasonNumber][episodeToRate - 1] = episodeRating
    autoSave(series) # Save the series to the file
    printVioletText("Episode rated successfully\n")