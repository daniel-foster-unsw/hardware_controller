"""
Unit tests for MockCaptureService.
"""

from src.camera.services.mock_capture_service import (
    MockCaptureService,
)
from tests.helpers.scan_context_factory import (
    create_scan_context,
)


def test_initialise() -> None:
    """Service initialises."""

    service = MockCaptureService()

    service.initialise(
        create_scan_context(),
    )

    assert service.initialised


def test_capture() -> None:
    """Capture returns a CaptureRecord."""

    service = MockCaptureService()

    context = create_scan_context()

    service.initialise(context)

    record = service.capture_position(
        context,
    )

    assert record.capture_index == 1

    assert record.camera_count == 5

    assert service.capture_count == 1


def test_multiple_captures() -> None:
    """Multiple captures are recorded."""

    service = MockCaptureService()

    context = create_scan_context()

    service.initialise(context)

    service.capture_position(context)

    service.capture_position(context)

    service.capture_position(context)

    assert service.capture_count == 3

    assert len(service.captures) == 3


def test_shutdown() -> None:
    """Shutdown resets state."""

    service = MockCaptureService()

    context = create_scan_context()

    service.initialise(context)

    service.shutdown(context)

    assert not service.initialised