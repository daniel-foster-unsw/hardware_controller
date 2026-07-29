"""
Mock download service.
"""

from __future__ import annotations

from src.camera.services.download_service import (
    DownloadService,
)
from src.scan.models.scan_context import (
    ScanContext,
)


class MockDownloadService(
    DownloadService,
):
    """
    Mock implementation of DownloadService.
    """

    def __init__(self) -> None:

        self._downloaded = False

        self._download_count = 0

    @property
    def downloaded(self) -> bool:
        """
        Return whether a download has occurred.
        """

        return self._downloaded

    @property
    def download_count(self) -> int:
        """
        Return the number of downloaded images.
        """

        return self._download_count

    def download(
        self,
        context: ScanContext,
    ) -> None:
        """
        Simulate downloading images.
        """

        self._downloaded = True

        self._download_count = (
            context.log.image_count
        )

    def delete_remote(
        self,
        context: ScanContext,
    ) -> None:
        """
        Simulate deleting remote images.
        """

        # Nothing required for the mock.

        pass