"""
Shared ScannerPose factory for tests.
"""

from src.scanner.models.scanner_pose import (
    ScannerPose,
)


def create_scanner_pose() -> ScannerPose:
    """
    Create a valid ScannerPose.
    """

    return ScannerPose(
        arm_x_mm=250.0,
        camera1_z_mm=320.0,
        camera2_z_mm=315.0,
        camera4_z_mm=305.0,
        camera5_z_mm=295.0,
    )