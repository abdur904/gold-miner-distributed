import random
from server import log_event

# Bot player name
bot_name = "Bot_1"

# Starting bot position
bot_x = 10
bot_y = 10

# Display bot connection message
print(bot_name, "connected")

# Log bot connection on server side
log_event(bot_name + " connected")

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

# Display bot movement
print(bot_name, "moved", direction)

# Log bot movement
log_event(bot_name + " moved " + direction)