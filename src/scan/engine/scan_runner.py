"""
Scan execution runner.
"""

from __future__ import annotations

from threading import Event

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


class ScanAborted(Exception):
    """
    Raised when a scan is requested to stop.
    """


class ScanRunner:
    """
    Executes the individual stages of a scan.
    """

    def run(
        self,
        context: ScanContext,
        motion: MotionService,
        capture: CaptureService,
        download: DownloadService,
        stop_event: Event | None = None,
    ) -> None:
        """
        Execute a complete scan.

        The optional stop event allows the scan manager
        to request termination between scan operations.
        """

        if stop_event is None:

            stop_event = Event()

        try:

            #
            # Initialise services.
            #

            self._check_stop(
                stop_event,
            )

            motion.initialise(
                context,
            )

            capture.initialise(
                context,
            )

            #
            # Home the scanner.
            #

            self._check_stop(
                stop_event,
            )

            motion.home(
                context,
            )

            #
            # Execute scan positions.
            #

            for position in (
                context.session.position_generator
            ):

                self._check_stop(
                    stop_event,
                )

                motion.move_to(
                    context,
                    position,
                )

                self._check_stop(
                    stop_event,
                )

                motion.wait_until_complete(
                    context,
                )

                self._check_stop(
                    stop_event,
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

            self._check_stop(
                stop_event,
            )

            download.download(
                context,
            )

        finally:

            #
            # Always shut down the services.
            #

            capture.shutdown(
                context,
            )

            motion.shutdown(
                context,
            )

    @staticmethod
    def _check_stop(
        stop_event: Event,
    ) -> None:
        """
        Raise ScanAborted if a stop was requested.
        """

        if stop_event.is_set():

            raise ScanAborted(
                "Scan was aborted."
            )