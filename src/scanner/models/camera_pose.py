"""
Camera pose.
"""

from dataclasses import dataclass

from src.scanner.enums.camera_id import CameraID


@dataclass(
    frozen=True,
    slots=True,
)
class CameraPose:
    """
    Physical pose of a camera during image capture.
    """

    #
    # Camera
    #

    camera_id: CameraID

    #
    # Position
    #

    x_mm: float

    z_mm: float

    #
    # Image
    #

    image_name: str

    #
    # Capture
    #

    capture_successful: bool