"""
Scan log IO.
"""

from __future__ import annotations

import json
from pathlib import Path

from src.scan.models.scan_log import (
    ScanLog,
)
from src.serialization.scan_log_serializer import (
    ScanLogSerializer,
)


class ScanLogIO:
    """Save and load ScanLog objects."""

    def __init__(self) -> None:

        self._serializer = (
            ScanLogSerializer()
        )

    def save(self, scan_log: ScanLog, path: Path,) -> None:
        """
        Save a ScanLog.
        """

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = self._serializer.serialize(
            scan_log,
        )

        with path.open("w", encoding="utf-8",) as file:

            json.dump(
                data,
                file,
                indent=4,
            )

    def load(self, path: Path,) -> ScanLog:
        """
        Load a ScanLog.
        """

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(
                file,
            )

        return self._serializer.deserialize(
            data,
        )