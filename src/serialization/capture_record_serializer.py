"""
CaptureRecord serializer.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from src.scan.models.capture_record import CaptureRecord
from src.serialization.camera_pose_serializer import (
    CameraPoseSerializer,
)
from src.serialization.scanner_pose_serializer import (
    ScannerPoseSerializer,
)
from src.serialization.serializer import Serializer


class CaptureRecordSerializer(
    Serializer,
):
    """Serialize CaptureRecord objects."""

    def __init__(self) -> None:

        self._scanner_serializer = (
            ScannerPoseSerializer()
        )

        self._camera_serializer = (
            CameraPoseSerializer()
        )

    def serialize(
        self,
        obj: CaptureRecord,
    ) -> dict[str, Any]:
        """
        Convert CaptureRecord to dictionary.
        """

        return {

            "capture_index":
                obj.capture_index,

            "target_position_mm":
                obj.target_position_mm,

            "timestamp":
                obj.timestamp.isoformat(),

            "scanner_pose":
                self._scanner_serializer.serialize(
                    obj.scanner_pose,
                ),

            "camera_poses": [

                self._camera_serializer.serialize(
                    pose,
                )

                for pose in obj.camera_poses

            ],
        }

    def deserialize(
        self,
        data: dict[str, Any],
    ) -> CaptureRecord:
        """
        Convert dictionary into CaptureRecord.
        """

        return CaptureRecord(

            capture_index=data[
                "capture_index"
            ],

            target_position_mm=data[
                "target_position_mm"
            ],

            timestamp=datetime.fromisoformat(
                data["timestamp"],
            ),

            scanner_pose=(
                self._scanner_serializer.deserialize(
                    data["scanner_pose"],
                )
            ),

            camera_poses=tuple(

                self._camera_serializer.deserialize(
                    pose,
                )

                for pose in data[
                    "camera_poses"
                ]

            ),
        )