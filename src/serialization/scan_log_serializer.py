"""
ScanLog serializer.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from src.scan.models.scan_log import ScanLog
from src.serialization.capture_record_serializer import (
    CaptureRecordSerializer,
)
from src.serialization.scan_configuration_serializer import (
    ScanConfigurationSerializer,
)
from src.serialization.serializer import Serializer


class ScanLogSerializer(
    Serializer,
):
    """Serialize ScanLog objects."""

    VERSION = 1

    def __init__(self) -> None:

        self._configuration_serializer = (
            ScanConfigurationSerializer()
        )

        self._capture_serializer = (
            CaptureRecordSerializer()
        )

    def serialize(
        self,
        obj: ScanLog,
    ) -> dict[str, Any]:
        """
        Convert ScanLog to a dictionary.
        """

        return {

            "version": self.VERSION,

            "configuration":
                self._configuration_serializer.serialize(
                    obj.configuration,
                ),

            "start_time":
                obj.start_time.isoformat(),

            "end_time":
                (
                    obj.end_time.isoformat()
                    if obj.end_time is not None
                    else None
                ),

            "captures": [

                self._capture_serializer.serialize(
                    capture,
                )

                for capture in obj.captures

            ],
        }

    def deserialize(
        self,
        data: dict[str, Any],
    ) -> ScanLog:
        """
        Convert dictionary into ScanLog.
        """

        return ScanLog(

            configuration=(
                self._configuration_serializer.deserialize(
                    data["configuration"],
                )
            ),

            start_time=datetime.fromisoformat(
                data["start_time"],
            ),

            end_time=(
                datetime.fromisoformat(
                    data["end_time"],
                )
                if data["end_time"] is not None
                else None
            ),

            captures=[

                self._capture_serializer.deserialize(
                    capture,
                )

                for capture in data[
                    "captures"
                ]

            ],
        )