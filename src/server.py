import zmq
from datetime import datetime

server_logs = []

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:5555")


def log_event(message):
    current_time = datetime.now().strftime("%H:%M:%S")
    log_message = "[" + current_time + "] " + message
    server_logs.append(log_message)
    print("[SERVER LOG]", log_message)


def start_server():
    log_event("Distributed game server started on port 5555")

    while True:
        try:
            message = socket.recv_string()
            log_event("Received: " + message)

        except KeyboardInterrupt:
            log_event("Server shutting down")
            break


if __name__ == "__main__":
    start_server()