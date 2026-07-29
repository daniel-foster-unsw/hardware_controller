"""
Scan context.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.scan.models.scan_configuration import (
    ScanConfiguration,
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

from src.scan.models.capture_record import (
    CaptureRecord,
)


@dataclass(
    slots=True,
)
class ScanContext:
    """
    Runtime context for a scan.
    """

    #
    # Configuration
    #

    configuration: ScanConfiguration

    #
    # Scanner
    #

    geometry: ScannerGeometry

    #
    # Runtime
    #

    session: ScanSession

    #
    # Results
    #

    log: ScanLog


    def add_capture(
        self,
        capture: CaptureRecord,
    ) -> None:
        """
        Add a capture record to the scan log.
        """

        self.log.add_capture(
            capture,
        )