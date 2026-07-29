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
    Build CameraPose objects from the scanner geometry and
    current scanner pose.
    """

    @staticmethod
    def build(
        geometry: ScannerGeometry,
        scanner_pose: ScannerPose,
        capture_index: int,
    ) -> tuple[CameraPose, ...]:
        """
        Build the camera poses for one capture.
        """

        return tuple(

            CameraPose(

                camera_id=camera.camera_id,

                x_mm=CameraPoseBuilder._build_x_position(
                    camera,
                    scanner_pose,
                ),

                z_mm=CameraPoseBuilder._build_z_position(
                    camera,
                    scanner_pose,
                ),

                image_name=(
                    f"{camera.camera_id.name}"
                    f"_{capture_index:06d}.jpg"
                ),

                capture_successful=True,

            )

            for camera in geometry.cameras
        )

    @staticmethod
    def _build_x_position(
        camera: CameraGeometry,
        scanner_pose: ScannerPose,
    ) -> float:
        """
        Calculate camera X position.
        """

        if camera.uses_arm_x:

            return scanner_pose.arm_x_mm

        return camera.fixed_x_mm or 0.0

    @staticmethod
    def _build_z_position(
        camera: CameraGeometry,
        scanner_pose: ScannerPose,
    ) -> float:
        """
        Calculate camera Z position.
        """

        if camera.fixed_z_mm is not None:

            return camera.fixed_z_mm

        return scanner_pose.camera_z_position(
            camera.camera_id,
        )