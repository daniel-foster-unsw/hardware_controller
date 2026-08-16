"""
Real integration tests for all five camera controllers.
"""

import os

from dataclasses import replace

from src.camera.services.camera_capture_service import (
    CameraCaptureService,
)

from tests.helpers.scan_context_factory import (
    create_scan_context,
)

from src.scanner.enums.camera_id import (
    CameraID,
)


CAMERA_PORT = 5000


def create_camera_hosts() -> dict[int, str]:
    """Read all camera hosts from the environment."""

    hosts = {}

    for camera_number in range(1, 6):

        variable = (
            f"CAM0{camera_number}_HOST"
        )

        host = os.environ.get(
            variable,
        )

        assert host is not None, (
            f"{variable} is not set."
        )

        hosts[camera_number] = host

    return hosts


def create_all_camera_context():
    """Create a scan context with all five cameras enabled."""

    context = create_scan_context()

    configuration = replace(
        context.configuration,
        enabled_cameras=(
            1,
            2,
            3,
            4,
            5,
        ),
    )

    context.configuration = configuration

    return context


def create_camera_service():
    """Create a five-camera capture service."""

    return CameraCaptureService(
        camera_hosts=create_camera_hosts(),
        port=CAMERA_PORT,
    )


def test_all_cameras_initialise():
    """All five cameras initialise successfully."""

    service = create_camera_service()

    context = create_all_camera_context()

    try:
        service.initialise(
            context,
        )

        assert service.initialised

        assert (
            service.camera_count
            == 5
        )

        assert set(
    service.clients.keys()
    ) == {
        CameraID.CAM01,
        CameraID.CAM02,
        CameraID.CAM03,
        CameraID.CAM04,
        CameraID.CAM05,
    }

    finally:
        service.shutdown(
            context,
        )


def test_all_cameras_capture_position():
    """All five cameras capture one position."""

    service = create_camera_service()

    context = create_all_camera_context()

    try:
        service.initialise(
            context,
        )

        record = (
            service.capture_position(
                context,
            )
        )

        assert record is not None

        assert (
            record.capture_index
            == 1
        )

        assert (
            record.camera_count
            == 5
        )

        assert (
            record.successful_captures
            == 5
        )

        assert (
            record.failed_captures
            == 0
        )

        assert record.successful

        assert len(
            record.image_names
        ) == 5

        for image_name in (
            record.image_names
        ):
            assert image_name

            assert image_name.endswith(
                ".jpg"
            )

    finally:
        service.shutdown(
            context,
        )


def test_all_cameras_multiple_positions():
    """All five cameras capture multiple positions."""

    service = create_camera_service()

    context = create_all_camera_context()

    try:
        service.initialise(
            context,
        )

        first = (
            service.capture_position(
                context,
            )
        )

        second = (
            service.capture_position(
                context,
            )
        )

        assert (
            first.capture_index
            == 1
        )

        assert (
            second.capture_index
            == 2
        )

        assert (
            first.camera_count
            == 5
        )

        assert (
            second.camera_count
            == 5
        )

        assert first.successful

        assert second.successful

        assert len(
            set(first.image_names)
        ) == 5

        assert len(
            set(second.image_names)
        ) == 5

        assert (
            set(first.image_names)
            .isdisjoint(
                set(second.image_names)
            )
        )

    finally:
        service.shutdown(
            context,
        )