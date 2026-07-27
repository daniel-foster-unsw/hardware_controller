"""
Unit tests for ScanConfigurationIO.
"""

import json
from pathlib import Path

import pytest

from src.scan.io.scan_configuration_io import (
    ScanConfigurationIO,
)
from tests.helpers.configuration_factory import (
    create_scan_configuration,
)


def test_save_configuration(
    tmp_path: Path,
) -> None:
    """
    Configuration is written to disk.
    """

    configuration = create_scan_configuration()

    path = tmp_path / "scan.json"

    ScanConfigurationIO.save(
        configuration,
        path,
    )

    assert path.exists()


def test_load_configuration(
    tmp_path: Path,
) -> None:
    """
    Configuration can be saved and loaded.
    """

    configuration = create_scan_configuration()

    path = tmp_path / "scan.json"

    ScanConfigurationIO.save(
        configuration,
        path,
    )

    loaded = ScanConfigurationIO.load(
        path,
    )

    assert loaded == configuration


def test_version_mismatch(
    tmp_path: Path,
) -> None:
    """
    Unsupported configuration versions are rejected.
    """

    path = tmp_path / "scan.json"

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            {
                "version": 999,
            },
            file,
        )

    with pytest.raises(ValueError):

        ScanConfigurationIO.load(
            path,
        )


def test_parent_directory_created(
    tmp_path: Path,
) -> None:
    """
    Parent directories are created automatically.
    """

    configuration = create_scan_configuration()

    path = (
        tmp_path
        / "configs"
        / "scan"
        / "scan.json"
    )

    ScanConfigurationIO.save(
        configuration,
        path,
    )

    assert path.exists()


def test_enabled_cameras_restored_as_tuple(
    tmp_path: Path,
) -> None:
    """
    Camera IDs are restored as a tuple.
    """

    configuration = create_scan_configuration()

    path = tmp_path / "scan.json"

    ScanConfigurationIO.save(
        configuration,
        path,
    )

    loaded = ScanConfigurationIO.load(
        path,
    )

    assert isinstance(
        loaded.enabled_cameras,
        tuple,
    )


def test_json_contains_version(
    tmp_path: Path,
) -> None:
    """
    Saved configuration includes the schema version.
    """

    configuration = create_scan_configuration()

    path = tmp_path / "scan.json"

    ScanConfigurationIO.save(
        configuration,
        path,
    )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    assert data["version"] == (
        ScanConfigurationIO.VERSION
    )


def test_json_stores_camera_ids_as_list(
    tmp_path: Path,
) -> None:
    """
    Camera IDs are stored as a JSON list.
    """

    configuration = create_scan_configuration()

    path = tmp_path / "scan.json"

    ScanConfigurationIO.save(
        configuration,
        path,
    )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    assert isinstance(
        data["enabled_cameras"],
        list,
    )