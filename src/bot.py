from server import log_event

# Bot player name
bot_name = "Bot_1"

# Starting bot position
bot_x = 10
bot_y = 10

print(bot_name, "connected")

# Log bot connection
log_event(bot_name + " connected")

# Move bot left
bot_x -= 1

print(bot_name, "moved LEFT")

# Log bot movement
log_event(bot_name + " moved LEFT")