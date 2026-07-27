"""
Unit tests for ScanContext.
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
from src.configuration.scanner.scanner_geometry_factory import (
    create_scanner_geometry,
)
from tests.helpers.configuration_factory import (
    create_scan_configuration,
)


def test_create_scan_context() -> None:
    """
    ScanContext can be created.
    """

    configuration = create_scan_configuration()

    session = ScanSession(
        configuration,
    )

    context = ScanContext(
        configuration=configuration,
        geometry=create_scanner_geometry(),
        session=session,
        log=ScanLog(
            configuration=configuration,
            start_time=datetime.now(),
        ),
    )

    assert context.configuration == configuration

    assert context.session == session

    assert context.geometry.camera_count == 5