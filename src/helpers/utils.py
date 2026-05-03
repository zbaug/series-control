# Dependencies
from InquirerPy import inquirer

# Python modules
import os

#|---------------------------|
#|     GENERAL FUNCTIONS     |
#|---------------------------|

# Color printing and input functions
def printVioletText(text):
    print(f" \033[1;38;2;180;80;255m{text}\033[0m")

def printRedText(text):
    print(f" \033[1;91m{text}\033[0m")

def printCyanText(text):
    print(f" \033[1;96m{text}\033[0m")

def inputCyan(text):
    return input(f" \033[1;96m{text}\033[0m")

# Return to command box function if user inputs "-"
def returnToCommandBox(variableInput):
    if variableInput == "-":
        printRedText("Process finished")
        return True
    return False

# Clwar console function for Windows and Unix-based systems
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# Input validation function for integer numbers
def inputInt(message):
    while True:
        try:
            value = input(f" \033[1;36m{message}\033[0m")
            return int(value)
        except ValueError:
            print(" \033[1;31mInvalid input. Please enter a valid integer number.\033[0m\n")

# Input validation function for non-empty strings
def validateInput(variable):
    if not variable:
        printRedText("Error: The input must not be empty. Please provide a valid value.\n")
        return None
    return variable

# Returns the rating value with color formatting based on the rating scale.
def getRatingColor(rating):
    if rating is None:
        return "-"

    rating = round(rating, 2)

    # Cyan: 9.7 - 10
    if rating >= 9.7:
        return f"\033[1;96m{rating}\033[0m"
    # Dark green: 9 - 9.6
    elif rating >= 9:
        return f"\033[1;38;5;28m{rating}\033[0m"
    # Light green: 8 - 8.9
    elif rating >= 8:
        return f"\033[1;38;5;78m{rating}\033[0m"
    # Yellow: 7 - 7.9
    elif rating >= 7:
        return f"\033[1;93m{rating}\033[0m"
    # Orange: 6 - 6.9
    elif rating >= 6:
        return f"\033[1;33m{rating}\033[0m"
    # Red: 5.1 - 5.9
    elif rating >= 5.1:
        return f"\033[1;91m{rating}\033[0m"
    # Purple: 0 - 5
    else:
        return f"\033[1;35m{rating}\033[0m"

#|---------------------------|
#|     COMMANDS FUNCTIONS    |
#|---------------------------|

# Looks for a serie in the series list by name
def lookingForSerie(series, serieName, value=0):
    for serie in series:
        if serie[0].lower() == serieName.lower():
            return serie

    if value == 1: return None
    printRedText("Serie is not in list.\n")
    return None

# Validates the rating input string and returns a float value if valid, or None with an error message printed.
def _validateRating(ratingInput):
    try:
        episodeRating = float(ratingInput) # Converts rating input to float

        # Case rating has more than 2 decimal places
        if episodeRating != round(episodeRating, 2):
            printRedText("Rating must have a maximum of 2 decimal places.\n")
            return None

        # Case rating is out of range
        if not 0 <= episodeRating <= 10:
            printRedText("Rating must be between 0 and 10.\n")
            return None

        return episodeRating
    
    # Case rating is not a number
    except ValueError:
        printRedText("Rating must be a number.\n")
        return None

RETURN_OPTION = "[ - ] Return to command box" # Option to return to command box in selection lists

# Displays an InquirerPy list of series for the user to select, with an option to return to the command box
def selectSerie(series, onlyWithoutSeasons=False):

    # If onlyWithoutSeasons is True, filter the series list to only include series without seasons. Otherwise, use the full series list.
    if onlyWithoutSeasons:
        available = [s for s in series if not s[1]]
    else:
        available = list(series)

    # If there are no series available to select, print an error message and return None.
    if not available:
        if onlyWithoutSeasons:
            printRedText("There are no series without seasons. Use < ams > to add more seasons to an existing serie.\n")
        else:
            printRedText("There is no series added yet.\n")
        return None

    choices = [s[0] for s in available] + [RETURN_OPTION] # Create a list of series names for the selection choices

    selection = inquirer.select(
        message=f"Select serie [{len(series)}]:",
        choices=choices,
        qmark=""
    ).execute()

    # Case user selects the return option
    if selection == RETURN_OPTION:
        printRedText("Process finished")
        return None

    return lookingForSerie(series, selection, 1) # Look for the selected serie in the original series list and return it.