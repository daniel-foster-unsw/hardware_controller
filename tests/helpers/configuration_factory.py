"""
Shared ScanConfiguration factory for tests.
"""

from src.scan.models.scan_configuration import (
    ScanConfiguration,
)


def create_scan_configuration() -> ScanConfiguration:
    """
    Create a valid ScanConfiguration.
    """

    return ScanConfiguration(
        scan_id="20260728_001",
        scan_name="Test Scan",
        start_position_mm=0,
        end_position_mm=1000,
        capture_spacing_mm=50,
        motor_speed_mm_s=100,
        capture_delay_s=0.5,
        enabled_cameras=(1, 2, 3, 4, 5),
        reset_before_scan=True,
        reset_after_scan=True,
        auto_download=True,
        delete_remote_files=False,
    )