import random
import os
import time
import zmq
import bot
from server import log_event

# Create ZeroMQ communication context
context = zmq.Context()

# Create client communication socket
socket = context.socket(zmq.PAIR)

# Connect player to distributed server
socket.connect("tcp://localhost:5555")


# Send message to ZeroMQ server safely
def send_message(message):

    try:
        socket.send_string(message, flags=zmq.NOBLOCK)

    except zmq.Again:
        log_event("ZeroMQ message could not be sent immediately: " + message)


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

    # Send lag event to distributed server
    send_message(
        "Lag simulated for "
        + player_name
        + ": "
        + str(round(lag_time, 2))
        + " seconds"
    )

    # Pause execution temporarily
    time.sleep(lag_time)


# Simulate lost message in distributed communication
def simulate_lost_message():

    # Randomly decide if a message is lost
    message_lost = random.choice([True, False, False])

    # Log simulated message loss
    if message_lost:
        log_event("Simulated lost message detected")

        # Send lost message event to distributed server
        send_message("Lost message simulated for " + player_name)

    return message_lost


# Simulate reconnect recovery after network failure
def simulate_reconnect():

    # Display reconnect message
    print("Reconnecting to distributed server...")

    # Log reconnect attempt
    log_event(player_name + " attempting reconnection")

    # Send reconnect attempt to distributed server
    send_message(player_name + " attempting reconnection")

    # Simulate reconnect delay
    time.sleep(1)

    # Display reconnect success
    print("Reconnection successful")

    # Log reconnect success
    log_event(player_name + " reconnected successfully")

    # Send reconnect success to distributed server
    send_message(player_name + " reconnected successfully")


# Ask the player for their name
player_name = input("Enter your name: ")

print("Welcome", player_name)

# Store connected players
players = []

# Add player information to multiplayer structure
player_data = {
    "name": player_name,
    "x": 0,
    "y": 0,
    "score": 0
}

players.append(player_data)

# Log player connection on server side
log_event(player_name + " joined the game")

# Send player connection to distributed server
send_message(player_name + " joined the game")

# Log bot connection on server side
log_event(bot.bot_name + " connected")

# Send bot connection to distributed server
send_message(bot.bot_name + " connected")

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

    # Display connected player count
    print("Connected Players:", len(players))

    # Display connected multiplayer data
    display_players(players)

    # Display player and bot scores
    print("\nPlayer:", player_name)
    print("Player Score:", score)
    print("Bot Score:", bot_score)

    # Display updated map
    display_map(game_map)

    # Ask player for movement
    move = input("Move (w/a/s/d or q to quit): ")

    # Simulate distributed lag after movement input
    simulate_lag()

    # Simulate lost message after movement input
    if simulate_lost_message():

        print("Movement message lost. Waiting for next update.")

        # Log lost movement update
        log_event(player_name + " movement message was lost")

        # Send lost movement update to distributed server
        send_message(player_name + " movement message was lost")

        # Simulate reconnect recovery
        simulate_reconnect()

        # Skip this turn to represent a lost movement update
        continue

    # Remove old player position
    game_map[player_y][player_x] = "."

    # Remove old bot position before moving the bot
    game_map[bot.bot_y][bot.bot_x] = "."

    # Quit game
    if move == "q":

        # Send exit event to distributed server
        send_message(player_name + " exited the game")

        log_event(player_name + " exited the game")

        print("Game ended")
        print("Final Player Score:", score)
        print("Final Bot Score:", bot_score)

        running = False

    # Move player right
    elif move == "d":

        player_x += 1

        # Send distributed movement update
        send_message(player_name + " moved RIGHT")

        log_event(player_name + " moved RIGHT")

    # Move player left
    elif move == "a":

        player_x -= 1

        # Send distributed movement update
        send_message(player_name + " moved LEFT")

        log_event(player_name + " moved LEFT")

    # Move player up
    elif move == "w":

        player_y -= 1

        # Send distributed movement update
        send_message(player_name + " moved UP")

        log_event(player_name + " moved UP")

    # Move player down
    elif move == "s":

        player_y += 1

        # Send distributed movement update
        send_message(player_name + " moved DOWN")

        log_event(player_name + " moved DOWN")

    # Handle invalid movement input
    else:

        print("Invalid input. Use w, a, s, d or q.")

        log_event(player_name + " entered invalid input")

        # Send invalid input event to distributed server
        send_message(player_name + " entered invalid input")

    # Prevent player from moving outside the game map
    if player_x < 0:
        player_x = 0

    elif player_x >= MAP_SIZE:
        player_x = MAP_SIZE - 1

    if player_y < 0:
        player_y = 0

    elif player_y >= MAP_SIZE:
        player_y = MAP_SIZE - 1

    # Update multiplayer player data
    player_data["x"] = player_x
    player_data["y"] = player_y
    player_data["score"] = score

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

            # Update multiplayer score
            player_data["score"] = score

            # Log gold collection
            log_event(player_name + " collected gold")

            # Send gold collection event to distributed server
            send_message(player_name + " collected gold")

            # Log score update
            log_event("Score updated for " + player_name)

            # Send score update to distributed server
            send_message("Score updated for " + player_name)

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

            # Send bot gold event to distributed server
            send_message(bot.bot_name + " collected gold")

            # Log bot score update
            log_event("Score updated for " + bot.bot_name)

            # Send bot score update to distributed server
            send_message("Score updated for " + bot.bot_name)

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

    # Prepare game state summary
    state_message = (
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

    # Log current game state summary for server-side monitoring
    log_event(state_message)

    # Send state update to distributed server
    send_message(state_message)

    # Small delay for smoother gameplay
    time.sleep(0.2)