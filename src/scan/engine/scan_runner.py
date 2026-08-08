"""
Scan execution runner.
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


class ScanRunner:

    def run(
        self,
        context: ScanContext,
        motion: MotionService,
        capture: CaptureService,
        download: DownloadService,
    ) -> None:
        """
        Execute a complete scan.
        """

        #
        # Initialise services.
        #

        motion.initialise(
            context,
        )

        capture.initialise(
            context,
        )

        #
        # Home the scanner.
        #

        motion.home(
            context,
        )

        #
        # Execute scan positions.
        #

        for position in (
            context.session.position_generator
        ):

            motion.move_to(
                context,
                position,
            )

            motion.wait_until_complete(
                context,
            )

            capture_record = (
                capture.capture_position(
                    context,
                )
            )

            context.add_capture(
                capture_record,
            )

        #
        # Download images.
        #

        download.download(
            context,
        )

        #
        # Shutdown services.
        #

        capture.shutdown(
            context,
        )

        motion.shutdown(
            context,
        )