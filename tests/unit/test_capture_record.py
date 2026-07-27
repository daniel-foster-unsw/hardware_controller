"""
Unit tests for CaptureRecord.
"""

from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest

from src.scanner.enums.camera_id import CameraID
from src.scanner.models.camera_pose import CameraPose
from src.scanner.models.scanner_pose import ScannerPose
from src.scan.models.capture_record import (
    CaptureRecord,
)
# Fixed timestamp used by every test
TEST_TIMESTAMP = datetime(
    2026,
    1,
    1,
    12,
    0,
    0,
)



def create_record() -> CaptureRecord:
    """Create a capture record."""

    scanner_pose = ScannerPose(
        arm_x_mm=250.0,
        camera1_z_mm=320.0,
        camera2_z_mm=315.0,
        camera4_z_mm=305.0,
        camera5_z_mm=295.0,
    )

    cameras = (

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
    )

    return CaptureRecord(
        capture_index=17,
        target_position_mm=250.0,
        timestamp=datetime.now().replace(microsecond=0),
        scanner_pose=scanner_pose,
        camera_poses=cameras,
    )


def test_create_capture_record() -> None:

    record = create_record()

    assert record.capture_index == 17

    assert record.target_position_mm == 250.0

    assert len(record.camera_poses) == 5


def test_successful_capture_count() -> None:

    record = create_record()

    assert record.successful_captures == 5


def test_failed_capture_count() -> None:

    record = create_record()

    assert record.failed_captures == 0


def test_capture_success() -> None:

    assert create_record().successful


def test_image_names() -> None:

    record = create_record()

    assert record.image_names == (

        "CAM01_000017.jpg",

        "CAM02_000017.jpg",

        "CAM03_000017.jpg",

        "CAM04_000017.jpg",

        "CAM05_000017.jpg",
    )


def test_capture_record_is_frozen() -> None:

    record = create_record()

    with pytest.raises(FrozenInstanceError):

        record.capture_index = 10


def test_capture_record_hashable() -> None:
    """CaptureRecord is hashable."""
    record1 = create_record()
    record2 = create_record()

    records = {record1}

    assert record2 in records
    


    def test_camera_count() -> None:
        """Camera count is returned."""

        record = create_record()

        assert record.camera_count == 5


    def test_find_camera() -> None:
        """Camera lookup succeeds."""

        record = create_record()

        camera = record.camera(
            CameraID.CAM03,
        )

        assert camera.camera_id == CameraID.CAM03

        assert camera.image_name == "CAM03_000017.jpg"


    def test_successful_camera_poses() -> None:
        """Successful camera poses are returned."""

        record = create_record()

        assert (
            len(record.successful_camera_poses)
            == 5
        )

        assert (
            len(record.failed_camera_poses)
            == 0
        )