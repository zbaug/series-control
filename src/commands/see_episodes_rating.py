from src.helpers.utils import printRedText, selectSerie
from src.helpers.table_helpers import _printEpisodesTable

def seeEpisodesRatings(series):

    # Show all the series
    serieFound = selectSerie(series)

    # If the user choses the < return option > 
    if serieFound is None:
        return

    # Get the dictionary of seasons for the selected series in a variable called seasons
    seasons = serieFound[1]

    # Case the serie has no seasons added
    if not seasons:
        printRedText("This serie has no seasons added.")
        return

    print(" Press < enter > to exit the section.\n")
    _printEpisodesTable(serieFound[0], "Own", seasons) # Print the table with the ratings of the episodes of the serie
    input()