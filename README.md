# Distributed Gold Miner Game

## Overview

This project is a Python terminal-based distributed Gold Miner prototype for COIT13229 Applied Distributed Systems Assignment 2.

The game allows one human player to compete against an automated bot on a 20x20 map while collecting gold objects. The project uses ZeroMQ to send distributed messages between the gameplay client and the distributed server node.

The system demonstrates distributed systems concepts such as:

- Network lag simulation
- Lost message simulation
- Reconnect recovery simulation
- Distributed communication
- Server-side logging
- Basic automated fault simulation testing

## Technologies Used

- Python 3
- ZeroMQ / pyzmq
- pytest

## Features

- Human player movement
- Automated bot movement
- Gold collection system
- Score tracking
- Distributed message sending
- Simulated network faults
- Server-side event logging
- Terminal-based 20x20 game map
- Automated pytest tests for fault simulation functions

## Project Structure

```text
gold-miner-distributed/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── game.py
│   ├── bot.py
│   ├── display.py
│   ├── faults.py
│   ├── network.py
│   └── server.py
├── tests/
│   └── test_faults.py
├── diagrams/
│   ├── use_case_diagram.png
│   ├── component_deployment_diagram.png
│   ├── high_level_class_diagram.png
│   ├── normal_gameplay_sequence_diagram.png
│   └── lost_message_reconnect_sequence_diagram.png

```

## Requirements

The `requirements.txt` file should contain:

```text
pyzmq>=26.0
pytest>=8.0
```

## Setup

Open Terminal and go to the project folder:

```bash
cd gold-miner-distributed
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment.

On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## How to Run the Project

Open two terminals in the project folder.

### Terminal 1 - Start the Server

```bash
python3 src/server.py
```

Expected output:

```text
[SERVER LOG] Distributed game server started on port 5555
```

Keep this terminal open while running the game.

### Terminal 2 - Start the Game Client

```bash
python3 src/game.py
```

When asked, enter a player name:

```text
Enter your name: Abdur
```

## Game Controls

```text
w = move up
a = move left
s = move down
d = move right
q = quit game
```

## How to Run Automated Tests

The project includes automated pytest tests for the fault simulation functions.

Run:

```bash
pytest -v
```

Expected result:

```text
tests/test_faults.py::test_simulate_lag_runs PASSED
tests/test_faults.py::test_simulate_lost_message_returns_boolean PASSED
tests/test_faults.py::test_simulate_reconnect_runs PASSED

3 passed
```

## Manual Testing

Manual testing was completed using terminal screenshots.

The main manual tests include:

- Starting the distributed server
- Starting the game client
- Player movement
- Server receiving distributed messages
- Bot movement toward gold
- Player gold collection
- Simulated network lag
- Simulated lost message
- Reconnect recovery
- Boundary movement
- Quit game and final statistics

## Lost Message Test

To force a lost message for testing, temporarily update `faults.py`.

Change:

```python
message_lost = random.choice([True, False, False])
```

to:

```python
message_lost = True
```

Then run the server and game again.

After taking screenshots, change it back to:

```python
message_lost = random.choice([True, False, False])
```

## Notes

This implementation is a prototype distributed system. It currently supports one human player, one bot module, and one distributed server node.

The bot logic runs inside the gameplay client as a separate module. In future development, the architecture could be extended to support multiple human players and independent bot nodes using more scalable ZeroMQ communication patterns.