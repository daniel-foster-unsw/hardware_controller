"""
Unit tests for ScanRunner.
"""

from src.scan.engine.scan_runner import (
    ScanRunner,
)

from tests.helpers.scan_engine_factory import (
    create_scan_engine,
)


def test_runner_executes_scan() -> None:
    """
    Runner executes the complete scan workflow.
    """

    fixture = create_scan_engine()

    runner = ScanRunner()

    runner.run(
        context=fixture.context,
        motion=fixture.motion,
        capture=fixture.capture,
        download=fixture.download,
    )

    assert fixture.motion.homed is True

    assert (
        len(fixture.motion.visited_positions)
        == fixture.context.session.total_positions
    )


def test_runner_visits_expected_positions() -> None:
    """
    Runner visits every generated scan position.
    """

    fixture = create_scan_engine()

    runner = ScanRunner()

    runner.run(
        context=fixture.context,
        motion=fixture.motion,
        capture=fixture.capture,
        download=fixture.download,
    )

    expected_positions = tuple(
        fixture.context.session.position_generator
    )

    assert (
        fixture.motion.visited_positions
        == expected_positions
    )


def test_runner_creates_capture_for_each_position() -> None:
    """
    Runner records one capture at each scan position.
    """

    fixture = create_scan_engine()

    runner = ScanRunner()

    runner.run(
        context=fixture.context,
        motion=fixture.motion,
        capture=fixture.capture,
        download=fixture.download,
    )

    assert (
        fixture.context.log.capture_count
        == fixture.context.session.total_positions
    )


def test_runner_shuts_down_motion() -> None:
    """
    Runner shuts down motion after the scan.
    """

    fixture = create_scan_engine()

    runner = ScanRunner()

    runner.run(
        context=fixture.context,
        motion=fixture.motion,
        capture=fixture.capture,
        download=fixture.download,
    )

    assert fixture.motion.initialised is False