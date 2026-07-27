"""
Unit tests for ScanLogSerializer.
"""

from src.serialization.scan_log_serializer import (
    ScanLogSerializer,
)
from tests.helpers.scan_log_factory import (
    create_scan_log,
)


def test_serialize_scan_log() -> None:
    """ScanLog serializes correctly."""

    serializer = ScanLogSerializer()

    data = serializer.serialize(
        create_scan_log(),
    )

    assert data["version"] == 1

    assert "configuration" in data

    assert "captures" in data

    assert isinstance(
        data["captures"],
        list,
    )

def test_round_trip():

    serializer = ScanLogSerializer()

    original = create_scan_log()

    restored = serializer.deserialize(
        serializer.serialize(
            original,
        ),
    )

    assert restored == original


def test_version_written():
    serializer = ScanLogSerializer()

    data = serializer.serialize(
        create_scan_log(),
    )

    assert data["version"] == 1