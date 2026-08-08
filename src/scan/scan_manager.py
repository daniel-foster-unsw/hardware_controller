"""
Scan manager.
"""

from __future__ import annotations

from src.camera.services.capture_service import (
    CaptureService,
)
from src.camera.services.download_service import (
    DownloadService,
)
from src.scan.engine.scan_engine import (
    ScanEngine,
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

    @property
    def context(self) -> ScanContext | None:
        """Return the current scan context."""

        return self._context

    @property
    def engine(self) -> ScanEngine | None:
        """Return the current scan engine."""

        return self._engine

    @property
    def active(self) -> bool:
        """Return True if a scan has been created."""

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

        if self.active:
            raise RuntimeError(
                "A scan is already active."
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

        return context

    def start_scan(self) -> None:
        """
        Execute the current scan.
        """

        if self._engine is None:
            raise RuntimeError(
                "No scan has been created."
            )

        self._engine.execute()

    def stop_scan(self) -> None:
        """
        Stop the current scan.
        """

        if self._context is None:
            raise RuntimeError(
                "No scan has been created."
            )

        if self._engine is None:
            raise RuntimeError(
                "No scan engine is available."
            )

        self._engine._motion.stop(
            self._context,
        )

    def clear_scan(self) -> None:
        """
        Clear the current scan.
        """

        self._engine = None

        self._context = None