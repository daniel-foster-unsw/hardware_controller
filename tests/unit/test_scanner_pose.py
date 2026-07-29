"""
Unit tests for ScannerPose.
"""

from dataclasses import FrozenInstanceError

import pytest

from src.scanner.models.scanner_pose import (
    ScannerPose,
)

from src.scanner.enums.camera_id import CameraID


def create_scanner_pose() -> ScannerPose:
    """
    Create a scanner pose.
    """

    return ScannerPose(
        arm_x_mm=250.0,
        camera1_z_mm=320.0,
        camera2_z_mm=315.0,
        camera4_z_mm=305.0,
        camera5_z_mm=295.0,
    )


def test_create_scanner_pose() -> None:
    """
    Scanner pose can be created.
    """

    pose = create_scanner_pose()

    assert pose.arm_x_mm == 250.0

    assert pose.camera1_z_mm == 320.0

    assert pose.camera2_z_mm == 315.0

    assert pose.camera4_z_mm == 305.0

    assert pose.camera5_z_mm == 295.0


def test_vertical_positions() -> None:
    """
    Vertical positions are returned.
    """

    pose = create_scanner_pose()

    assert pose.vertical_positions == (
        320.0,
        315.0,
        305.0,
        295.0,
    )


def test_average_vertical_position() -> None:
    """
    Average camera height is calculated.
    """

    pose = create_scanner_pose()

    assert pose.average_vertical_position == 308.75


def test_pose_is_frozen() -> None:
    """
    Scanner pose is immutable.
    """

    pose = create_scanner_pose()

    with pytest.raises(FrozenInstanceError):

        pose.arm_x_mm = 100.0


def test_pose_equality() -> None:
    """
    Equal poses compare equal.
    """

    assert (
        create_scanner_pose()
        == create_scanner_pose()
    )


def test_pose_is_hashable() -> None:
    """
    Scanner pose is hashable.
    """

    poses = {
        create_scanner_pose(),
    }

    assert (
        create_scanner_pose()
        in poses
    )


    def test_camera_z_position() -> None:
        """
        Camera Z positions can be queried.
        """

        pose = create_scanner_pose()

        assert (
            pose.camera_z_position(
                CameraID.CAM01,
            )
            == 320.0
        )

        assert (
            pose.camera_z_position(
                CameraID.CAM02,
            )
            == 315.0
        )

        assert (
            pose.camera_z_position(
                CameraID.CAM04,
            )
            == 305.0
        )

        assert (
            pose.camera_z_position(
                CameraID.CAM05,
            )
            == 295.0
        )


    def test_camera3_has_no_vertical_axis() -> None:
        """
        Camera 3 does not have a movable vertical axis.
        """

        pose = create_scanner_pose()

        with pytest.raises(KeyError):

            pose.camera_z_position(
                CameraID.CAM03,
            )