# Dependencies
from platformdirs import user_data_dir

# Python modules
import os

# Own modules
from src.helpers.utils import inputCyan, printRedText, printVioletText, clear, returnToCommandBox
from src.db.storage import _DATA_DIR

def setApiKey():
    clear()

    # Check if there's already a key saved and warn the user that it will be replaced if they continue
    envPath = os.path.join(user_data_dir("serctl", appauthor=False), ".env")

    # If the .env file exists
    if os.path.exists(envPath):
        existingKey = None # Variable to store the existing key if found

        # Read the .env file to find the existing key
        with open(envPath, "r") as f:
            for line in f:
                if line.startswith("OMDB_API_KEY="):
                    existingKey = line.split("=", 1)[1].strip() # Extract the key value
                    break
        
        # Case if an existing key is found
        if existingKey:
            printRedText("You already have an API key saved. If you continue, it will be replaced.\n")

    print(" This command saves your OMDb API key so IMDb comparisons work.")
    print(" Get a free key at: https://www.omdbapi.com/apikey.aspx\n")
    print(" To use IMDb comparisons you need a free API key from OMDb:")
    print(" 1. Register at https://www.omdbapi.com/apikey.aspx (free tier, should be enough for personal usage)")
    print(" 2. Activate the key from the email they send you\n")

    while True:
        apiKey = inputCyan("Enter your OMDb API key: ")

        # Case the user types - and returns to the command box
        if returnToCommandBox(apiKey):
            return

        # Case the user types an empty key
        if not apiKey.strip():
            printRedText("Error: the key must not be empty.\n")
            continue

        break
    
    # Save the key in a .env file in the user data directory, creating the directory if it doesn't exist
    envPath = os.path.join(user_data_dir("serctl", appauthor=False), ".env")

    # Try to create the directory if it doesn't exist
    try:
        os.makedirs(os.path.dirname(envPath), exist_ok=True)
        lines = []        # List to store the lines of the .env file, either updated or unchanged
        keyUpdated = False  # Flag to check if the key was updated, if not we will add it at the end of the file

        # Case the .env file already exists
        if os.path.exists(envPath):
            with open(envPath, "r") as f:
                for line in f:
                    if line.startswith("OMDB_API_KEY="):
                        lines.append(f"OMDB_API_KEY={apiKey.strip()}\n")  # Update the line with the new key
                        keyUpdated = True
                    else:
                        lines.append(line)  # Keep the rest of the lines unchanged

        # If the key was not found in the file, add it at the end
        if not keyUpdated:
            lines.append(f"OMDB_API_KEY={apiKey.strip()}\n")

        # Write the updated lines back to the .env file
        with open(envPath, "w") as f:
            f.writelines(lines)

        # Apply the key to the current environment without needing to restart
        os.environ["OMDB_API_KEY"] = apiKey.strip()

        printVioletText(f"API key saved correctly in {envPath}\n")

    except Exception as e:
        printRedText(f"Error saving the key: {e}\n")