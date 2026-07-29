"""
Unit tests for ScannerGeometry.
"""

import pytest

from src.scanner.enums.camera_id import CameraID
from src.scanner.factories.scanner_geometry_factory import (
    create_scanner_geometry,
)


def test_camera_count() -> None:
    """Geometry contains five cameras."""

    geometry = create_scanner_geometry()

    assert geometry.camera_count == 5


def test_find_camera() -> None:
    """Camera lookup succeeds."""

    geometry = create_scanner_geometry()

    camera = geometry.camera(
        CameraID.CAM03,
    )

    assert camera.camera_number == 3


def test_invalid_camera() -> None:
    """Unknown cameras raise KeyError."""

    geometry = create_scanner_geometry()

    class FakeCamera:
        name = "UNKNOWN"

    with pytest.raises(KeyError):

        geometry.camera(FakeCamera())  # type: ignore[arg-type]