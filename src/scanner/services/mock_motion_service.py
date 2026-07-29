"""
Mock motion service.
"""

from __future__ import annotations

from src.scan.models.scan_context import ScanContext
from src.scanner.services.motion_service import MotionService


class MockMotionService(MotionService):
    """
    Mock implementation of MotionService.
    """

    def __init__(self) -> None:

        self._initialised = False

        self._homed = False

        self._current_position = 0.0

        self._visited_positions: list[float] = []

    @property
    def initialised(self) -> bool:
        """
        Return whether the motion system is initialised.
        """

        return self._initialised

    @property
    def homed(self) -> bool:
        """
        Return whether the scanner has been homed.
        """

        return self._homed

    @property
    def current_position(self) -> float:
        """
        Return the current scanner position.
        """

        return self._current_position

    @property
    def visited_positions(self) -> tuple[float, ...]:
        """
        Return all visited scan positions.
        """

        return tuple(
            self._visited_positions
        )

    def initialise(
        self,
        context: ScanContext,
    ) -> None:
        """
        Initialise the motion system.
        """

        self._initialised = True

    def home(
        self,
        context: ScanContext,
    ) -> None:
        """
        Home the scanner.
        """

        self._homed = True

        self._current_position = 0.0

    def move_to(
        self,
        context: ScanContext,
        position_mm: float,
    ) -> None:
        """
        Move to a scan position.
        """

        self._current_position = position_mm

        self._visited_positions.append(
            position_mm,
        )

    def wait_until_complete(
        self,
        context: ScanContext,
    ) -> None:
        """
        Motion is instantaneous in the mock.
        """

    def stop(
        self,
        context: ScanContext,
    ) -> None:
        """
        Stop the scanner.
        """

    def shutdown(
        self,
        context: ScanContext,
    ) -> None:
        """
        Shutdown the motion system.
        """

        self._initialised = False