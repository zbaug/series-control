# Python modules
import re

# Own modules
from src.helpers.utils import getRatingColor

# Returns the visible length of a string, ignoring ANSI escape codes
def _visibleLen(text):
    # Remove ANSI escape codes from the string and return the length of the result
    ansiEscape = re.compile(r'\033\[[0-9;]*m')
    return len(ansiEscape.sub('', text))

# Returns the maximum visible width among a list of lines
def _maxVisibleWidth(lines):
    # Return the longest visible line width, or 0 if the list is empty
    return max(_visibleLen(line) for line in lines) if lines else 0

# Pads a line with spaces to reach the target width based on visible length
def _formatRatingCell(rating):
    # Get the colored rating string
    value = getRatingColor(rating)
    # Calculate the visible length of the rating to determine the padding needed
    if rating is None:
        visible_length = 1  # "-" is 1 character
    else:
        visible_length = len(str(round(rating, 2)))
    # Fill the rest of the cell with spaces to keep all cells the same width
    padding = 7 - visible_length
    return value + (" " * padding)

# Builds a list of strings (lines) for a series rating table without printing.
def _buildTableLines(displayName, sourceLabel, seasons):
    lines = []
    seasonNumbers = sorted(seasons.keys())
    # Get the episode count of the season with the most episodes to determine the table height
    maxEpisodes = max(len(seasons[s]) for s in seasonNumbers)

    # Title row with the serie name and source label
    lines.append(f" \033[1;97m{displayName.upper()}\033[0m \033[1;38;5;245m({sourceLabel})\033[0m")

    # Header row with season numbers
    header = "      "
    for s in seasonNumbers:
        header += f"S{s:<6}"
    lines.append(header)

    # Episode rows with ratings
    for ep in range(1, maxEpisodes + 1):
        row = f" E{ep:<3} "
        for s in seasonNumbers:
            if ep <= len(seasons[s]):
                # Add the colored rating cell for this episode
                row += _formatRatingCell(seasons[s][ep - 1])
            else:
                # Season has less episodes than the max, fill with empty space
                row += "       "
        lines.append(row)

    return lines

# Prints a formatted episode ratings table. Used by ser and cs commands.
def _printEpisodesTable(displayName, sourceLabel, seasons):
    seasonNumbers = sorted(seasons.keys())
    # Get the episode count of the season with the most episodes to determine the table height
    maxEpisodes = max(len(seasons[s]) for s in seasonNumbers)

    # Print title row with the serie name and source label
    print(f" \033[1;97m{displayName.upper()}\033[0m \033[1;38;5;245m({sourceLabel})\033[0m")

    # Print header row with season numbers
    header = "      "
    for s in seasonNumbers:
        header += f"S{s:<6}"
    print(header)

    # Print episode rows with ratings
    for ep in range(1, maxEpisodes + 1):
        row = f" E{ep:<3} "
        for s in seasonNumbers:
            if ep <= len(seasons[s]):
                # Add the colored rating cell for this episode
                row += _formatRatingCell(seasons[s][ep - 1])
            else:
                # Season has less episodes than the max, fill with empty space
                row += "       "
        print(row)

    print()