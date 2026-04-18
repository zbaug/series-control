# Own modules
from src.repl import SRA
from src.helpers.utils import printVioletText
from src.db.storage import loadSeriesFromJSON

# Logo
LOGO = """                                    
   ▄▄▄▄  ▄▄▄▄▄▄ ▄▄▄▄▄    ▄▄▄ ▄▄▄▄▄▄▄ ▄     
  █▀   ▀ █      █   ▀█ ▄▀   ▀   █    █     
  ▀█▄▄▄  █▄▄▄▄▄ █▄▄▄▄▀ █        █    █     
      ▀█ █      █   ▀▄ █        █    █     
  ▀▄▄▄█▀ █▄▄▄▄▄ █    █  ▀▄▄▄▀   █    █▄▄▄▄▄                     
"""

# Main function
def main():
    series = loadSeriesFromJSON() # Load series from database

    print(LOGO)

    # Initial message
    print("""
 Hello! Welcome to serctl, a series rating program that can be 
 controlled by using the terminal. If you don't know the commands 
 put < help >.
 Also, if you put < - > in the first question in any command case 
 it will take you to the command box.\n
 ────────────────────────────────────────────────────────────────\n""")

    # Confirmation to see if the series are load correctly
    if series:
        printVioletText(f"Loaded {len(series)} series from database.\n")

    # Inicializate main loop
    SRA(series).cmdloop()


if __name__ == "__main__":
    main()