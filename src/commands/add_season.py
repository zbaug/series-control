# Own modules
from src.db.storage import autoSave
from src.helpers.utils import printRedText, printVioletText, clear, inputInt, selectSerie

def addSeason(series):
    clear()

    # Select the serie to add seasons to only showing the ones that don't have seasons yet
    serieFound = selectSerie(series, onlyWithoutSeasons=True)

    # If the user choses the < return option > 
    if serieFound is None:
        return

    # SerieName gets the name of the serie
    serieName = serieFound[0] # serieFound = [serieName, {seasonNumber: [ratings]}]

    # Loop to ask the user for the seasons quantity until they input a valid number
    while True:
        seasonsQuantity = inputInt(f"How many seasons do you want to add in {serieName.upper()}: ")

        # In case the user inputs a number less than or equal to 0, show an error message and ask again
        if seasonsQuantity <= 0:
            printRedText("Error: the seasons must be 1 or higher.\n")
            continue

        break

    # Ask the user for the episodes quantity of each season and add it to the serieFound[1] which is the seasons dictionary of the serie
    for seasonNumber in range(1, seasonsQuantity + 1):
        while True:
            episodesQuantity = inputInt(
                f"How many episodes does season {seasonNumber} have?: "
            )

            # In case the user inputs a number less than or equal to 0, show an error message and ask again
            if episodesQuantity <= 0:
                printRedText("Error: the season episodes must be 1 or higher.\n")
                continue

            serieFound[1][seasonNumber] = [None] * episodesQuantity # Create a list with episodesQuantity and fill it with None values to represent the ratings of each episode
            break

    autoSave(series) # Save the series to the file
    printVioletText("Seasons added correctly\n")