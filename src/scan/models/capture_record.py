"""
Capture record.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.scanner.enums.camera_id import CameraID
from src.scanner.models.camera_pose import (
    CameraPose,
)
from src.scanner.models.scanner_pose import (
    ScannerPose,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CaptureRecord:
    """
    Record of a single capture position.
    """

    #
    # Identity
    #

    capture_index: int

    #
    # Planned Position
    #

    target_position_mm: float

    #
    # Capture Time
    #

    timestamp: datetime

    #
    # Actual Machine State
    #

    scanner_pose: ScannerPose

    #
    # Camera Results
    #

    camera_poses: tuple[
        CameraPose,
        ...
    ]

    #
    # Properties
    #

    @property
    def camera_count(self) -> int:
        """
        Return the number of cameras.
        """

        return len(self.camera_poses)

    @property
    def successful_captures(self) -> int:
        """
        Return the number of successful captures.
        """

        return sum(
            pose.capture_successful
            for pose in self.camera_poses
        )

    @property
    def failed_captures(self) -> int:
        """
        Return the number of failed captures.
        """

        return (
            self.camera_count
            - self.successful_captures
        )

    @property
    def successful(self) -> bool:
        """
        Return True if every camera captured successfully.
        """

        return (
            self.failed_captures == 0
        )

    @property
    def image_names(self) -> tuple[str, ...]:
        """
        Return all image names.
        """

        return tuple(
            pose.image_name
            for pose in self.camera_poses
        )

    @property
    def successful_camera_poses(
        self,
    ) -> tuple[
        CameraPose,
        ...
    ]:
        """
        Return successful camera captures.
        """

        return tuple(
            pose
            for pose in self.camera_poses
            if pose.capture_successful
        )

    @property
    def failed_camera_poses(
        self,
    ) -> tuple[
        CameraPose,
        ...
    ]:
        """
        Return failed camera captures.
        """

        return tuple(
            pose
            for pose in self.camera_poses
            if not pose.capture_successful
        )

    def camera(
        self,
        camera_id: CameraID,
    ) -> CameraPose:
        """
        Return the capture for a camera.

        Raises
        ------
        KeyError
            If the camera is not present.
        """

        for pose in self.camera_poses:

            if pose.camera_id == camera_id:

                return pose

        raise KeyError(
            f"{camera_id.name} not found."
        )