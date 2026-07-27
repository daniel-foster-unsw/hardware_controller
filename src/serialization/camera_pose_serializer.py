"""
CameraPose serializer.
"""

from __future__ import annotations

from typing import Any

from src.scanner.enums.camera_id import CameraID
from src.scanner.models.camera_pose import CameraPose
from src.serialization.serializer import Serializer


class CameraPoseSerializer(
    Serializer,
):
    """Serialize CameraPose objects."""

    def serialize(
        self,
        obj: CameraPose,
    ) -> dict[str, Any]:
        """
        Convert CameraPose to a dictionary.
        """

        return {
            "camera_id": obj.camera_id.value,
            "x_mm": obj.x_mm,
            "z_mm": obj.z_mm,
            "image_name": obj.image_name,
            "capture_successful": obj.capture_successful,
        }

    def deserialize(
        self,
        data: dict[str, Any],
    ) -> CameraPose:
        """
        Convert dictionary into CameraPose.
        """

        return CameraPose(
            camera_id=CameraID(
                data["camera_id"],
            ),
            x_mm=data["x_mm"],
            z_mm=data["z_mm"],
            image_name=data["image_name"],
            capture_successful=data[
                "capture_successful"
            ],
        )