"""
ScannerPose serializer.
"""

from __future__ import annotations

from typing import Any

from src.scanner.models.scanner_pose import ScannerPose
from src.serialization.serializer import Serializer


class ScannerPoseSerializer(
    Serializer,
):
    """Serialize ScannerPose objects."""

    def serialize(
        self,
        obj: ScannerPose,
    ) -> dict[str, Any]:
        """
        Convert ScannerPose to dictionary.
        """

        return {
            "arm_x_mm": obj.arm_x_mm,
            "camera1_z_mm": obj.camera1_z_mm,
            "camera2_z_mm": obj.camera2_z_mm,
            "camera4_z_mm": obj.camera4_z_mm,
            "camera5_z_mm": obj.camera5_z_mm,
        }

    def deserialize(
        self,
        data: dict[str, Any],
    ) -> ScannerPose:
        """
        Convert dictionary into ScannerPose.
        """

        return ScannerPose(
            arm_x_mm=data["arm_x_mm"],
            camera1_z_mm=data[
                "camera1_z_mm"
            ],
            camera2_z_mm=data[
                "camera2_z_mm"
            ],
            camera4_z_mm=data[
                "camera4_z_mm"
            ],
            camera5_z_mm=data[
                "camera5_z_mm"
            ],
        )