"""
Mock motion service.
"""

from __future__ import annotations

from threading import Event

from src.scan.models.scan_context import (
    ScanContext,
)

from src.scanner.services.motion_service import (
    MotionService,
)


class MockMotionService(MotionService):
    """
    Mock implementation of MotionService.
    """

    def __init__(self, block_motion: bool = False) -> None:

        self._initialised = False

        self._homed = False

        self._current_position = 0.0

        self._visited_positions: list[float] = []

        #
        # Synchronisation
        #

        self.started_event = Event()

        self.release_event = Event()

        self.stopped = False

        self._block_motion = block_motion

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

        self.started_event.set()

        if self._block_motion:
            self.release_event.wait()

        if self.stopped:
            return

        self._current_position = position_mm

        self._visited_positions.append(
            position_mm,
        )

    def wait_until_complete(
        self,
        context: ScanContext,
    ) -> None:
        """
        Wait for the mock motion operation to complete.
        """

        if self._block_motion:
            self.release_event.wait()

    def stop(
        self,
        context: ScanContext,
    ) -> None:
        """
        Stop the scanner.
        """

        self.stopped = True

        self.release_event.set()

    def shutdown(
        self,
        context: ScanContext,
    ) -> None:
        """
        Shutdown the motion system.
        """

        self._initialised = False