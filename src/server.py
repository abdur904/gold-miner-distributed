import zmq
from datetime import datetime

# Store server activity logs
server_logs = []

# Create ZeroMQ variables
context = None
socket = None


# Log distributed server events
def log_event(message):

    current_time = datetime.now().strftime("%H:%M:%S")

    log_message = (
        "[" + current_time + "] "
        + message
    )

    server_logs.append(log_message)

    print("[SERVER LOG]", log_message)


# Start distributed server
def start_server():

    global context
    global socket

    # Create ZeroMQ communication context
    context = zmq.Context()

    # Create server socket
    socket = context.socket(zmq.PAIR)

    # Bind socket to distributed port
    socket.bind("tcp://*:5555")

    log_event(
        "Distributed game server started on port 5555"
    )

    while True:

        try:

            # Receive distributed message
            message = socket.recv_string()

            # Log received message
            log_event("Received: " + message)

        except KeyboardInterrupt:

            log_event("Server shutting down")

            break


# Run server directly
if __name__ == "__main__":

    start_server()