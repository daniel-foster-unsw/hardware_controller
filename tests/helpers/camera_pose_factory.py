"""
Shared CameraPose factory for tests.
"""

from src.scanner.enums.camera_id import CameraID
from src.scanner.models.camera_pose import (
    CameraPose,
)


def create_camera_pose(
    camera_id: CameraID = CameraID.CAM01,
) -> CameraPose:
    """
    Create a valid CameraPose.
    """

    positions = {

        CameraID.CAM01: (0.0, 320.0),

        CameraID.CAM02: (250.0, 315.0),

        CameraID.CAM03: (250.0, 150.0),

        CameraID.CAM04: (250.0, 305.0),

        CameraID.CAM05: (1200.0, 295.0),
    }

    x_mm, z_mm = positions[camera_id]

    return CameraPose(
        camera_id=camera_id,
        x_mm=x_mm,
        z_mm=z_mm,
        image_name=f"{camera_id.name}_000017.jpg",
        capture_successful=True,
    )