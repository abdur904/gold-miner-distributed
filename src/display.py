import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def display_map(game_map):
    for row in game_map:
        print(" ".join(row))


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