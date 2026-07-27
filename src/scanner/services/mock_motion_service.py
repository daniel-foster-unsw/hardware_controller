"""
Mock motion service.
"""

from __future__ import annotations

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

    def __init__(self) -> None:

        self.initialised = False

        self.homed = False

        self.current_position = 0.0

    def initialise(
        self,
        context: ScanContext,
    ) -> None:

        self.initialised = True

    def home(
        self,
        context: ScanContext,
    ) -> None:

        self.homed = True

        self.current_position = 0.0

    def move_to(
        self,
        context: ScanContext,
        position_mm: float,
    ) -> None:

        self.current_position = position_mm

    def wait_until_complete(
        self,
        context: ScanContext,
    ) -> None:

        # Instant in mock.
        pass

    def stop(
        self,
        context: ScanContext,
    ) -> None:

        pass

    def shutdown(
        self,
        context: ScanContext,
    ) -> None:

        self.initialised = False