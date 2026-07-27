"""
Unit tests for ScanLogIO.
"""

from pathlib import Path

from src.scan.io.scan_log_io import (
    ScanLogIO,
)
from tests.helpers.scan_log_factory import (
    create_scan_log,
)


def test_save_scan_log(
    tmp_path: Path,
) -> None:
    """ScanLog is saved."""

    io = ScanLogIO()

    path = tmp_path / "scan.json"

    io.save(
        create_scan_log(),
        path,
    )

    assert path.exists()


def test_save_creates_directory(
    tmp_path: Path,
) -> None:
    """Directories are created automatically."""

    io = ScanLogIO()

    path = (
        tmp_path
        / "logs"
        / "scan.json"
    )

    io.save(
        create_scan_log(),
        path,
    )

    assert path.exists()