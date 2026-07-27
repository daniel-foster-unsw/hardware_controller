"""
Unit tests for ScanSession.
"""

from datetime import timedelta

from src.scan.models.scan_session import (
    ScanSession,
)
from src.scan.models.scan_state import (
    ScanState,
)
from tests.helpers.configuration_factory import (
    create_scan_configuration,
)


def test_create_session() -> None:
    """Session can be created."""

    session = ScanSession(
        configuration=create_scan_configuration(),
    )

    assert session.state == ScanState.IDLE

    assert session.current_position_index == 0

    assert session.current_position_mm == 0

    assert session.downloaded_images == 0

    assert session.failed_images == 0


def test_total_positions() -> None:
    """Total positions are calculated."""

    session = ScanSession(
        configuration=create_scan_configuration(),
    )

    assert session.total_positions == 21


def test_total_images() -> None:
    """Total image count is calculated."""

    session = ScanSession(
        configuration=create_scan_configuration(),
    )

    assert session.total_images == 105


def test_progress_initial() -> None:
    """Progress starts at zero."""

    session = ScanSession(
        configuration=create_scan_configuration(),
    )

    assert session.progress == 0.0


def test_progress_halfway() -> None:
    """Progress updates correctly."""

    session = ScanSession(
        configuration=create_scan_configuration(),
    )

    session.current_position_index = (
        session.total_positions - 1
    ) // 2

    assert session.progress == 0.5


def test_completed_false() -> None:
    """Session is not complete."""

    session = ScanSession(
        configuration=create_scan_configuration(),
    )

    assert not session.completed


def test_completed_true() -> None:
    """Session reports complete."""

    session = ScanSession(
        configuration=create_scan_configuration(),
    )

    session.state = ScanState.COMPLETE

    assert session.completed


def test_end_time_initially_none() -> None:
    """End time is initially None."""

    session = ScanSession(
        configuration=create_scan_configuration(),
    )

    assert session.end_time is None


def test_duration() -> None:
    """Duration is calculated."""

    session = ScanSession(
        configuration=create_scan_configuration(),
    )

    session.end_time = (
        session.start_time
        + timedelta(seconds=30)
    )

    assert session.duration == 30.0

    def test_current_position() -> None:
        """Current position is derived from the scan plan."""

        session = ScanSession(
            configuration=create_scan_configuration(),
        )

        session.current_position_index = 5

        assert session.current_position_mm == 250