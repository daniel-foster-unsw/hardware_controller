"""
Unit tests for ScanState.
"""

from src.scan.models.scan_state import ScanState


def test_scan_state_count() -> None:
    """All scan states are defined."""

    assert len(ScanState) == 14


def test_initial_state() -> None:
    """Idle is the initial state."""

    assert ScanState.IDLE.value == "Idle"


def test_terminal_states() -> None:
    """Terminal states exist."""

    assert ScanState.COMPLETE.value == "Complete"

    assert ScanState.ERROR.value == "Error"

    assert ScanState.ABORTED.value == "Aborted"


def test_wait_states() -> None:
    """Asynchronous wait states exist."""

    assert ScanState.WAIT_FOR_MOTION.value == "Wait For Motion"

    assert ScanState.WAIT_FOR_CAPTURE.value == "Wait For Capture"