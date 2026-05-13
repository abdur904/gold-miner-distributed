import random
import time
from server import log_event
from network import send_message


def simulate_lag(player_name):
    lag_time = random.uniform(0.1, 0.5)

    log_event(
        "Simulated network lag: "
        + str(round(lag_time, 2))
        + " seconds"
    )

    send_message(
        "Lag simulated for "
        + player_name
        + ": "
        + str(round(lag_time, 2))
        + " seconds"
    )

    time.sleep(lag_time)


def simulate_lost_message(player_name):
    message_lost = random.choice([True, False, False])

    if message_lost:
        log_event("Simulated lost message detected")
        send_message("Lost message simulated for " + player_name)

    return message_lost


def simulate_reconnect(player_name):
    print("Reconnecting to distributed server...")

    log_event(player_name + " attempting reconnection")
    send_message(player_name + " attempting reconnection")

    time.sleep(1)

    print("Reconnection successful")

    log_event(player_name + " reconnected successfully")
    send_message(player_name + " reconnected successfully")