"""
Capture service interface.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.scan.models.capture_record import (
    CaptureRecord,
)
from src.scan.models.scan_context import (
    ScanContext,
)


class CaptureService(ABC):
    """
    Image capture interface.
    """

    @abstractmethod
    def initialise(
        self,
        context: ScanContext,
    ) -> None:
        """
        Initialise cameras.
        """

    @abstractmethod
    def capture_position(
        self,
        context: ScanContext,
    ) -> CaptureRecord:
        """
        Capture one scan position.
        """

    @abstractmethod
    def shutdown(
        self,
        context: ScanContext,
    ) -> None:
        """
        Shutdown cameras.
        """

    def add_capture(
        self,
        capture: CaptureRecord,
    ) -> None:
        """
        Add a capture to the scan log.
        """

        self.log.add_capture(
            capture,
        )