"""
Mock capture service.
"""



from __future__ import annotations

from src.scanner.models.scanner_pose import (
    ScannerPose,
)

from datetime import datetime

from src.camera.services.capture_service import (
    CaptureService,
)
from src.scan.models.capture_record import (
    CaptureRecord,
)
from src.scan.models.scan_context import (
    ScanContext,
)
from src.scanner.builders.camera_pose_builder import (
    CameraPoseBuilder,
)




class MockCaptureService(CaptureService):
    """
    Mock implementation of CaptureService.
    """

    def __init__(self) -> None:

        self._initialised = False

        self._capture_index = 0

        self._captures: list[CaptureRecord] = []

    @property
    def initialised(self) -> bool:
        """Return whether the service is initialised."""

        return self._initialised

    @property
    def capture_count(self) -> int:
        """Return the number of captures."""

        return len(self._captures)

    @property
    def captures(self) -> tuple[CaptureRecord, ...]:
        """Return all capture records."""

        return tuple(self._captures)

    def initialise(
        self,
        context: ScanContext,
    ) -> None:

        self._initialised = True

        self._capture_index = 0

        self._captures.clear()





    def capture_position(
        self,
        context: ScanContext,
    ) -> CaptureRecord:
        """
        Capture a scan position.
        """

        self._capture_index += 1

        scanner_pose = ScannerPose(
            arm_x_mm=float(self._capture_index * 50),
            camera1_z_mm=320.0,
            camera2_z_mm=315.0,
            camera4_z_mm=305.0,
            camera5_z_mm=295.0,
        )

        camera_poses = CameraPoseBuilder.build(
            geometry=context.geometry,
            scanner_pose=scanner_pose,
            capture_index=self._capture_index,
        )

        record = CaptureRecord(
            capture_index=self._capture_index,
            target_position_mm=scanner_pose.arm_x_mm,
            timestamp=datetime.now(),
            scanner_pose=scanner_pose,
            camera_poses=camera_poses,
        )

        self._captures.append(
            record,
        )

        return record    
    """
    def capture_position(
        self,
        context: ScanContext,
    ) -> CaptureRecord:

        self._capture_index += 1

        scanner_pose = context.scanner_pose

        camera_poses = CameraPoseBuilder.build(
            geometry=context.geometry,
            scanner_pose=scanner_pose,
            capture_index=self._capture_index,
        )

        record = CaptureRecord(
            capture_index=self._capture_index,
            target_position_mm=scanner_pose.arm_x_mm,
            timestamp=datetime.now(),
            scanner_pose=scanner_pose,
            camera_poses=camera_poses,
        )

        self._captures.append(record)

        return record
    """
    def shutdown(
        self,
        context: ScanContext,
    ) -> None:

        self._initialised = False



    @property
    def image_count(self) -> int:
        """
        Return the number of captured images.
        """

        return sum(

            capture.camera_count

            for capture

            in self._captures

        )