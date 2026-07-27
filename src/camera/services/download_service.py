"""
Download service interface.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.scan.models.scan_context import (
    ScanContext,
)


class DownloadService(ABC):
    """
    Image download interface.
    """

    @abstractmethod
    def download(
        self,
        context: ScanContext,
    ) -> None:
        """
        Download captured images.
        """

    @abstractmethod
    def delete_remote(
        self,
        context: ScanContext,
    ) -> None:
        """
        Delete remote images.
        """