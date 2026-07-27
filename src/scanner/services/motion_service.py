"""
Motion service interface.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.scan.models.scan_context import (
    ScanContext,
)


class MotionService(ABC):
    """
    Scanner motion interface.
    """

    @abstractmethod
    def initialise(
        self,
        context: ScanContext,
    ) -> None:
        """
        Initialise the motion system.
        """

    @abstractmethod
    def home(
        self,
        context: ScanContext,
    ) -> None:
        """
        Home the scanner.
        """

    @abstractmethod
    def move_to(
        self,
        context: ScanContext,
        position_mm: float,
    ) -> None:
        """
        Move to a scan position.
        """

    @abstractmethod
    def wait_until_complete(
        self,
        context: ScanContext,
    ) -> None:
        """
        Wait for motion to complete.
        """

    @abstractmethod
    def stop(
        self,
        context: ScanContext,
    ) -> None:
        """
        Emergency stop.
        """

    @abstractmethod
    def shutdown(
        self,
        context: ScanContext,
    ) -> None:
        """
        Shutdown motion system.
        """