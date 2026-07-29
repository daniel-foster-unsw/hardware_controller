"""
Camera geometry.
"""

from dataclasses import dataclass

from src.scanner.enums.camera_id import CameraID


@dataclass(
    frozen=True,
    slots=True,
)
class CameraGeometry:
    """Physical configuration of a camera."""

    #
    # Identity
    #

    camera_id: CameraID

    camera_number: int

    #
    # Fixed Geometry
    #

    fixed_x_mm: float | None = None

    fixed_z_mm: float | None = None

    #
    # Motion
    #

    uses_arm_x: bool = False

    uses_vertical_motor: bool = False

    vertical_motor_id: int | None = None

    #
    # Calibration
    #

    x_offset_mm: float = 0.0

    z_offset_mm: float = 0.0