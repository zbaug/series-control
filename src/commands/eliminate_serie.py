# Dependencies
from InquirerPy import inquirer

# Own modules
from src.db.storage import autoSave
from src.helpers.utils import clear, printVioletText, selectSerie

def eliminateSerie(series):
    clear()

    # Show all the series
    serieFound = selectSerie(series)

    # Case the user choses the < return option >
    if serieFound is None:
        return

    # SerieName gets the name of the serie
    serieName = serieFound[0]

    # Confirmation to delete the serie
    yesNoChoice = inquirer.select(
        message=f"Are you sure you want to delete '{serieName}'?",
        choices=["Yes", "No"],
        qmark=""
    ).execute()

    if yesNoChoice == "Yes":
        series.remove(serieFound) # Remove the serie from the list of series
        autoSave(series) # Save the series to the file
        printVioletText("Serie deleted correctly\n")