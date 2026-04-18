# Dependencies
from InquirerPy import inquirer

# Own modules
from src.db.storage import autoSave
from src.helpers.utils import inputCyan, printRedText, printVioletText, clear, validateInput, returnToCommandBox, lookingForSerie

def newSerie(series):
    clear()

    while True:
        serieName = inputCyan("Enter the name for the serie: ")

        # If user put < - > in input 
        if returnToCommandBox(serieName):
            return

        # Verify that the user don t put an empty string or only spaces
        if validateInput(serieName) is None: continue

        # Verify that the serie is not already added
        if lookingForSerie(series, serieName, 1) is not None:
            printRedText("Error: This serie is already added.\n")
            continue
        
        # Ask the user if he is sure to add the serie
        yesNoChoice = inquirer.select(
            message=f" Are you sure you want to add '{serieName}'?",
            choices=["Yes", "No"],
            qmark=""
        ).execute()

        if yesNoChoice == "Yes":
            break
        else:
            return # Return to the command box

    series.append([serieName, {}]) # Add the serie to the list of series
    autoSave(series) # Save the series to the file
    printVioletText("Serie added correctly\n")