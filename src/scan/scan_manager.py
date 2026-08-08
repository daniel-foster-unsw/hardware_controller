"""
Scan manager.
"""

from __future__ import annotations

from threading import Event
from threading import Lock
from threading import Thread

from src.camera.services.capture_service import (
    CaptureService,
)

from src.camera.services.download_service import (
    DownloadService,
)

from src.scan.engine.scan_engine import (
    ScanEngine,
)

from src.scan.engine.scan_runner import (
    ScanAborted,
)

from src.scan.models.scan_configuration import (
    ScanConfiguration,
)

from src.scan.models.scan_context import (
    ScanContext,
)

from src.scan.models.scan_log import (
    ScanLog,
)

from src.scan.models.scan_session import (
    ScanSession,
)

from src.scan.models.scan_state import (
    ScanState,
)

from src.scanner.models.scanner_geometry import (
    ScannerGeometry,
)

from src.scanner.services.motion_service import (
    MotionService,
)


class ScanManager:
    """
    Owns the lifecycle of the current scan.
    """

    def __init__(self) -> None:

        self._context: ScanContext | None = None

        self._engine: ScanEngine | None = None

        self._thread: Thread | None = None

        self._stop_event: Event | None = None

        self._state = ScanState.IDLE

        self._error: Exception | None = None

        self._lock = Lock()

    @property
    def context(
        self,
    ) -> ScanContext | None:
        """
        Return the current scan context.
        """

        return self._context

    @property
    def engine(
        self,
    ) -> ScanEngine | None:
        """
        Return the current scan engine.
        """

        return self._engine

    @property
    def state(
        self,
    ) -> ScanState:
        """
        Return the current scan state.
        """

        with self._lock:

            return self._state

    @property
    def error(
        self,
    ) -> Exception | None:
        """
        Return the scan error, if any.
        """

        with self._lock:

            return self._error

    @property
    def active(
        self,
    ) -> bool:
        """
        Return whether a scan is currently executing.
        """

        with self._lock:

            return (
                self._thread is not None
                and self._thread.is_alive()
            )

    @property
    def scan_created(
        self,
    ) -> bool:
        """
        Return whether a scan context exists.
        """

        return self._context is not None

    def create_scan(
        self,
        configuration: ScanConfiguration,
        geometry: ScannerGeometry,
        motion_service: MotionService,
        capture_service: CaptureService,
        download_service: DownloadService,
    ) -> ScanContext:
        """
        Create the current scan.
        """

        with self._lock:

            if self._context is not None:

                raise RuntimeError(
                    "A scan is already created."
                )

            if self._thread is not None:

                raise RuntimeError(
                    "A scan thread already exists."
                )

            session = ScanSession(
                configuration,
            )

            context = ScanContext(
                configuration=configuration,
                geometry=geometry,
                session=session,
                log=ScanLog(
                    configuration=configuration,
                    start_time=session.start_time,
                ),
            )

            self._context = context

            self._engine = ScanEngine(
                context=context,
                motion_service=motion_service,
                capture_service=capture_service,
                download_service=download_service,
            )

            self._error = None

            self._state = (
                ScanState.CREATE_SCAN
            )

            return context

    def start_scan(self) -> None:
        """
        Start the current scan in a background thread.
        """

        with self._lock:

            if self._context is None:

                raise RuntimeError(
                    "No scan has been created."
                )

            if self._engine is None:

                raise RuntimeError(
                    "No scan engine is available."
                )

            if (
                self._thread is not None
                and self._thread.is_alive()
            ):

                raise RuntimeError(
                    "A scan is already running."
                )

            self._stop_event = Event()

            self._error = None

            self._state = ScanState.MOVE

            self._thread = Thread(
                target=self._run_scan,
                name="ScanRunner",
                daemon=True,
            )

            self._thread.start()

    def stop_scan(self) -> None:
        """
        Request the current scan to stop.
        """

        with self._lock:

            if (
                self._thread is None
                or not self._thread.is_alive()
            ):

                raise RuntimeError(
                    "No scan is currently running."
                )

            self._state = (
                ScanState.ABORTED
            )

            if self._stop_event is not None:

                self._stop_event.set()

            engine = self._engine

        #
        # Do not call the motion service while
        # holding the manager lock.
        #

        if engine is not None:

            engine.stop()

    def clear_scan(self) -> None:
        """
        Clear the current scan.

        A running scan cannot be cleared.
        """

        with self._lock:

            if (
                self._thread is not None
                and self._thread.is_alive()
            ):

                raise RuntimeError(
                    "Cannot clear a running scan."
                )

            self._engine = None

            self._context = None

            self._thread = None

            self._stop_event = None

            self._error = None

            self._state = ScanState.IDLE

    def wait_for_completion(
        self,
        timeout: float | None = None,
    ) -> None:
        """
        Wait for the background scan to finish.
        """

        thread = self._thread

        if thread is not None:

            thread.join(
                timeout=timeout,
            )

    def _run_scan(self) -> None:
        """
        Execute the scan on the background thread.
        """

        engine = self._engine

        stop_event = self._stop_event

        if engine is None or stop_event is None:

            with self._lock:

                self._state = (
                    ScanState.ERROR
                )

                self._error = RuntimeError(
                    "Scan thread started without "
                    "a scan engine or stop event."
                )

            return

        try:

            engine.execute(
                stop_event=stop_event,
            )

        except ScanAborted:

            with self._lock:

                self._state = (
                    ScanState.ABORTED
                )

        except Exception as exception:

            with self._lock:

                self._error = exception

                self._state = (
                    ScanState.ERROR
                )

        else:

            with self._lock:

                self._state = (
                    ScanState.COMPLETE
                )