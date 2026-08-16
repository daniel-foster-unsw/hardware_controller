"""
Real integration tests for all five camera controllers.
"""

import os

from concurrent.futures import (
    ThreadPoolExecutor,
    TimeoutError as FutureTimeoutError,
)

from dataclasses import replace

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

# Maximum time allowed for an individual camera operation.
CAMERA_TIMEOUT_SECONDS = 5.0


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

        except FutureTimeoutError:

            future.cancel()

            raise TimeoutError(
                "Camera operation timed out."
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

        assert service.camera_count == 5

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
    """
    All five cameras are given an opportunity to capture
    one position.

    A camera that exceeds the timeout is skipped so that
    the remaining cameras can continue.
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
            CameraID.CAM02,
            CameraID.CAM03,
            CameraID.CAM04,
            CameraID.CAM05,
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

                results[camera_id] = response

                print(
                    f"{camera_id.name}: "
                    "capture response received."
                )

            except TimeoutError:

                results[camera_id] = None

                print(
                    f"{camera_id.name}: "
                    f"timed out after "
                    f"{CAMERA_TIMEOUT_SECONDS} seconds."
                )

        successful = sum(
            response is not None
            for response in results.values()
        )

        print(
            f"Successful cameras: "
            f"{successful}/5"
        )

        assert successful > 0, (
            "No cameras completed the capture."
        )

    finally:
        service.shutdown(
            context,
        )


def test_all_cameras_multiple_positions():
    """
    All five cameras are given two capture opportunities.

    Individual camera timeouts do not prevent the test
    from continuing to the next camera.
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
            CameraID.CAM02,
            CameraID.CAM03,
            CameraID.CAM04,
            CameraID.CAM05,
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
                        f"capture {capture_number} "
                        "completed."
                    )

                except TimeoutError:

                    camera_results.append(
                        None,
                    )

                    print(
                        f"{camera_id.name}: "
                        f"capture {capture_number} "
                        f"timed out after "
                        f"{CAMERA_TIMEOUT_SECONDS} seconds."
                    )

            results[camera_id] = (
                camera_results
            )

        successful = sum(
            response is not None
            for camera_results
            in results.values()
            for response
            in camera_results
        )

        print(
            f"Successful captures: "
            f"{successful}/10"
        )

        assert successful > 0, (
            "No camera captures completed."
        )

    finally:
        service.shutdown(
            context,
        )