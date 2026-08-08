"""
Scan engine.
"""

from __future__ import annotations

from src.camera.services.capture_service import (
    CaptureService,
)
from src.camera.services.download_service import (
    DownloadService,
)
from src.scan.models.scan_context import (
    ScanContext,
)
from src.scanner.services.motion_service import (
    MotionService,
)
from src.scan.engine.scan_runner import (
    ScanRunner,
)


class ScanEngine:
    """
    Coordinates the execution of a scan.
    """

    def __init__(
        self,
        context: ScanContext,
        motion_service: MotionService,
        capture_service: CaptureService,
        download_service: DownloadService,
        runner: ScanRunner | None = None,
    ) -> None:
        """
        Initialise the scan engine.
        """

        self._context = context

        self._motion = motion_service

        self._capture = capture_service

        self._download = download_service

        self._runner = (
            runner
            if runner is not None
            else ScanRunner()
        )
        
    @property
    def context(
        self,
    ) -> ScanContext:
        """
        Return the current scan context.
        """

        return self._context

    def execute(self) -> None:
        """
        Execute a scan.
        """

        self._runner.run(
            context=self._context,
            motion=self._motion,
            capture=self._capture,
            download=self._download,
        )


    def stop(self) -> None:
        """
        Stop the current scan.
        """

        self._motion.stop(
            self._context,
        )