"""
Unit tests for CameraGeometry.
"""

from dataclasses import FrozenInstanceError

import pytest

from src.scanner.enums.camera_id import CameraID
from src.configuration.scanner.camera_geometry import (
    CameraGeometry,
)


def test_create_camera_geometry() -> None:
    """Camera geometry can be created."""

    geometry = CameraGeometry(
        camera_id=CameraID.CAM01,
        camera_number=1,
        fixed_x_mm=0.0,
        uses_vertical_motor=True,
        vertical_motor_id=1,
    )

    assert geometry.camera_id == CameraID.CAM01

    assert geometry.camera_number == 1


def test_camera_geometry_is_frozen() -> None:
    """Camera geometry is immutable."""

    geometry = CameraGeometry(
        camera_id=CameraID.CAM01,
        camera_number=1,
    )

    with pytest.raises(FrozenInstanceError):

        geometry.camera_number = 2
        