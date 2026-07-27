"""
Scan engine.
"""

from __future__ import annotations

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
from src.configuration.scanner.scanner_geometry_factory import (
    create_scanner_geometry,
)


class ScanEngine:
    """
    Coordinates a scan.
    """

    def __init__(
        self,
        configuration: ScanConfiguration,
    ) -> None:

        session = ScanSession(
            configuration,
        )

        self._context = ScanContext(
            configuration=configuration,
            geometry=create_scanner_geometry(),
            session=session,
            log=ScanLog(
                configuration=configuration,
                start_time=session.start_time,
            ),
        )

    @property
    def context(
        self,
    ) -> ScanContext:
        """
        Return the current scan context.
        """

        return self._context