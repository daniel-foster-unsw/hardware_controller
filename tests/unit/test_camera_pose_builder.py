"""
Unit tests for CameraPoseBuilder.
"""

from src.scanner.builders.camera_pose_builder import (
    CameraPoseBuilder,
)
from src.scanner.enums.camera_id import CameraID
from src.scanner.factories.scanner_geometry_factory import (
    create_scanner_geometry,
)
from tests.helpers.scanner_pose_factory import (
    create_scanner_pose,
)


def test_build_camera_poses() -> None:
    """
    Camera poses can be built.
    """

    poses = CameraPoseBuilder.build(

        create_scanner_geometry(),

        create_scanner_pose(),

        capture_index=17,
    )

    assert len(poses) == 5


def test_camera_1_position() -> None:
    """
    Camera 1 uses fixed X.
    """

    poses = CameraPoseBuilder.build(

        create_scanner_geometry(),

        create_scanner_pose(),

        17,
    )

    camera = next(

        pose

        for pose in poses

        if pose.camera_id == CameraID.CAM01
    )

    assert camera.x_mm == 0.0

    assert camera.z_mm == 320.0


def test_camera_3_position() -> None:
    """
    Camera 3 uses arm X and fixed Z.
    """

    poses = CameraPoseBuilder.build(

        create_scanner_geometry(),

        create_scanner_pose(),

        17,
    )

    camera = next(

        pose

        for pose in poses

        if pose.camera_id == CameraID.CAM03
    )

    assert camera.x_mm == 250.0

    assert camera.z_mm == 0.0


def test_image_names() -> None:
    """
    Image names are generated correctly.
    """

    poses = CameraPoseBuilder.build(

        create_scanner_geometry(),

        create_scanner_pose(),

        17,
    )

    assert poses[0].image_name == (
        "CAM01_000017.jpg"
    )

    assert poses[4].image_name == (
        "CAM05_000017.jpg"
    )