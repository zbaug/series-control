# Dependencies
from InquirerPy import inquirer

# Own modules
from src.helpers.utils import clear, printRedText, selectSerie
from src.helpers.ombd_api_helpers import _getSerieData
from src.helpers.table_helpers import _buildTableLines, _maxVisibleWidth, _visibleLen

def compareSeries(series):
    clear()

    sourceChoice1 = inquirer.select(
        message="Select the source for serie 1:",
        choices=["Own ratings", "IMDb", "-"],
        qmark=""
    ).execute()

    # Case the user wants to return to the command box
    if sourceChoice1 == "-":
        return

    if sourceChoice1 == "Own ratings":

        # Case there are no series added yet, show a message and return to the command box
        if not series:
            printRedText("There is no series added yet.\n")
            return
        
        serieFound1 = selectSerie(series) # Show the list of series and let the user select one

        # Case the user choses the < return option > in the serie selection
        if serieFound1 is None:
            return
        
        name1, label1, seasons1 = serieFound1[0], "Own", serieFound1[1] # Unpack serie data into separate variables, label as "Own" to indicate user ratings

    else:
        # Fetch serie data from the selected source (Own ratings or IMDb), if user cancels return
        name1, label1, seasons1 = _getSerieData(series, 1, sourceChoice1)
        if name1 is None:
            return

    sourceChoice2 = inquirer.select(
        message="Select the source for serie 2:",
        choices=["Own ratings", "IMDb"],
        qmark=""
    ).execute()

    if sourceChoice2 == "Own ratings":

        # Case there are no series added yet, show a message and return to the command box
        if not series:
            printRedText("There is no series added yet.\n")
            return
        
        serieFound2 = selectSerie(series) # Show the list of series and let the user select one

        # Case the user choses the < return option > in the serie selection
        if serieFound2 is None:
            return
        
        name2, label2, seasons2 = serieFound2[0], "Own", serieFound2[1] # Unpack serie data into separate variables, label as "Own" to indicate user ratings

    else:
        # Fetch serie data from the selected source (Own ratings or IMDb), if user cancels return
        name2, label2, seasons2 = _getSerieData(series, 2, sourceChoice2)
        if name2 is None:
            return

    clear()
    print(" Press < enter > to exit the section.\n")

    #|-------------------------------|
    #|   SIDE BY SIDE TABLE DISPLAY  |
    #|-------------------------------|

    # Build the table lines for each serie
    leftLines  = _buildTableLines(name1, label1, seasons1)
    rightLines = _buildTableLines(name2, label2, seasons2)

    # Get the width of the left table to align the right table correctly
    leftWidth = _maxVisibleWidth(leftLines)

    # Get the total rows needed based on the serie with more episodes
    maxRows   = max(len(leftLines), len(rightLines))

    for i in range(maxRows):

        # If one serie has less rows than the other, fill with empty string
        leftLine  = leftLines[i]  if i < len(leftLines)  else ""
        rightLine = rightLines[i] if i < len(rightLines) else ""

        # Calculate padding to keep the right table aligned regardless of ANSI color codes
        leftPadding = " " * (leftWidth - _visibleLen(leftLine) + 6)

        # Print both tables side by side
        print(leftLine + leftPadding + rightLine)

    print()
    input()