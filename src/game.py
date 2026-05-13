import random
import time
import bot

from server import log_event
from network import send_message, get_sent_message_count
from display import clear_screen, display_map, display_players
from faults import simulate_lag, simulate_lost_message, simulate_reconnect

MAP_SIZE = 20

game_map = []

for i in range(MAP_SIZE):
    row = []

    for j in range(MAP_SIZE):
        row.append(".")

    game_map.append(row)


player_name = input("Enter your name: ")

print("Welcome", player_name)

players = []

player_data = {
    "name": player_name,
    "x": 0,
    "y": 0,
    "score": 0
}

players.append(player_data)

log_event(player_name + " joined the game")
send_message(player_name + " joined the game")

log_event(bot.bot_name + " connected")
send_message(bot.bot_name + " connected")

score = 0
bot_score = 0

player_x = 0
player_y = 0

gold_positions = []

for i in range(3):
    gold_x = random.randint(0, MAP_SIZE - 1)
    gold_y = random.randint(0, MAP_SIZE - 1)

    gold_positions.append((gold_x, gold_y))

for gold in gold_positions:
    game_map[gold[1]][gold[0]] = "G"

game_map[bot.bot_y][bot.bot_x] = "B"
game_map[player_y][player_x] = "H"

running = True

while running:

    clear_screen()

    print("Connected Players:", len(players))
    display_players(players)

    print("\nPlayer:", player_name)
    print("Player Score:", score)
    print("Bot Score:", bot_score)
    print("Messages Sent To Server:", get_sent_message_count())

    display_map(game_map)

    move = input("Move (w/a/s/d or q to quit): ")

    simulate_lag(player_name)

    if simulate_lost_message(player_name):
        print("Movement message lost.")

        log_event(player_name + " movement message was lost")
        send_message(player_name + " movement message was lost")

        simulate_reconnect(player_name)

        continue

    game_map[player_y][player_x] = "."
    game_map[bot.bot_y][bot.bot_x] = "."

    if move == "q":
        send_message(player_name + " exited the game")

        log_event(player_name + " exited the game")

        print("Game ended")
        print("Final Player Score:", score)
        print("Final Bot Score:", bot_score)

        running = False

    elif move == "d":
        player_x += 1

        send_message(player_name + " moved RIGHT")
        log_event(player_name + " moved RIGHT")

    elif move == "a":
        player_x -= 1

        send_message(player_name + " moved LEFT")
        log_event(player_name + " moved LEFT")

    elif move == "w":
        player_y -= 1

        send_message(player_name + " moved UP")
        log_event(player_name + " moved UP")

    elif move == "s":
        player_y += 1

        send_message(player_name + " moved DOWN")
        log_event(player_name + " moved DOWN")

    else:
        print("Invalid input.")

        log_event(player_name + " entered invalid input")
        send_message(player_name + " entered invalid input")

    if player_x < 0:
        player_x = 0

    elif player_x >= MAP_SIZE:
        player_x = MAP_SIZE - 1

    if player_y < 0:
        player_y = 0

    elif player_y >= MAP_SIZE:
        player_y = MAP_SIZE - 1

    player_data["x"] = player_x
    player_data["y"] = player_y
    player_data["score"] = score

    # Move smarter bot toward nearby gold
    bot.move_bot(gold_positions)

    # Clear whole map before redraw
    for y in range(MAP_SIZE):

        for x in range(MAP_SIZE):
            game_map[y][x] = "."

    # Redraw all gold positions
    for gold in gold_positions:
        game_map[gold[1]][gold[0]] = "G"

    # Draw updated bot position
    game_map[bot.bot_y][bot.bot_x] = "B"

    # Draw updated player position
    game_map[player_y][player_x] = "H"

    for gold in gold_positions:

        if player_x == gold[0] and player_y == gold[1]:
            print("Gold collected")

            score += 10
            player_data["score"] = score

            log_event(player_name + " collected gold")
            send_message(player_name + " collected gold")

            log_event("Score updated for " + player_name)
            send_message("Score updated for " + player_name)

            gold_positions.remove(gold)

            new_gold_x = random.randint(0, MAP_SIZE - 1)
            new_gold_y = random.randint(0, MAP_SIZE - 1)

            gold_positions.append((new_gold_x, new_gold_y))
            game_map[new_gold_y][new_gold_x] = "G"

            break

    for gold in gold_positions:

        if bot.bot_x == gold[0] and bot.bot_y == gold[1]:
            print("Bot collected gold")

            bot_score += 10

            log_event(bot.bot_name + " collected gold")
            send_message(bot.bot_name + " collected gold")

            log_event("Score updated for " + bot.bot_name)
            send_message("Score updated for " + bot.bot_name)

            gold_positions.remove(gold)

            new_gold_x = random.randint(0, MAP_SIZE - 1)
            new_gold_y = random.randint(0, MAP_SIZE - 1)

            gold_positions.append((new_gold_x, new_gold_y))
            game_map[new_gold_y][new_gold_x] = "G"

            break

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

    log_event(state_message)
    send_message(state_message)

    time.sleep(0.2)