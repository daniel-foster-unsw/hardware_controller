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
from src.configuration.scanner.scanner_geometry import (
    ScannerGeometry,
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