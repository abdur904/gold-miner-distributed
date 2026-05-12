import random
from server import log_event

# Bot player name
bot_name = "Bot_1"

# Starting bot position
bot_x = 10
bot_y = 10


# Update bot movement
def move_bot():

    global bot_x
    global bot_y

    # Select random movement direction
    direction = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])

    # Move bot left
    if direction == "LEFT":
        bot_x -= 1

    # Move bot right
    elif direction == "RIGHT":
        bot_x += 1

    # Move bot up
    elif direction == "UP":
        bot_y -= 1

    # Move bot down
    elif direction == "DOWN":
        bot_y += 1

    # Prevent bot from moving outside the game map
    if bot_x < 0:
        bot_x = 0

    elif bot_x >= 20:
        bot_x = 19

    if bot_y < 0:
        bot_y = 0

    elif bot_y >= 20:
        bot_y = 19

    # Log bot movement
    log_event(bot_name + " moved " + direction)