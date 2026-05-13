import zmq
from server import log_event

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:5555")

sent_message_count = 0


def send_message(message):
    global sent_message_count

    try:
        socket.send_string(message, flags=zmq.NOBLOCK)
        sent_message_count += 1

    except zmq.Again:
        log_event("ZeroMQ message could not be sent immediately: " + message)


def get_sent_message_count():
    return sent_message_count