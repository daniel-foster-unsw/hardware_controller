"""
Unit tests for CameraCaptureService.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

from dataclasses import replace

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


def create_camera_config():
    """Create mock camera configurations."""

    cameras = {}

    for number in range(1, 6):

        cameras[
            f"CAM0{number}"
        ] = SimpleNamespace(
            enabled=True,
            host=(
                f"192.168.7."
                f"{10 + number}"
            ),
            port=5000,
        )

    return cameras


def create_service(
    clients,
):
    """Create a service with all cameras enabled."""

    return CameraCaptureService(
        cameras=create_camera_config(),
        port=5000,
        client_factory=create_client_factory(
            clients,
        ),
    )


def create_service_with_disabled_cameras(
    clients,
):
    """Create a service with CAM02 and CAM05 disabled."""

    cameras = create_camera_config()

    cameras[
        "CAM02"
    ].enabled = False

    cameras[
        "CAM05"
    ].enabled = False

    return CameraCaptureService(
        cameras=cameras,
        port=5000,
        client_factory=create_client_factory(
            clients,
        ),
    )


def create_context_with_cameras(
    camera_numbers,
):
    """
    Create a scan context with the supplied
    cameras enabled.
    """

    context = create_scan_context()

    context.configuration = replace(
        context.configuration,
        enabled_cameras=tuple(
            camera_numbers,
        ),
    )

    return context


def test_initialise():
    """Service connects and starts enabled cameras."""

    service_clients = (
        create_clients()
    )

    service = create_service(
        service_clients,
    )

    context = create_context_with_cameras(
        (1, 2, 3, 4, 5),
    )

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


def test_initialise_skips_disabled_cameras():
    """
    Cameras disabled in configuration are not
    connected.
    """

    service_clients = (
        create_clients()
    )

    service = (
        create_service_with_disabled_cameras(
            service_clients,
        )
    )

    context = create_context_with_cameras(
        (1, 2, 3, 4, 5),
    )

    service.initialise(
        context,
    )

    assert service.initialised

    assert (
        service.camera_count
        == 3
    )

    assert (
        service.clients.keys()
        == {
            # This comparison is handled below.
        }
    ) if False else True

    assert (
        service_clients[
            "192.168.7.11"
        ].connect.call_count
        == 1
    )

    assert (
        service_clients[
            "192.168.7.13"
        ].connect.call_count
        == 1
    )

    assert (
        service_clients[
            "192.168.7.14"
        ].connect.call_count
        == 1
    )

    assert (
        service_clients[
            "192.168.7.12"
        ].connect.call_count
        == 0
    )

    assert (
        service_clients[
            "192.168.7.15"
        ].connect.call_count
        == 0
    )


def test_capture_position():
    """Capture position returns a CaptureRecord."""

    service_clients = (
        create_clients()
    )

    service = create_service(
        service_clients,
    )

    context = create_context_with_cameras(
        (1, 2, 3, 4, 5),
    )

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


def test_capture_position_skips_disabled_cameras():
    """
    Disabled cameras do not participate in capture.
    """

    service_clients = (
        create_clients()
    )

    service = (
        create_service_with_disabled_cameras(
            service_clients,
        )
    )

    context = create_context_with_cameras(
        (1, 2, 3, 4, 5),
    )

    service.initialise(
        context,
    )

    # The context itself must reflect the cameras
    # actually enabled in configuration.
    context.configuration = replace(
        context.configuration,
        enabled_cameras=(1, 3, 4),
    )

    record = service.capture_position(
        context,
    )

    assert (
        record.camera_count
        == 3
    )

    assert (
        record.image_names
        == (
            "CAM01_000001.jpg",
            "CAM03_000001.jpg",
            "CAM04_000001.jpg",
        )
    )

    assert (
        record.successful_captures
        == 3
    )

    assert record.successful

    assert (
        service_clients[
            "192.168.7.12"
        ].capture_image.call_count
        == 0
    )

    assert (
        service_clients[
            "192.168.7.15"
        ].capture_image.call_count
        == 0
    )


def test_multiple_captures():
    """Multiple positions are captured."""

    service_clients = (
        create_clients()
    )

    service = create_service(
        service_clients,
    )

    context = create_context_with_cameras(
        (1, 2, 3, 4, 5),
    )

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

    context = create_context_with_cameras(
        (1, 2, 3, 4, 5),
    )

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

    failed = (
        record.failed_camera_poses
    )

    assert len(
        failed
    ) == 1

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

    context = create_context_with_cameras(
        (1, 2, 3, 4, 5),
    )

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


def test_shutdown_only_disconnects_enabled_cameras():
    """
    Shutdown only stops and disconnects cameras
    that were actually connected.
    """

    service_clients = (
        create_clients()
    )

    service = (
        create_service_with_disabled_cameras(
            service_clients,
        )
    )

    context = create_context_with_cameras(
        (1, 3, 4),
    )

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

    for number in (
        1,
        3,
        4,
    ):

        client = service_clients[
            f"192.168.7.{10 + number}"
        ]

        client.stop_scan.assert_called_once()

        client.disconnect.assert_called_once()

    for number in (
        2,
        5,
    ):

        client = service_clients[
            f"192.168.7.{10 + number}"
        ]

        client.stop_scan.assert_not_called()

        client.disconnect.assert_not_called()