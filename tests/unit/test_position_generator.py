"""
Unit tests for PositionGenerator.
"""

from src.scan.generators.position_generator import (
    PositionGenerator,
)
from tests.helpers.configuration_factory import (
    create_scan_configuration,
)


def test_generate_positions() -> None:
    """Positions are generated."""

    generator = PositionGenerator(
        create_scan_configuration(),
    )

    assert len(generator) == 21


def test_first_position() -> None:
    """First position."""

    generator = PositionGenerator(
        create_scan_configuration(),
    )

    assert generator[0] == 0


def test_last_position() -> None:
    """Last position."""

    generator = PositionGenerator(
        create_scan_configuration(),
    )

    assert generator[-1] == 1000


def test_position_spacing() -> None:
    """Spacing is correct."""

    generator = PositionGenerator(
        create_scan_configuration(),
    )

    assert generator[5] == 250


def test_iteration() -> None:
    """Generator is iterable."""

    generator = PositionGenerator(
        create_scan_configuration(),
    )

    positions = list(generator)

    assert positions == list(generator.positions)


def test_positions_property() -> None:
    """Positions are immutable."""

    generator = PositionGenerator(
        create_scan_configuration(),
    )

    assert isinstance(
        generator.positions,
        tuple,
    )


def test_position_count_matches_configuration() -> None:
    """Position count matches configuration."""

    configuration = create_scan_configuration()

    generator = PositionGenerator(
        configuration,
    )

    assert (
        len(generator)
        == configuration.capture_count
    )