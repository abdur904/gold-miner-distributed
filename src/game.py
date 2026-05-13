import random
import time
import bot

from server import log_event
from network import send_message, get_sent_message_count
from display import clear_screen, display_map, display_players
from faults import (
    simulate_lag,
    simulate_lost_message,
    simulate_reconnect
)

# Size of game map
MAP_SIZE = 20


# Create empty game map
def create_map():

    return [
        ["." for _ in range(MAP_SIZE)]
        for _ in range(MAP_SIZE)
    ]


# Generate random gold position
def create_gold():

    return (
        random.randint(0, MAP_SIZE - 1),
        random.randint(0, MAP_SIZE - 1)
    )


# Redraw all game objects
def redraw_map(
    game_map,
    gold_positions,
    player_x,
    player_y
):

    # Clear map
    for y in range(MAP_SIZE):

        for x in range(MAP_SIZE):
            game_map[y][x] = "."

    # Draw gold
    for gold in gold_positions:
        game_map[gold[1]][gold[0]] = "G"

    # Draw bot
    game_map[bot.bot_y][bot.bot_x] = "B"

    # Draw player
    game_map[player_y][player_x] = "H"


# Ask player name
player_name = input("Enter your name: ")

print("Welcome", player_name)

# Store connected players
players = [
    {
        "name": player_name,
        "x": 0,
        "y": 0,
        "score": 0
    }
]

# Log player connection
log_event(player_name + " joined the game")
send_message(player_name + " joined the game")

# Log bot connection
log_event(bot.bot_name + " connected")
send_message(bot.bot_name + " connected")

# Create game map
game_map = create_map()

# Create gold positions
gold_positions = [
    create_gold()
    for _ in range(3)
]

# Starting player position
player_x = 0
player_y = 0

# Store player score
score = 0

# Store bot score
bot_score = 0

# Track total player movements
player_moves = 0

# Track collected gold
gold_collected = 0

# Control gameplay loop
running = True

# Main gameplay loop
while running:

    # Redraw map every turn
    redraw_map(
        game_map,
        gold_positions,
        player_x,
        player_y
    )

    # Clear terminal screen
    clear_screen()

    # Display connected player count
    print("Connected Players:", len(players))

    # Display multiplayer information
    display_players(players)

    # Display player statistics
    print("\nPlayer:", player_name)
    print("Player Score:", score)
    print("Bot Score:", bot_score)

    print(
        "Messages Sent:",
        get_sent_message_count()
    )

    # Display updated map
    display_map(game_map)

    # Ask player for movement
    move = input(
        "Move (w/a/s/d or q to quit): "
    )

    # Simulate network lag
    simulate_lag(player_name)

    # Simulate lost distributed message
    if simulate_lost_message(player_name):

        print("Movement message lost.")

        # Simulate reconnect recovery
        simulate_reconnect(player_name)

        continue

    # Quit game
    if move == "q":

        log_event(player_name + " exited the game")

        print("Game ended")

        print("Final Player Score:", score)
        print("Final Bot Score:", bot_score)

        print("Total Moves:", player_moves)
        print("Gold Collected:", gold_collected)

        running = False

    # Move player up
    elif move == "w":

        player_y -= 1
        player_moves += 1

    # Move player down
    elif move == "s":

        player_y += 1
        player_moves += 1

    # Move player left
    elif move == "a":

        player_x -= 1
        player_moves += 1

    # Move player right
    elif move == "d":

        player_x += 1
        player_moves += 1

    # Invalid movement input
    else:

        print("Invalid input.")

        continue

    # Prevent movement outside map
    player_x = max(
        0,
        min(player_x, MAP_SIZE - 1)
    )

    player_y = max(
        0,
        min(player_y, MAP_SIZE - 1)
    )

    # Update multiplayer player information
    players[0]["x"] = player_x
    players[0]["y"] = player_y
    players[0]["score"] = score

    # Move bot automatically
    bot.move_bot(gold_positions)

    # Check player gold collection
    for gold in gold_positions:

        if (
            player_x == gold[0]
            and player_y == gold[1]
        ):

            # Increase player score
            score += 10

            # Increase collected gold counter
            gold_collected += 1

            # Update multiplayer score
            players[0]["score"] = score

            # Log gold collection
            log_event(
                player_name
                + " collected gold"
            )

            # Remove collected gold
            gold_positions.remove(gold)

            # Create replacement gold
            gold_positions.append(create_gold())

            break

    # Check bot gold collection
    for gold in gold_positions:

        if (
            bot.bot_x == gold[0]
            and bot.bot_y == gold[1]
        ):

            # Increase bot score
            bot_score += 10

            # Log bot gold collection
            log_event(
                bot.bot_name
                + " collected gold"
            )

            # Remove collected gold
            gold_positions.remove(gold)

            # Create replacement gold
            gold_positions.append(create_gold())

            break

    # Log game state update
    log_event(
        "State update - "
        + player_name
        + " position=("
        + str(player_x)
        + ","
        + str(player_y)
        + ")"
    )

    # Small gameplay delay
    time.sleep(0.2)