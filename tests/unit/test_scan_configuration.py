"""
Unit tests for ScanConfiguration.
"""

from dataclasses import FrozenInstanceError
from dataclasses import replace

import pytest

from src.scan.models.scan_configuration import (
    ScanConfiguration,
)


def create_configuration() -> ScanConfiguration:
    """Create a valid scan configuration."""

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


def test_create_configuration() -> None:
    """A valid configuration can be created."""

    configuration = create_configuration()

    assert configuration.scan_id == "20260728_001"
    assert configuration.scan_name == "Test Scan"
    assert configuration.capture_count == 21
    assert configuration.camera_count == 5
    assert configuration.estimated_image_count == 105


def test_scan_range() -> None:
    """Scan range is calculated correctly."""

    configuration = create_configuration()

    assert configuration.scan_range_mm == 1000


def test_empty_scan_id() -> None:

    with pytest.raises(ValueError):
        replace(create_configuration(), scan_id="")


def test_empty_scan_name() -> None:

    with pytest.raises(ValueError):
        replace(create_configuration(), scan_name="")


def test_negative_start_position() -> None:

    with pytest.raises(ValueError):
        replace(create_configuration(), start_position_mm=-1)


def test_end_before_start() -> None:

    with pytest.raises(ValueError):
        replace(
            create_configuration(),
            start_position_mm=100,
            end_position_mm=50,
        )


def test_zero_capture_spacing() -> None:

    with pytest.raises(ValueError):
        replace(
            create_configuration(),
            capture_spacing_mm=0,
        )


def test_negative_capture_spacing() -> None:

    with pytest.raises(ValueError):
        replace(
            create_configuration(),
            capture_spacing_mm=-10,
        )


def test_capture_spacing_exceeds_range() -> None:

    with pytest.raises(ValueError):
        replace(
            create_configuration(),
            capture_spacing_mm=2000,
        )


def test_zero_motor_speed() -> None:

    with pytest.raises(ValueError):
        replace(
            create_configuration(),
            motor_speed_mm_s=0,
        )


def test_negative_motor_speed() -> None:

    with pytest.raises(ValueError):
        replace(
            create_configuration(),
            motor_speed_mm_s=-100,
        )


def test_negative_capture_delay() -> None:

    with pytest.raises(ValueError):
        replace(
            create_configuration(),
            capture_delay_s=-1.0,
        )


def test_empty_camera_list() -> None:

    with pytest.raises(ValueError):
        replace(
            create_configuration(),
            enabled_cameras=(),
        )


def test_duplicate_camera_ids() -> None:

    with pytest.raises(ValueError):
        replace(
            create_configuration(),
            enabled_cameras=(1, 2, 2),
        )


def test_invalid_camera_id() -> None:

    with pytest.raises(ValueError):
        replace(
            create_configuration(),
            enabled_cameras=(0, 1, 2),
        )


def test_configuration_is_frozen() -> None:

    configuration = create_configuration()

    with pytest.raises(FrozenInstanceError):
        configuration.scan_name = "Modified"


def test_configuration_equality() -> None:

    assert (
        create_configuration()
        == create_configuration()
    )


def test_configuration_is_hashable() -> None:

    configurations = {
        create_configuration(),
    }

    assert create_configuration() in configurations