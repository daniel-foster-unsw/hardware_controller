"""
ScanConfiguration serializer.
"""

from __future__ import annotations

from typing import Any

from src.scan.models.scan_configuration import (
    ScanConfiguration,
)
from src.serialization.serializer import (
    Serializer,
)


class ScanConfigurationSerializer(
    Serializer,
):
    """Serialize ScanConfiguration objects."""

    def serialize(
        self,
        obj: ScanConfiguration,
    ) -> dict[str, Any]:
        """
        Convert ScanConfiguration to a dictionary.
        """

        return {

            "scan_id":
                obj.scan_id,

            "scan_name":
                obj.scan_name,

            "start_position_mm":
                obj.start_position_mm,

            "end_position_mm":
                obj.end_position_mm,

            "capture_spacing_mm":
                obj.capture_spacing_mm,

            "motor_speed_mm_s":
                obj.motor_speed_mm_s,

            "capture_delay_s":
                obj.capture_delay_s,

            "enabled_cameras":
                list(
                    obj.enabled_cameras
                ),

            "reset_before_scan":
                obj.reset_before_scan,

            "reset_after_scan":
                obj.reset_after_scan,

            "auto_download":
                obj.auto_download,

            "delete_remote_files":
                obj.delete_remote_files,
        }

    def deserialize(
        self,
        data: dict[str, Any],
    ) -> ScanConfiguration:
        """
        Convert dictionary into ScanConfiguration.
        """

        return ScanConfiguration(

            scan_id=data["scan_id"],

            scan_name=data["scan_name"],

            start_position_mm=data[
                "start_position_mm"
            ],

            end_position_mm=data[
                "end_position_mm"
            ],

            capture_spacing_mm=data[
                "capture_spacing_mm"
            ],

            motor_speed_mm_s=data[
                "motor_speed_mm_s"
            ],

            capture_delay_s=data[
                "capture_delay_s"
            ],

            enabled_cameras=tuple(
                data["enabled_cameras"]
            ),

            reset_before_scan=data[
                "reset_before_scan"
            ],

            reset_after_scan=data[
                "reset_after_scan"
            ],

            auto_download=data[
                "auto_download"
            ],

            delete_remote_files=data[
                "delete_remote_files"
            ],
        )