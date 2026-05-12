# Size of the 2D game map
MAP_SIZE = 20

# Create empty game map
game_map = []

# Fill the map with empty cells
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

# Starting player position
player_x = 0
player_y = 0

# Gold position
gold_x = 5
gold_y = 5

# Place human player on map
game_map[player_y][player_x] = "H"

# Place gold on map
game_map[gold_y][gold_x] = "G"

# Display map before movement
display_map(game_map)

# Ask player to move
move = input("Move (w/a/s/d): ")

# Remove old player position
game_map[player_y][player_x] = "."

# Move player right
if move == "d":
    player_x += 1

# Move player left
elif move == "a":
    player_x -= 1

# Move player up
elif move == "w":
    player_y -= 1

# Move player down
elif move == "s":
    player_y += 1

# Check gold collection
if player_x == gold_x and player_y == gold_y:
    print("Gold collected")

# Place updated player position
game_map[player_y][player_x] = "H"

print(player_name, "moved", move)

# Display updated map
display_map(game_map)