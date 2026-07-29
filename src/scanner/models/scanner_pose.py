"""
Scanner pose.
"""

from dataclasses import dataclass

from src.scanner.enums.camera_id import CameraID


@dataclass(
    frozen=True,
    slots=True,
)
class ScannerPose:
    """
    Physical pose of the scanner.
    """

    #
    # Horizontal
    #

    arm_x_mm: float

    #
    # Vertical
    #

    camera1_z_mm: float

    camera2_z_mm: float

    camera4_z_mm: float

    camera5_z_mm: float

    @property
    def vertical_positions(self) -> tuple[float, ...]:
        """
        Return all movable camera heights.
        """

        return (
            self.camera1_z_mm,
            self.camera2_z_mm,
            self.camera4_z_mm,
            self.camera5_z_mm,
        )

    @property
    def average_vertical_position(self) -> float:
        """
        Return the average camera height.
        """

        return (
            sum(self.vertical_positions)
            / len(self.vertical_positions)
        )

    def camera_z_position(
        self,
        camera_id: CameraID,
    ) -> float:
        """
        Return the Z position for the specified camera.

        Raises:
            KeyError: If the camera does not have a movable
                vertical axis.
        """

        lookup = {

            CameraID.CAM01:
                self.camera1_z_mm,

            CameraID.CAM02:
                self.camera2_z_mm,

            CameraID.CAM04:
                self.camera4_z_mm,

            CameraID.CAM05:
                self.camera5_z_mm,
        }

        try:

            return lookup[camera_id]

        except KeyError as error:

            raise KeyError(
                f"{camera_id.name} does not have a movable vertical axis."
            ) from error