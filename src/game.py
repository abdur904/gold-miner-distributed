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


# Show the game map
display_map(game_map)