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

    service.home(
        create_scan_context(),
    )

    assert service.homed

    assert service.current_position == 0.0


def test_move() -> None:

    service = MockMotionService()

    service.move_to(
        create_scan_context(),
        250.0,
    )

    assert service.current_position == 250.0


def test_shutdown() -> None:

    service = MockMotionService()

    service.initialise(
        create_scan_context(),
    )

    service.shutdown(
        create_scan_context(),
    )

    assert not service.initialised



def test_visited_positions() -> None:
    """
    Visited positions are recorded.
    """

    service = MockMotionService()

    context = create_scan_context()

    service.move_to(
        context,
        100.0,
    )

    service.move_to(
        context,
        250.0,
    )

    service.move_to(
        context,
        400.0,
    )

    assert service.visited_positions == (
        100.0,
        250.0,
        400.0,
    )


def test_no_positions_before_move() -> None:
    """
    No positions have been visited initially.
    """

    service = MockMotionService()

    assert service.visited_positions == ()