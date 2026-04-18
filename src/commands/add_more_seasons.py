# Own modules
from src.helpers.utils import inputInt, printRedText, printVioletText, clear, selectSerie
from src.db.storage import autoSave

def addMoreSeasons(series):
    clear()

    # Show all the series
    serieFound = selectSerie(series)

    # If the user choses the < return option > 
    if serieFound is None:
        return

    # SerieName gets the name of the serie
    serieName = serieFound[0]

    # existingKeys gets the existing seasons of the serie.
    existingKeys = serieFound[1].keys()

    # startSeason gets the number of the next season to add, if there are no seasons it starts with 1
    startSeason = (max(existingKeys) + 1) if existingKeys else 1

    # currentSeasons gets the number of seasons the serie currently has
    currentSeasons = len(existingKeys)

    while True:
        seasonsQuantityToAdd = inputInt(
            f"There are currently {currentSeasons} seasons in {serieName}, how many more seasons to add? "
        )

        # Case the user enters a number less than or equal to 0
        if seasonsQuantityToAdd <= 0:
            printRedText("Error: the seasons must be 1 or higher.\n")
            continue

        break

    # Loop to ask the user for the episodes quantity of each season
    for seasonNumber in range(startSeason, startSeason + seasonsQuantityToAdd):
        while True:
            episodesQuantity = inputInt(
                f"How many episodes does season {seasonNumber} have?: "
            )

            # Case the user enters a number less than or equal to 0
            if episodesQuantity <= 0:
                printRedText("Error: the season episodes must be 1 or higher.\n")
                continue

            serieFound[1][seasonNumber] = [None] * episodesQuantity # Create a list with episodesQuantity and fill it with None values to represent the ratings of each episode
            break

    autoSave(series) # Save the series to the file
    printVioletText("New seasons added correctly\n")