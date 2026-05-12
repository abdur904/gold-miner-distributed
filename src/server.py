from datetime import datetime

# Store server activity logs
server_logs = []


# Add activity message to server log
def log_event(message):
    current_time = datetime.now().strftime("%H:%M:%S")

    log_message = "[" + current_time + "] " + message

    server_logs.append(log_message)

    print("[SERVER LOG]", log_message)


# Start distributed game server
print("Server started")


# Example distributed events
log_event("Human player connected")
log_event("Bot connected")
log_event("Player moved RIGHT")
log_event("Gold collected")
log_event("Player score updated")