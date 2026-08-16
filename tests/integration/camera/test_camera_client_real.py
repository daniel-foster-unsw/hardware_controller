import os

from src.camera.client.camera_client import (
    CameraClient,
)


CAMERA_HOST = os.environ.get(
    "CAM01_HOST",
)

CAMERA_PORT = 5000


def test_cam01_ping():
    assert CAMERA_HOST is not None

    client = CameraClient(
        CAMERA_HOST,
        CAMERA_PORT,
    )

    try:
        client.connect()

        response = client.ping()

        assert response["status"] == "OK"

        assert (
            response["message"]
            == "PONG"
        )

    finally:
        client.disconnect()


def test_cam01_get_status():
    assert CAMERA_HOST is not None

    client = CameraClient(
        CAMERA_HOST,
        CAMERA_PORT,
    )

    try:
        client.connect()

        response = client.get_status()

        assert response["status"] == "OK"

        assert "data" in response

    finally:
        client.disconnect()


def test_cam01_capture_image():
    assert CAMERA_HOST is not None

    client = CameraClient(
        CAMERA_HOST,
        CAMERA_PORT,
    )

    scan_started = False

    try:
        client.connect()

        start_response = (
            client.start_scan()
        )

        assert (
            start_response["status"]
            == "OK"
        )

        scan_started = True

        capture_response = (
            client.capture_image()
        )

        assert (
            capture_response["status"]
            == "OK"
        )

        assert (
            capture_response["message"]
            == "Image captured."
        )

        data = (
            capture_response["data"]
        )

        assert data is not None

        assert data["filename"]

        assert (
            data["filesize"] > 0
        )

        assert (
            data["width"] > 0
        )

        assert (
            data["height"] > 0
        )

        assert (
            data["format"]
            == "JPEG"
        )

    finally:
        if scan_started:
            try:
                client.stop_scan()
            except Exception:
                pass

        client.disconnect()