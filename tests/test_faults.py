import sys
import time
from pathlib import Path

# Add src folder to Python path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from faults import simulate_lag, simulate_lost_message, simulate_reconnect


def test_simulate_lag_runs():
    """
    Test that simulate_lag() runs without crashing.
    This supports the test plan for simulated network lag.
    """
    start_time = time.time()

    simulate_lag("TestPlayer")

    end_time = time.time()

    assert end_time >= start_time


def test_simulate_lost_message_returns_boolean():
    """
    Test that simulate_lost_message() returns True or False.
    This supports the test plan for lost distributed messages.
    """
    result = simulate_lost_message("TestPlayer")

    assert result in [True, False]


def test_simulate_reconnect_runs():
    """
    Test that simulate_reconnect() runs without crashing.
    This supports the test plan for reconnect recovery simulation.
    """
    result = simulate_reconnect("TestPlayer")

    assert result is None