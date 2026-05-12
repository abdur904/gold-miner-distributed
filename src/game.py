import random
from server import log_event

# Size of the 2D game map
MAP_SIZE = 20

# Create empty game map
game_map = []

# Fill map with empty cells
for i in range(MAP_SIZE):
    row = []

    for j in range(MAP_SIZE):
        row.append(".")

    game_map.append(row)


# Display the current game map
def display_map(game_map):
    for row in game_map:
        print(" ".join(row))


# Ask the player for their name
player_name = input("Enter your name: ")

print("Welcome", player_name)

# Log player connection on server side
log_event(player_name + " joined the game")

# Player score
score = 0

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

# Control game loop
running = True


# Main gameplay loop
while running:

    # Reset game map every turn
    game_map = []

    # Create fresh empty map
    for i in range(MAP_SIZE):
        row = []

        for j in range(MAP_SIZE):
            row.append(".")

        game_map.append(row)

    # Place all gold objects on map
    for gold in gold_positions:
        game_map[gold[1]][gold[0]] = "G"

    # Place player on map
    game_map[player_y][player_x] = "H"

    # Display player score
    print("Player:", player_name)
    print("Score:", score)

    # Display updated map
    display_map(game_map)

    # Ask player for movement
    move = input("Move (w/a/s/d or q to quit): ")

    # Quit game
    if move == "q":
        log_event(player_name + " exited the game")

        print("Game ended")
        print("Final Score:", score)

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

    # Check gold collection
    for gold in gold_positions:

        if player_x == gold[0] and player_y == gold[1]:

            print("Gold collected")

            # Increase player score
            score += 10

            # Log gold collection
            log_event(player_name + " collected gold")

            # Log score update
            log_event("Score updated for " + player_name)

            print("Score:", score)

            # Remove collected gold
            gold_positions.remove(gold)

            # Generate replacement gold
            new_gold_x = random.randint(0, MAP_SIZE - 1)
            new_gold_y = random.randint(0, MAP_SIZE - 1)

            gold_positions.append((new_gold_x, new_gold_y))

            break