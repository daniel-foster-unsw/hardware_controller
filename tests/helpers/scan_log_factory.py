"""
Shared ScanLog factory for tests.
"""

from datetime import datetime

from src.scan.models.scan_log import (
    ScanLog,
)

from tests.helpers.capture_record_factory import (
    create_capture_record,
)
from tests.helpers.configuration_factory import (
    create_scan_configuration,
)


def create_scan_log() -> ScanLog:
    """
    Create a valid ScanLog.
    """

    log = ScanLog(
        configuration=create_scan_configuration(),
        start_time=datetime.now(),
    )

    log.add_capture(
        create_capture_record(),
    )

    return log