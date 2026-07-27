"""
Unit tests for CaptureRecordSerializer.
"""

from datetime import datetime

from src.scanner.enums.camera_id import CameraID
from src.scanner.models.camera_pose import CameraPose
from src.scan.models.capture_record import CaptureRecord
from src.scanner.models.scanner_pose import ScannerPose
from src.serialization.capture_record_serializer import (
    CaptureRecordSerializer,
)


TEST_TIME = datetime(
    2026,
    7,
    28,
    12,
    0,
    0,
)


def create_capture_record() -> CaptureRecord:
    """Create a CaptureRecord."""

    return CaptureRecord(

        capture_index=17,

        target_position_mm=250.0,

        timestamp=TEST_TIME,

        scanner_pose=ScannerPose(
            arm_x_mm=250.0,
            camera1_z_mm=320.0,
            camera2_z_mm=315.0,
            camera4_z_mm=305.0,
            camera5_z_mm=295.0,
        ),

        camera_poses=(

            CameraPose(
                camera_id=CameraID.CAM01,
                x_mm=0.0,
                z_mm=320.0,
                image_name="CAM01_000017.jpg",
                capture_successful=True,
            ),

            CameraPose(
                camera_id=CameraID.CAM02,
                x_mm=250.0,
                z_mm=315.0,
                image_name="CAM02_000017.jpg",
                capture_successful=True,
            ),

            CameraPose(
                camera_id=CameraID.CAM03,
                x_mm=250.0,
                z_mm=150.0,
                image_name="CAM03_000017.jpg",
                capture_successful=True,
            ),

            CameraPose(
                camera_id=CameraID.CAM04,
                x_mm=250.0,
                z_mm=305.0,
                image_name="CAM04_000017.jpg",
                capture_successful=True,
            ),

            CameraPose(
                camera_id=CameraID.CAM05,
                x_mm=1200.0,
                z_mm=295.0,
                image_name="CAM05_000017.jpg",
                capture_successful=True,
            ),
        ),
    )


def test_serialize() -> None:
    """CaptureRecord serializes correctly."""

    serializer = CaptureRecordSerializer()

    data = serializer.serialize(
        create_capture_record(),
    )

    assert data["capture_index"] == 17
    assert data["target_position_mm"] == 250.0
    assert data["timestamp"] == TEST_TIME.isoformat()

    assert len(
        data["camera_poses"]
    ) == 5

    assert (
        data["scanner_pose"]["arm_x_mm"]
        == 250.0
    )


def test_deserialize() -> None:
    """CaptureRecord deserializes correctly."""

    serializer = CaptureRecordSerializer()

    original = create_capture_record()

    data = serializer.serialize(
        original,
    )

    restored = serializer.deserialize(
        data,
    )

    assert restored.capture_index == 17
    assert restored.target_position_mm == 250.0
    assert restored.timestamp == TEST_TIME

    assert (
        restored.scanner_pose.arm_x_mm
        == 250.0
    )

    assert (
        len(restored.camera_poses)
        == 5
    )

    assert (
        restored.camera_poses[0].camera_id
        == CameraID.CAM01
    )


def test_round_trip() -> None:
    """CaptureRecord survives a round trip."""

    serializer = CaptureRecordSerializer()

    original = create_capture_record()

    restored = serializer.deserialize(
        serializer.serialize(
            original,
        ),
    )

    assert restored == original


def test_timestamp_serialized_as_iso_string() -> None:
    """Timestamp is stored as an ISO-8601 string."""

    serializer = CaptureRecordSerializer()

    data = serializer.serialize(
        create_capture_record(),
    )

    assert isinstance(
        data["timestamp"],
        str,
    )

    assert (
        data["timestamp"]
        == TEST_TIME.isoformat()
    )

    def test_nested_objects_preserved() -> None:
        """Nested objects are preserved."""

        serializer = CaptureRecordSerializer()

        restored = serializer.deserialize(
            serializer.serialize(
                create_capture_record(),
            ),
        )

        assert (
            restored.scanner_pose
            == create_capture_record().scanner_pose
        )

        assert (
            restored.camera_poses
            == create_capture_record().camera_poses
        )