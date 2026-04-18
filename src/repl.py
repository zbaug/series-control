# Python modules
import cmd
from time import sleep

# Own modules
from src.helpers.utils import printRedText, printVioletText, clear
from src.commands import *

# Class to manage the main loop
class SRA(cmd.Cmd):
    prompt = "\033[1;38;5;245m > \033[0m" # Grey
    intro = None

    def __init__(self, series):
        super().__init__()
        self.series = series

    # Wait time and clear the terminal after every command
    def _after_command(self):
        sleep(0.35)
        clear()

    #|----------------------|
    #|       COMMANDS       |
    #|----------------------|

    # Add new serie
    def do_ns(self, _):
        newSerie(self.series)
        self._after_command()

    # Add seasons to a serie
    def do_as(self, _):
        addSeason(self.series)
        self._after_command()

    # Add more seasons to an existing serie
    def do_ams(self, _):
        addMoreSeasons(self.series)
        self._after_command()

    # Eliminate a serie
    def do_es(self, _):
        eliminateSerie(self.series)
        self._after_command()

    # Put ratings to episodes
    def do_prte(self, _):
        putRatingsToEpisodes(self.series)
        self._after_command()

    # See all series
    def do_ss(self, _):
        seeSeries(self.series)
        self._after_command()

    # See episode ratings in table format
    def do_ser(self, _):
        seeEpisodesRatings(self.series)
        self._after_command()

    # Rate all episodes from a serie
    def do_ra(self, _):
        rateAll(self.series)
        self._after_command()

    # Compare episode ratings between two series side by side
    def do_cs(self, _):
        compareSeries(self.series)
        self._after_command()

    # Insert the api key
    def do_setkey(self, _):
        setApiKey()
        self._after_command()

    # Exit the program
    def do_exit(self, _):
        printVioletText("Exiting program. Data saved automatically.")
        return True

    #|----------------------|
    #|        EXTRAS        |
    #|----------------------|

    # Help to show commands
    def do_help(self, _):
        """Show available commands"""
        print("Press < enter > to exit the section.\n")
        print("""\
Commands available:
 < ns >   : Add a new serie
 < as >   : Add seasons to a serie
 < ams >  : Add more seasons to an existing serie
 < es >   : Eliminate a serie
 < prte > : Put ratings to episodes
 < ss >   : See all series
 < ser >  : See episode ratings in table format
 < ra >   : Rate all episodes from a serie
 < cs >   : Compare episode ratings between two series side by side
 < setkey > : Save your OMDb API key for IMDb comparisons
 < exit > : Exit the program
        """)
        input()
        self._after_command()

    # Ctrl + C case
    def cmdloop(self, intro=None):
        try:
            super().cmdloop(intro)
        except KeyboardInterrupt:
            print()
            printVioletText("\nProgram interrupted. Data saved automatically.")

    # Unknown command
    def default(self, line):
        printRedText("Unknown command\n")