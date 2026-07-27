"""
Unit tests for ScannerGeometryFactory.
"""

from src.scanner.enums.camera_id import CameraID
from src.configuration.scanner.scanner_geometry_factory import (
    create_scanner_geometry,
)


def test_default_geometry() -> None:
    """Default geometry is correct."""

    geometry = create_scanner_geometry()

    assert geometry.camera_count == 5

    assert geometry.camera(
        CameraID.CAM01
    ).uses_arm_x is False

    assert geometry.camera(
        CameraID.CAM02
    ).uses_arm_x is True

    assert geometry.camera(
        CameraID.CAM03
    ).uses_arm_x is True

    assert geometry.camera(
        CameraID.CAM04
    ).uses_arm_x is True

    assert geometry.camera(
        CameraID.CAM05
    ).uses_arm_x is False

    assert geometry.camera(
        CameraID.CAM03
    ).uses_vertical_motor is False

    assert geometry.camera(
        CameraID.CAM05
    ).uses_vertical_motor is True