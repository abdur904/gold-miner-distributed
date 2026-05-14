# Distributed Gold Miner Game

## Overview

This project is a Python terminal-based distributed Gold Miner prototype for COIT13229 Assignment 2.

The game allows one human player to compete against an automated bot on a 20x20 map while collecting gold objects. The project uses ZeroMQ to send distributed messages between the gameplay client and the server.

The system demonstrates distributed systems concepts such as:

- Network lag simulation
- Lost message simulation
- Reconnect recovery simulation
- Distributed communication
- Server-side logging

## Technologies Used

- Python 3
- ZeroMQ (pyzmq)

## Features

- Human player movement
- Automated bot movement
- Gold collection system
- Score tracking
- Distributed message sending
- Simulated network faults
- Server-side event logging
- Terminal-based 20x20 game map

## Project Structure

```text
src/
├── game.py       # Main gameplay loop
├── bot.py        # Bot movement logic
├── display.py    # Terminal display functions
├── faults.py     # Lag, lost message, and reconnect simulation
├── network.py    # ZeroMQ message sending
└── server.py     # ZeroMQ message receiver and event logger