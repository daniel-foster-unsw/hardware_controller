"""
Unit tests for ScanConfigurationSerializer.
"""

from src.scan.models.scan_configuration import (
    ScanConfiguration,
)
from src.serialization.scan_configuration_serializer import (
    ScanConfigurationSerializer,
)


def create_scan_configuration() -> ScanConfiguration:
    """Create a ScanConfiguration."""

    return ScanConfiguration(

        scan_id="20260728_001",

        scan_name="Test Scan",

        start_position_mm=0,

        end_position_mm=1000,

        capture_spacing_mm=50,

        motor_speed_mm_s=100,

        capture_delay_s=1.0,

        enabled_cameras=(
            1,
            2,
            3,
            4,
            5,
        ),

        reset_before_scan=True,

        reset_after_scan=True,

        auto_download=True,

        delete_remote_files=False,
    )


def test_serialize() -> None:
    """Configuration serializes correctly."""

    serializer = (
        ScanConfigurationSerializer()
    )

    configuration = (
        create_scan_configuration()
    )

    data = serializer.serialize(
        configuration,
    )

    assert data["scan_id"] == (
        configuration.scan_id
    )

    assert data["scan_name"] == (
        configuration.scan_name
    )

    assert (
        data["start_position_mm"]
        == 0
    )

    assert (
        data["end_position_mm"]
        == 1000
    )

    assert (
        data["capture_spacing_mm"]
        == 50
    )

    assert (
        data["motor_speed_mm_s"]
        == 100
    )

    assert (
        data["capture_delay_s"]
        == 1.0
    )

    assert (
        data["enabled_cameras"]
        == [1, 2, 3, 4, 5]
    )

    assert (
        data["reset_before_scan"]
        is True
    )

    assert (
        data["reset_after_scan"]
        is True
    )

    assert (
        data["auto_download"]
        is True
    )

    assert (
        data["delete_remote_files"]
        is False
    )


def test_deserialize() -> None:
    """Configuration deserializes correctly."""

    serializer = (
        ScanConfigurationSerializer()
    )

    original = (
        create_scan_configuration()
    )

    data = serializer.serialize(
        original,
    )

    restored = serializer.deserialize(
        data,
    )

    assert restored == original


def test_round_trip() -> None:
    """Configuration survives a round trip."""

    serializer = (
        ScanConfigurationSerializer()
    )

    original = (
        create_scan_configuration()
    )

    restored = serializer.deserialize(
        serializer.serialize(
            original,
        ),
    )

    assert restored == original


def test_enabled_cameras_restored_as_tuple() -> None:
    """Camera IDs are restored as a tuple."""

    serializer = (
        ScanConfigurationSerializer()
    )

    original = (
        create_scan_configuration()
    )

    restored = serializer.deserialize(
        serializer.serialize(
            original,
        ),
    )

    assert isinstance(
        restored.enabled_cameras,
        tuple,
    )

    assert (
        restored.enabled_cameras
        == (1, 2, 3, 4, 5)
    )