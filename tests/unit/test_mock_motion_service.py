"""
Unit tests for MockMotionService.
"""

from src.scanner.services.mock_motion_service import (
    MockMotionService,
)
from tests.helpers.scan_context_factory import (
    create_scan_context,
)


def test_initialise() -> None:

    service = MockMotionService()

    service.initialise(
        create_scan_context(),
    )

    assert service.initialised


def test_home() -> None:

    service = MockMotionService()

    context = create_scan_context()

    service.home(
        context,
    )

    assert service.homed

    assert service.current_position == 0.0


def test_move() -> None:

    service = MockMotionService()

    context = create_scan_context()

    service.move_to(
        context,
        250.0,
    )

    assert (
        service.current_position
        == 250.0
    )


def test_shutdown() -> None:

    service = MockMotionService()

    context = create_scan_context()

    service.initialise(
        context,
    )

    service.shutdown(
        context,
    )

    assert not service.initialised