"""
Scanner geometry.
"""

from dataclasses import dataclass

from src.scanner.enums.camera_id import CameraID
from src.scanner.models.camera_geometry import (
    CameraGeometry,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ScannerGeometry:
    """Complete scanner geometry."""

    cameras: tuple[
        CameraGeometry,
        ...
    ]

    @property
    def camera_count(self) -> int:
        """Return the number of cameras."""

        return len(self.cameras)

    def camera(
        self,
        camera_id: CameraID,
    ) -> CameraGeometry:
        """
        Return a camera definition.
        """

        for camera in self.cameras:

            if camera.camera_id == camera_id:

                return camera

        raise KeyError(
            f"{camera_id.name} not found."
        )