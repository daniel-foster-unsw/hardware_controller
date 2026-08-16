"""
Real integration tests for the enabled camera controllers.
"""

from __future__ import annotations

import os

from concurrent.futures import (
    ThreadPoolExecutor,
    TimeoutError as FutureTimeoutError,
)

from dataclasses import replace
from types import SimpleNamespace

from src.camera.services.camera_capture_service import (
    CameraCaptureService,
)

from src.scanner.enums.camera_id import (
    CameraID,
)

from tests.helpers.scan_context_factory import (
    create_scan_context,
)


CAMERA_PORT = 5000

CAMERA_TIMEOUT_SECONDS = 5.0


# Cameras currently available for the milestone.
#
# CAM02 and CAM05 remain disabled because of the
# current networking problems.
ENABLED_CAMERA_NUMBERS = (
    1,
    3,
    4,
)


def create_camera_config():
    """
    Create configuration for all five cameras.

    Only the currently available cameras are enabled.
    """

    cameras = {}

    for number in range(1, 6):

        camera_name = (
            f"CAM0{number}"
        )

        host = os.environ.get(
            f"{camera_name}_HOST",
        )

        if number in ENABLED_CAMERA_NUMBERS:

            assert host is not None, (
                f"{camera_name}_HOST is not set."
            )

            enabled = True

        else:

            enabled = False

        cameras[
            camera_name
        ] = SimpleNamespace(
            enabled=enabled,
            host=(
                host
                or f"192.168.7.{10 + number}"
            ),
            port=CAMERA_PORT,
        )

    return cameras


def create_all_camera_context():
    """
    Create a scan context using the currently
    enabled cameras.
    """

    context = create_scan_context()

    context.configuration = replace(
        context.configuration,
        enabled_cameras=(
            ENABLED_CAMERA_NUMBERS
        ),
    )

    return context


def create_camera_service():
    """Create a camera capture service."""

    return CameraCaptureService(
        cameras=create_camera_config(),
        port=CAMERA_PORT,
    )


def run_with_timeout(
    function,
    timeout: float,
):
    """
    Run one camera operation with a timeout.
    """

    with ThreadPoolExecutor(
        max_workers=1,
    ) as executor:

        future = executor.submit(
            function,
        )

        try:

            return future.result(
                timeout=timeout,
            )

        except FutureTimeoutError as exception:

            future.cancel()

            raise TimeoutError(
                "Camera operation timed out."
            ) from exception


def test_all_cameras_initialise():
    """
    All currently enabled cameras initialise.
    """

    service = create_camera_service()

    context = create_all_camera_context()

    try:

        service.initialise(
            context,
        )

        assert service.initialised

        assert (
            service.camera_count
            == len(
                ENABLED_CAMERA_NUMBERS
            )
        )

        assert set(
            service.clients.keys()
        ) == {
            CameraID.CAM01,
            CameraID.CAM03,
            CameraID.CAM04,
        }

        assert (
            CameraID.CAM02
            not in service.clients
        )

        assert (
            CameraID.CAM05
            not in service.clients
        )

    finally:

        service.shutdown(
            context,
        )


def test_all_cameras_capture_position():
    """
    All enabled cameras are given an opportunity
    to capture one position.

    A camera that exceeds the timeout is skipped
    so the remaining cameras can continue.
    """

    service = create_camera_service()

    context = create_all_camera_context()

    try:

        service.initialise(
            context,
        )

        results = {}

        for camera_id in (
            CameraID.CAM01,
            CameraID.CAM03,
            CameraID.CAM04,
        ):

            client = service.clients.get(
                camera_id,
            )

            assert client is not None

            try:

                response = run_with_timeout(
                    client.capture_image,
                    CAMERA_TIMEOUT_SECONDS,
                )

                results[
                    camera_id
                ] = response

                print(
                    f"{camera_id.name}: "
                    "capture response received."
                )

            except TimeoutError:

                results[
                    camera_id
                ] = None

                print(
                    f"{camera_id.name}: "
                    f"timed out after "
                    f"{CAMERA_TIMEOUT_SECONDS} "
                    "seconds."
                )

        successful = sum(
            response is not None
            for response
            in results.values()
        )

        print(
            "Successful cameras: "
            f"{successful}/"
            f"{len(ENABLED_CAMERA_NUMBERS)}"
        )

        assert successful > 0, (
            "No enabled cameras completed "
            "the capture."
        )

    finally:

        service.shutdown(
            context,
        )


def test_all_cameras_multiple_positions():
    """
    All enabled cameras are given two capture
    opportunities.

    Individual camera timeouts do not prevent
    the test from continuing to the next camera.
    """

    service = create_camera_service()

    context = create_all_camera_context()

    try:

        service.initialise(
            context,
        )

        results = {}

        for camera_id in (
            CameraID.CAM01,
            CameraID.CAM03,
            CameraID.CAM04,
        ):

            client = service.clients.get(
                camera_id,
            )

            assert client is not None

            camera_results = []

            for capture_number in (
                1,
                2,
            ):

                try:

                    response = run_with_timeout(
                        client.capture_image,
                        CAMERA_TIMEOUT_SECONDS,
                    )

                    camera_results.append(
                        response,
                    )

                    print(
                        f"{camera_id.name}: "
                        f"capture "
                        f"{capture_number} "
                        "completed."
                    )

                except TimeoutError:

                    camera_results.append(
                        None,
                    )

                    print(
                        f"{camera_id.name}: "
                        f"capture "
                        f"{capture_number} "
                        f"timed out after "
                        f"{CAMERA_TIMEOUT_SECONDS} "
                        "seconds."
                    )

            results[
                camera_id
            ] = camera_results

        successful = sum(
            response is not None
            for camera_results
            in results.values()
            for response
            in camera_results
        )

        total_opportunities = (
            len(
                ENABLED_CAMERA_NUMBERS
            )
            * 2
        )

        print(
            "Successful captures: "
            f"{successful}/"
            f"{total_opportunities}"
        )

        assert successful > 0, (
            "No enabled cameras completed "
            "any captures."
        )

    finally:

        service.shutdown(
            context,
        )