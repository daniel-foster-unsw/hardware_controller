"""
Unit tests for ScanLog.
"""

from datetime import timedelta

from tests.helpers.capture_record_factory import (
    create_capture_record,
)
from tests.helpers.scan_log_factory import (
    create_scan_log,
)


def test_create_scan_log() -> None:
    """ScanLog can be created."""

    log = create_scan_log()

    assert log.capture_count == 1


def test_add_capture() -> None:
    """Capture records can be added."""

    log = create_scan_log()

    log.add_capture(
        create_capture_record(),
    )

    assert log.capture_count == 2


def test_image_count() -> None:
    """Image count is calculated."""

    log = create_scan_log()

    assert log.image_count == 5


def test_successful_images() -> None:
    """Successful image count is calculated."""

    log = create_scan_log()

    assert log.successful_images == 5


def test_failed_images() -> None:
    """Failed image count is calculated."""

    log = create_scan_log()

    assert log.failed_images == 0


def test_completed_false() -> None:
    """Scan is initially incomplete."""

    log = create_scan_log()

    assert not log.completed


def test_completed_true() -> None:
    """Completed scan is detected."""

    log = create_scan_log()

    log.end_time = (
        log.start_time
        + timedelta(seconds=10)
    )

    assert log.completed


def test_duration() -> None:
    """Duration is calculated."""

    log = create_scan_log()

    log.end_time = (
        log.start_time
        + timedelta(seconds=15)
    )

    assert log.duration_seconds == 15.0