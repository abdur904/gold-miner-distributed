import os


# Clear terminal screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# Display the game map with borders
def display_map(game_map):

    # Create top border
    border = "+" + "--" * len(game_map[0]) + "+"

    print(border)

    for row in game_map:

        # Display row with side borders
        print("|" + " ".join(row) + "|")

    # Create bottom border
    print(border)


# Display connected player information
def display_players(players):

    print("\nConnected Player Information")

    for player in players:

        print(
            "Name:",
            player["name"],
            "| Position:",
            "(" + str(player["x"]) + "," + str(player["y"]) + ")",
            "| Score:",
            player["score"]
        )