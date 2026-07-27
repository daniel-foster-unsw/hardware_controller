"""
Shared CaptureRecord factory for tests.
"""

from datetime import datetime

from src.scanner.enums.camera_id import CameraID
from src.scan.models.capture_record import (
    CaptureRecord,
)

from tests.helpers.camera_pose_factory import (
    create_camera_pose,
)
from tests.helpers.scanner_pose_factory import (
    create_scanner_pose,
)


def create_capture_record() -> CaptureRecord:
    """
    Create a valid CaptureRecord.
    """

    return CaptureRecord(
        capture_index=17,
        target_position_mm=250.0,
        timestamp=datetime.now(),
        scanner_pose=create_scanner_pose(),
        camera_poses=(

            create_camera_pose(
                CameraID.CAM01,
            ),

            create_camera_pose(
                CameraID.CAM02,
            ),

            create_camera_pose(
                CameraID.CAM03,
            ),

            create_camera_pose(
                CameraID.CAM04,
            ),

            create_camera_pose(
                CameraID.CAM05,
            ),
        ),
    )