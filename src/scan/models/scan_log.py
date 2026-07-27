"""
Scan log.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime

from src.scan.models.capture_record import (
    CaptureRecord,
)
from src.scan.models.scan_configuration import (
    ScanConfiguration,
)


@dataclass(
    slots=True,
)
class ScanLog:
    """
    Complete log of a scan.
    """

    #
    # Configuration
    #

    configuration: ScanConfiguration

    #
    # Timing
    #

    start_time: datetime

    end_time: datetime | None = None

    #
    # Capture Records
    #

    captures: list[
        CaptureRecord
    ] = field(
        default_factory=list,
    )

    #
    # Properties
    #

    @property
    def capture_count(self) -> int:
        """
        Return the number of capture records.
        """

        return len(self.captures)

    @property
    def image_count(self) -> int:
        """
        Return the total number of images.
        """

        return sum(
            record.camera_count
            for record in self.captures
        )

    @property
    def successful_captures(self) -> int:
        """
        Return the number of successful capture positions.
        """

        return sum(
            record.successful
            for record in self.captures
        )

    @property
    def failed_captures(self) -> int:
        """
        Return the number of failed capture positions.
        """

        return (
            self.capture_count
            - self.successful_captures
        )

    @property
    def successful_images(self) -> int:
        """
        Return the number of successful images.
        """

        return sum(
            record.successful_captures
            for record in self.captures
        )

    @property
    def failed_images(self) -> int:
        """
        Return the number of failed images.
        """

        return sum(
            record.failed_captures
            for record in self.captures
        )

    @property
    def completed(self) -> bool:
        """
        Return True if the scan has completed.
        """

        return self.end_time is not None

    @property
    def duration_seconds(self) -> float:
        """
        Return the scan duration in seconds.
        """

        end = (
            self.end_time
            if self.end_time is not None
            else datetime.now()
        )

        return (
            end - self.start_time
        ).total_seconds()

    def add_capture(
        self,
        capture: CaptureRecord,
    ) -> None:
        """
        Add a capture record.
        """

        self.captures.append(
            capture,
        )