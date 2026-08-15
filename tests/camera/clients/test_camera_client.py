import json
import socket
import threading

import pytest

from src.camera.client.camera_client import (
    CameraClient,
)


def start_server(response):
    """Start a simple local camera server."""

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1,
    )

    server.bind(
        ("127.0.0.1", 0)
    )

    server.listen(1)

    port = server.getsockname()[1]

    def run():
        connection, _ = server.accept()

        try:
            reader = connection.makefile(
                "r",
                encoding="utf-8",
            )

            writer = connection.makefile(
                "w",
                encoding="utf-8",
            )

            request = reader.readline()

            if not request:
                return

            writer.write(
                json.dumps(response)
                + "\n"
            )

            writer.flush()

            writer.close()
            reader.close()

        finally:
            connection.close()
            server.close()

    thread = threading.Thread(
        target=run,
        daemon=True,
    )

    thread.start()

    return port, thread


def test_connect():
    response = {
        "version": "1.0",
        "status": "OK",
        "message": "PONG",
    }

    port, thread = start_server(
        response
    )

    client = CameraClient(
        "127.0.0.1",
        port,
    )

    try:
        client.connect()

        assert client.connected is True

    finally:
        client.disconnect()

    thread.join(
        timeout=1
    )


def test_ping():
    response = {
        "version": "1.0",
        "status": "OK",
        "message": "PONG",
    }

    port, thread = start_server(
        response
    )

    client = CameraClient(
        "127.0.0.1",
        port,
    )

    try:
        client.connect()

        result = client.ping()

        assert result["status"] == "OK"

        assert result["message"] == "PONG"

    finally:
        client.disconnect()

    thread.join(
        timeout=1
    )


def test_get_status():
    response = {
        "version": "1.0",
        "status": "OK",
        "message": "Camera status.",
        "data": {
            "state": "READY",
        },
    }

    port, thread = start_server(
        response
    )

    client = CameraClient(
        "127.0.0.1",
        port,
    )

    try:
        client.connect()

        result = client.get_status()

        assert result["status"] == "OK"

        assert (
            result["data"]["state"]
            == "READY"
        )

    finally:
        client.disconnect()

    thread.join(
        timeout=1
    )


def test_capture_image():
    response = {
        "version": "1.0",
        "status": "OK",
        "message": "Image captured.",
        "data": {
            "filename":
                "20260720_0601_CAM01_000001.jpg",

            "filesize":
                254390,

            "width":
                4056,

            "height":
                3040,

            "format":
                "JPEG",
        },
    }

    port, thread = start_server(
        response
    )

    client = CameraClient(
        "127.0.0.1",
        port,
    )

    try:
        client.connect()

        result = client.capture_image()

        assert result["status"] == "OK"

        assert (
            result["data"]["filename"]
            == "20260720_0601_CAM01_000001.jpg"
        )

        assert (
            result["data"]["format"]
            == "JPEG"
        )

    finally:
        client.disconnect()

    thread.join(
        timeout=1
    )


def test_command_without_connection_raises():
    client = CameraClient(
        "127.0.0.1",
        5000,
    )

    with pytest.raises(
        RuntimeError
    ):
        client.ping()


def test_disconnect():
    response = {
        "version": "1.0",
        "status": "OK",
        "message": "PONG",
    }

    port, thread = start_server(
        response
    )

    client = CameraClient(
        "127.0.0.1",
        port,
    )

    client.connect()

    assert client.connected is True

    client.disconnect()

    assert client.connected is False

    thread.join(
        timeout=1
    )