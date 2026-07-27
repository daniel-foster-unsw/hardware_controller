"""
Scanner pose.
"""

from dataclasses import dataclass


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

    camera1_z_mm: floatW

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