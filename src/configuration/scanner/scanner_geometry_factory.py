"""
Scanner geometry factory.
"""

from src.scanner.enums.camera_id import CameraID
from src.configuration.scanner.camera_geometry import (
    CameraGeometry,
)
from src.configuration.scanner.scanner_geometry import (
    ScannerGeometry,
)


def create_scanner_geometry() -> ScannerGeometry:
    """
    Create the default scanner geometry.
    """

    return ScannerGeometry(

        cameras=(

            #
            # CAM01
            #

            CameraGeometry(
                camera_id=CameraID.CAM01,
                camera_number=1,
                fixed_x_mm=0.0,
                uses_vertical_motor=True,
                vertical_motor_id=1,
            ),

            #
            # CAM02
            #

            CameraGeometry(
                camera_id=CameraID.CAM02,
                camera_number=2,
                uses_arm_x=True,
                uses_vertical_motor=True,
                vertical_motor_id=2,
            ),

            #
            # CAM03
            #

            CameraGeometry(
                camera_id=CameraID.CAM03,
                camera_number=3,
                uses_arm_x=True,
                fixed_z_mm=0.0,
            ),

            #
            # CAM04
            #

            CameraGeometry(
                camera_id=CameraID.CAM04,
                camera_number=4,
                uses_arm_x=True,
                uses_vertical_motor=True,
                vertical_motor_id=3,
            ),

            #
            # CAM05
            #

            CameraGeometry(
                camera_id=CameraID.CAM05,
                camera_number=5,
                fixed_x_mm=1200.0,
                uses_vertical_motor=True,
                vertical_motor_id=4,
            ),
        ),
    )