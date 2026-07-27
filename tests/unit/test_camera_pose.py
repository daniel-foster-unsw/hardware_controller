"""
Unit tests for CameraPose.
"""

from dataclasses import FrozenInstanceError

import pytest

from src.scanner.enums.camera_id import CameraID
from src.scanner.models.camera_pose import CameraPose


def create_camera_pose() -> CameraPose:
    """
    Create a camera pose.
    """

    return CameraPose(
        camera_id=CameraID.CAM02,
        x_mm=250.0,
        z_mm=315.0,
        image_name="CAM02_000017.jpg",
        capture_successful=True,
    )


def test_create_camera_pose() -> None:
    """
    Camera pose can be created.
    """

    pose = create_camera_pose()

    assert pose.camera_id == CameraID.CAM02

    assert pose.x_mm == 250.0

    assert pose.z_mm == 315.0

    assert pose.image_name == "CAM02_000017.jpg"

    assert pose.capture_successful


def test_camera_pose_is_frozen() -> None:
    """
    Camera pose is immutable.
    """

    pose = create_camera_pose()

    with pytest.raises(FrozenInstanceError):

        pose.image_name = "new.jpg"


def test_camera_pose_equality() -> None:
    """
    Equal camera poses compare equal.
    """

    assert (
        create_camera_pose()
        == create_camera_pose()
    )


def test_camera_pose_is_hashable() -> None:
    """
    Camera pose is hashable.
    """

    poses = {
        create_camera_pose(),
    }

    assert create_camera_pose() in poses