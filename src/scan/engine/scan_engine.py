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
    ) -> None:
        """
        Initialise the scan engine.
        """

        self._context = context

        self._motion = motion_service

        self._capture = capture_service

        self._download = download_service

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

        #
        # Initialise services.
        #

        self._motion.initialise(
            self._context,
        )

        self._capture.initialise(
            self._context,
        )

        #
        # Home the scanner.
        #

        self._motion.home(
            self._context,
        )

        #
        # Execute scan positions.
        #

        for position in (
            self._context.session.position_generator
        ):

            self._motion.move_to(
                self._context,
                position,
            )

            self._motion.wait_until_complete(
                self._context,
            )

            self._context.add_capture(

                self._capture.capture_position(
                    self._context,
                )

            )

            

        #
        # Download images.
        #

        self._download.download(
            self._context,
        )

        #
        # Shutdown services.
        #

        self._capture.shutdown(
            self._context,
        )

        self._motion.shutdown(
            self._context,
        )