"""
Camera pose builder.
"""

from __future__ import annotations

from src.scanner.enums.camera_id import CameraID
from src.scanner.models.camera_geometry import CameraGeometry
from src.scanner.models.camera_pose import CameraPose
from src.scanner.models.scanner_geometry import ScannerGeometry
from src.scanner.models.scanner_pose import ScannerPose


class CameraPoseBuilder:
    """
    Build CameraPose objects from scanner state.
    """

    @staticmethod
    def build(
        geometry: ScannerGeometry,
        scanner_pose: ScannerPose,
        capture_index: int,
    ) -> tuple[
        CameraPose,
        ...
    ]:

        poses: list[CameraPose] = []

        for camera in geometry.cameras:

            poses.append(

                CameraPose(

                    camera_id=camera.camera_id,

                    x_mm=CameraPoseBuilder._x_position(
                        camera,
                        scanner_pose,
                    ),

                    z_mm=CameraPoseBuilder._z_position(
                        camera,
                        scanner_pose,
                    ),

                    image_name=(
                        f"{camera.camera_id.name}"
                        f"_{capture_index:06d}.jpg"
                    ),

                    capture_successful=True,
                )
            )

        return tuple(poses)


    @staticmethod
    def _x_position(
        camera: CameraGeometry,
        pose: ScannerPose,
    ) -> float:

        if camera.uses_arm_x:

            return pose.arm_x_mm

        return camera.fixed_x_mm or 0.0


    @staticmethod
    def _z_position(
        camera: CameraGeometry,
        pose: ScannerPose,
    ) -> float:

        if camera.fixed_z_mm is not None:

            return camera.fixed_z_mm

        return {

            CameraID.CAM01: pose.camera1_z_mm,

            CameraID.CAM02: pose.camera2_z_mm,

            CameraID.CAM04: pose.camera4_z_mm,

            CameraID.CAM05: pose.camera5_z_mm,

        }.get(
            camera.camera_id,
            0.0,
        )