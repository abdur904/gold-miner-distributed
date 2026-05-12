import random
import os
import time
import bot
from server import log_event

# Size of the 2D game map
MAP_SIZE = 20

# Create empty persistent game map
game_map = []

# Fill map with empty cells
for i in range(MAP_SIZE):

    row = []

    for j in range(MAP_SIZE):
        row.append(".")

    game_map.append(row)


# Clear terminal screen for better game display
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# Display the current game map
def display_map(game_map):

    for row in game_map:
        print(" ".join(row))


# Simulate distributed network lag
def simulate_lag():

    # Generate random lag time
    lag_time = random.uniform(0.1, 0.5)

    # Log lag simulation
    log_event(
        "Simulated network lag: "
        + str(round(lag_time, 2))
        + " seconds"
    )

    # Pause execution temporarily
    time.sleep(lag_time)


# Ask the player for their name
player_name = input("Enter your name: ")

print("Welcome", player_name)

# Log player connection on server side
log_event(player_name + " joined the game")

# Log bot connection on server side
log_event(bot.bot_name + " connected")

# Player score
score = 0

# Bot score
bot_score = 0

# Starting player position
player_x = 0
player_y = 0

# Store multiple gold positions
gold_positions = []

# Generate 3 random gold objects
for i in range(3):

    gold_x = random.randint(0, MAP_SIZE - 1)
    gold_y = random.randint(0, MAP_SIZE - 1)

    gold_positions.append((gold_x, gold_y))

# Place initial gold objects
for gold in gold_positions:
    game_map[gold[1]][gold[0]] = "G"

# Place initial bot position
game_map[bot.bot_y][bot.bot_x] = "B"

# Place initial player position
game_map[player_y][player_x] = "H"

# Control game loop
running = True


# Main gameplay loop
while running:

    # Clear terminal before displaying new game state
    clear_screen()

    # Display player and bot scores
    print("Player:", player_name)
    print("Player Score:", score)
    print("Bot Score:", bot_score)

    # Display updated map
    display_map(game_map)

    # Ask player for movement
    move = input("Move (w/a/s/d or q to quit): ")

    # Simulate distributed lag after movement input
    simulate_lag()

    # Remove old player position
    game_map[player_y][player_x] = "."

    # Remove old bot position before moving the bot
    game_map[bot.bot_y][bot.bot_x] = "."

    # Quit game
    if move == "q":

        log_event(player_name + " exited the game")

        print("Game ended")
        print("Final Player Score:", score)
        print("Final Bot Score:", bot_score)

        running = False

    # Move player right
    elif move == "d":

        player_x += 1

        log_event(player_name + " moved RIGHT")

    # Move player left
    elif move == "a":

        player_x -= 1

        log_event(player_name + " moved LEFT")

    # Move player up
    elif move == "w":

        player_y -= 1

        log_event(player_name + " moved UP")

    # Move player down
    elif move == "s":

        player_y += 1

        log_event(player_name + " moved DOWN")

    # Handle invalid movement input
    else:

        print("Invalid input. Use w, a, s, d or q.")

        log_event(player_name + " entered invalid input")

    # Prevent player from moving outside the game map
    if player_x < 0:
        player_x = 0

    elif player_x >= MAP_SIZE:
        player_x = MAP_SIZE - 1

    if player_y < 0:
        player_y = 0

    elif player_y >= MAP_SIZE:
        player_y = MAP_SIZE - 1

    # Move bot automatically once per turn
    bot.move_bot()

    # Place updated bot position
    game_map[bot.bot_y][bot.bot_x] = "B"

    # Place updated player position
    game_map[player_y][player_x] = "H"

    # Check player gold collection
    for gold in gold_positions:

        if player_x == gold[0] and player_y == gold[1]:

            print("Gold collected")

            # Increase player score
            score += 10

            # Log gold collection
            log_event(player_name + " collected gold")

            # Log score update
            log_event("Score updated for " + player_name)

            print("Player Score:", score)

            # Remove collected gold
            gold_positions.remove(gold)

            # Generate replacement gold
            new_gold_x = random.randint(0, MAP_SIZE - 1)
            new_gold_y = random.randint(0, MAP_SIZE - 1)

            gold_positions.append((new_gold_x, new_gold_y))

            # Add new gold to map
            game_map[new_gold_y][new_gold_x] = "G"

            break

    # Check bot gold collection
    for gold in gold_positions:

        if bot.bot_x == gold[0] and bot.bot_y == gold[1]:

            print("Bot collected gold")

            # Increase bot score
            bot_score += 10

            # Log bot gold collection
            log_event(bot.bot_name + " collected gold")

            # Log bot score update
            log_event("Score updated for " + bot.bot_name)

            print("Bot Score:", bot_score)

            # Remove collected gold
            gold_positions.remove(gold)

            # Generate replacement gold
            new_gold_x = random.randint(0, MAP_SIZE - 1)
            new_gold_y = random.randint(0, MAP_SIZE - 1)

            gold_positions.append((new_gold_x, new_gold_y))

            # Add new gold to map
            game_map[new_gold_y][new_gold_x] = "G"

            break

    # Log current game state summary for server-side monitoring
    log_event(
        "State update - "
        + player_name
        + " position=("
        + str(player_x)
        + ","
        + str(player_y)
        + "), "
        + bot.bot_name
        + " position=("
        + str(bot.bot_x)
        + ","
        + str(bot.bot_y)
        + "), Player Score="
        + str(score)
        + ", Bot Score="
        + str(bot_score)
    )

    # Small delay for smoother gameplay
    time.sleep(0.2)