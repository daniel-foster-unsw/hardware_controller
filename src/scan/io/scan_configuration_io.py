"""
Scan configuration I/O.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from src.scan.models.scan_configuration import ScanConfiguration


class ScanConfigurationIO:
    """Read and write scan configuration files."""

    VERSION = 1

    @classmethod
    def save(
        cls,
        configuration: ScanConfiguration,
        path: Path,
    ) -> None:
        """
        Save a scan configuration.

        Args:
            configuration: Configuration to save.
            path: Destination JSON file.
        """

        data = asdict(configuration)

        #
        # JSON does not distinguish tuples.
        #

        data["enabled_cameras"] = list(
            configuration.enabled_cameras
        )

        data["version"] = cls.VERSION

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
            )

    @classmethod
    def load(
        cls,
        path: Path,
    ) -> ScanConfiguration:
        """
        Load a scan configuration.

        Args:
            path: JSON file.

        Returns:
            Scan configuration.
        """

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        version = data.pop("version")

        if version != cls.VERSION:

            raise ValueError(
                "Unsupported configuration version."
            )

        #
        # Restore tuple.
        #

        data["enabled_cameras"] = tuple(
            data["enabled_cameras"]
        )

        return ScanConfiguration(
            **data,
        )