MAP_SIZE = 20

game_map = []

for i in range(MAP_SIZE):
    row = []
    for j in range(MAP_SIZE):
        row.append(".")
    game_map.append(row)

print(game_map)