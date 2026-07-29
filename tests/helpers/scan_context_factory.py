"""
Shared ScanContext factory.
"""

from datetime import datetime

from src.scan.models.scan_context import (
    ScanContext,
)
from src.scan.models.scan_log import (
    ScanLog,
)
from src.scan.models.scan_session import (
    ScanSession,
)
from src.scanner.factories.scanner_geometry_factory import (
    create_scanner_geometry,
)
from tests.helpers.configuration_factory import (
    create_scan_configuration,
)


def create_scan_context() -> ScanContext:
    """
    Create a valid ScanContext.
    """

    configuration = create_scan_configuration()

    session = ScanSession(
        configuration,
    )

    return ScanContext(
        configuration=configuration,
        geometry=create_scanner_geometry(),
        session=session,
        log=ScanLog(
            configuration=configuration,
            start_time=datetime.now(),
        ),
    )