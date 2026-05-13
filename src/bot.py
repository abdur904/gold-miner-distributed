from server import log_event
from network import send_message

# Bot player name
bot_name = "Bot_1"

# Starting bot position
bot_x = 10
bot_y = 10


# Move bot automatically toward nearby gold
def move_bot(gold_positions):

    global bot_x
    global bot_y

    # Stop movement if no gold exists
    if len(gold_positions) == 0:
        return

    # Find nearest gold object
    nearest_gold = gold_positions[0]

    shortest_distance = (
        abs(bot_x - nearest_gold[0])
        + abs(bot_y - nearest_gold[1])
    )

    for gold in gold_positions:

        distance = (
            abs(bot_x - gold[0])
            + abs(bot_y - gold[1])
        )

        if distance < shortest_distance:

            shortest_distance = distance
            nearest_gold = gold

    direction = "STAY"

    # Move horizontally toward gold
    if bot_x < nearest_gold[0]:

        bot_x += 1
        direction = "RIGHT"

    elif bot_x > nearest_gold[0]:

        bot_x -= 1
        direction = "LEFT"

    # Move vertically toward gold
    elif bot_y < nearest_gold[1]:

        bot_y += 1
        direction = "DOWN"

    elif bot_y > nearest_gold[1]:

        bot_y -= 1
        direction = "UP"

    # Prevent bot from moving outside map
    if bot_x < 0:
        bot_x = 0

    elif bot_x >= 20:
        bot_x = 19

    if bot_y < 0:
        bot_y = 0

    elif bot_y >= 20:
        bot_y = 19

    # Create movement message
    bot_message = (
        bot_name
        + " moved "
        + direction
    )

    # Send distributed movement update
    send_message(bot_message)

    # Log bot movement
    log_event(bot_message)