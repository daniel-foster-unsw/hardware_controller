"""
Generate scan positions.
"""

from __future__ import annotations

from collections.abc import Iterator

from src.scan.models.scan_configuration import (
    ScanConfiguration,
)


class PositionGenerator:
    """Immutable scan plan."""

    def __init__(
        self,
        configuration: ScanConfiguration,
    ) -> None:

        self._configuration = configuration

        self._positions = (
            self._generate_positions()
        )

    @property
    def positions(self) -> tuple[int, ...]:
        """Generated positions."""

        return self._positions

    @property
    def first(self) -> int:
        """First position."""

        return self._positions[0]

    @property
    def last(self) -> int:
        """Last position."""

        return self._positions[-1]

    def __len__(self) -> int:

        return len(self._positions)

    def __getitem__(
        self,
        index: int,
    ) -> int:

        return self._positions[index]

    def __iter__(
        self,
    ) -> Iterator[int]:

        return iter(self._positions)

    def _generate_positions(
        self,
    ) -> tuple[int, ...]:

        positions: list[int] = []

        position = (
            self._configuration.start_position_mm
        )

        while (
            position
            <= self._configuration.end_position_mm
        ):

            positions.append(position)

            position += (
                self._configuration.capture_spacing_mm
            )

        return tuple(
            positions,
        )