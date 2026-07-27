"""
Scan session.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime

from src.scan.generators.position_generator import (
    PositionGenerator,
)
from src.scan.models.scan_configuration import (
    ScanConfiguration,
)
from src.scan.models.scan_state import (
    ScanState,
)


@dataclass(slots=True)
class ScanSession:
    """Runtime state of a scan."""

    #
    # Configuration
    #

    configuration: ScanConfiguration

    #
    # Scan plan
    #

    position_generator: PositionGenerator = field(
        init=False,
    )

    #
    # Runtime state
    #

    state: ScanState = ScanState.IDLE

    current_position_index: int = 0

    downloaded_images: int = 0

    failed_images: int = 0

    #
    # Timing
    #

    start_time: datetime = field(
        default_factory=datetime.now,
    )

    end_time: datetime | None = None

    def __post_init__(self) -> None:
        """Create the scan plan."""

        self.position_generator = PositionGenerator(
            self.configuration,
        )

    #
    # Properties
    #

    @property
    def current_position_mm(self) -> int:
        """Return the current scan position."""

        return self.position_generator[
            self.current_position_index
        ]

    @property
    def total_positions(self) -> int:
        """Return the number of positions."""

        return len(
            self.position_generator,
        )

    @property
    def total_images(self) -> int:
        """Return the expected image count."""

        return (
            self.configuration.estimated_image_count
        )

    @property
    def progress(self) -> float:
        """Return scan progress."""

        if self.total_positions <= 1:
            return 0.0

        return (
            self.current_position_index
            / (self.total_positions - 1)
        )

    @property
    def completed(self) -> bool:
        """Return True if complete."""

        return (
            self.state
            == ScanState.COMPLETE
        )

    @property
    def duration(self) -> float:
        """Return elapsed time."""

        end = (
            self.end_time
            if self.end_time is not None
            else datetime.now()
        )

        return (
            end - self.start_time
        ).total_seconds()