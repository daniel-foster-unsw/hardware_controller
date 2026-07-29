"""
Unit tests for MockDownloadService.
"""

from src.camera.services.mock_download_service import (
    MockDownloadService,
)
from tests.helpers.capture_record_factory import (
    create_capture_record,
)
from tests.helpers.scan_context_factory import (
    create_scan_context,
)


def test_download() -> None:
    """
    Images are downloaded.
    """

    service = MockDownloadService()

    context = create_scan_context()

    context.add_capture(
        create_capture_record(),
    )

    service.download(
        context,
    )

    assert service.downloaded

    assert service.download_count == 5


def test_delete_remote() -> None:
    """
    Remote delete completes.
    """

    service = MockDownloadService()

    service.delete_remote(
        create_scan_context(),
    )