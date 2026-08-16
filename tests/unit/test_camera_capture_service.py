"""
Unit tests for CameraCaptureService.
"""

from unittest.mock import (
    MagicMock,
)

from src.camera.services.camera_capture_service import (
    CameraCaptureService,
)

from tests.helpers.scan_context_factory import (
    create_scan_context,
)


def create_client_factory(
    clients,
):
    """Create a camera client factory."""

    def factory(
        host,
        port,
    ):
        return clients[host]

    return factory


def create_clients():
    """Create mock camera clients."""

    clients = {}

    for number in range(1, 6):

        client = MagicMock()

        client.connect.return_value = None

        client.start_scan.return_value = {
            "status": "OK",
            "message": "Scan started.",
        }

        client.stop_scan.return_value = {
            "status": "OK",
            "message": "Scan stopped.",
        }

        client.capture_image.return_value = {
            "status": "OK",
            "message": "Image captured.",
            "data": {
                "filename":
                    f"CAM0{number}_000001.jpg",

                "filesize": 100,

                "width": 4056,

                "height": 3040,

                "format": "JPEG",
            },
        }

        clients[
            f"192.168.7.{10 + number}"
        ] = client

    return clients


def create_service(
    clients,
):
    """Create a service using mock clients."""

    hosts = {
        1: "192.168.7.11",
        2: "192.168.7.12",
        3: "192.168.7.13",
        4: "192.168.7.14",
        5: "192.168.7.15",
    }

    return CameraCaptureService(
        camera_hosts=hosts,
        client_factory=create_client_factory(
            clients,
        ),
    )


def test_initialise():
    """Service connects and starts enabled cameras."""

    service_clients = (
        create_clients()
    )

    service = create_service(
        service_clients,
    )

    context = create_scan_context()

    service.initialise(
        context,
    )

    assert service.initialised

    assert (
        service.camera_count
        == context.configuration.camera_count
    )

    for client in service_clients.values():

        client.connect.assert_called_once()

        client.start_scan.assert_called_once()


def test_capture_position():
    """Capture position returns a CaptureRecord."""

    service_clients = (
        create_clients()
    )

    service = create_service(
        service_clients,
    )

    context = create_scan_context()

    service.initialise(
        context,
    )

    record = service.capture_position(
        context,
    )

    assert (
        record.capture_index
        == 1
    )

    assert (
        record.camera_count
        == context.configuration.camera_count
    )

    assert (
        record.successful_captures
        == context.configuration.camera_count
    )

    assert record.successful

    assert (
        record.image_names
        == (
            "CAM01_000001.jpg",
            "CAM02_000001.jpg",
            "CAM03_000001.jpg",
            "CAM04_000001.jpg",
            "CAM05_000001.jpg",
        )
    )


def test_multiple_captures():
    """Multiple positions are captured."""

    service_clients = (
        create_clients()
    )

    service = create_service(
        service_clients,
    )

    context = create_scan_context()

    service.initialise(
        context,
    )

    first = service.capture_position(
        context,
    )

    second = service.capture_position(
        context,
    )

    assert (
        first.capture_index
        == 1
    )

    assert (
        second.capture_index
        == 2
    )

    for client in service_clients.values():

        assert (
            client.capture_image.call_count
            == 2
        )


def test_failed_camera_capture():
    """A failed camera is recorded as unsuccessful."""

    service_clients = (
        create_clients()
    )

    service_clients[
        "192.168.7.13"
    ].capture_image.return_value = {
        "status": "ERROR",
        "message": "Capture failed.",
        "data": None,
    }

    service = create_service(
        service_clients,
    )

    context = create_scan_context()

    service.initialise(
        context,
    )

    record = service.capture_position(
        context,
    )

    assert (
        record.camera_count
        == 5
    )

    assert (
        record.successful_captures
        == 4
    )

    assert (
        record.failed_captures
        == 1
    )

    assert not record.successful

    failed = record.failed_camera_poses

    assert len(failed) == 1

    assert (
        failed[0].image_name
        == ""
    )


def test_shutdown():
    """Shutdown stops and disconnects cameras."""

    service_clients = (
        create_clients()
    )

    service = create_service(
        service_clients,
    )

    context = create_scan_context()

    service.initialise(
        context,
    )

    service.shutdown(
        context,
    )

    assert not service.initialised

    assert (
        service.camera_count
        == 0
    )

    for client in service_clients.values():

        client.stop_scan.assert_called_once()

        client.disconnect.assert_called_once()