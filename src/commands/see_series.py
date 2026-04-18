from src.helpers.utils import printRedText, printVioletText

def seeSeries(series):

    # Case when there is no series added yet.
    if not series:
        printRedText("There is no series added yet.")
        return

    print(" Press < enter > to exit the section.\n")

    # Loop through the series and display their names, seasons, and episodes.
    for serie in series:
        totalEpisodes = sum(len(episodes) for episodes in serie[1].values()) # Total number of episodes in the series.
        ratedEpisodes = sum(1 for episodes in serie[1].values() for ep in episodes if ep is not None) # Number of episodes that have been rated (not None).

        # Display the series name along with the count of rated episodes and total episodes in the format: "Series Name [ratedEpisodes/totalEpisodes]".
        printVioletText(serie[0].upper() + f" [{ratedEpisodes}/{totalEpisodes}]")   

        # Case when there are no seasons added for the series
        if not serie[1]:
            print("   No seasons added yet.\n")
        else:
            # Loop through the seasons and display the season number along with the count of episodes in that season in the format: "Season X / Episodes Y".
            for season, ratings in serie[1].items():
                print(f"   Season {season} / Episodes {len(ratings)}")
            print()

    input()