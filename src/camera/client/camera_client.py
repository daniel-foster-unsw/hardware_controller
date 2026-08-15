"""
Client for communicating with a Raspberry Pi camera controller.
"""

import json
import socket
from typing import Any, Dict, Optional


class CameraClient:
    """TCP client for a single camera controller."""

    PROTOCOL_VERSION = "1.0"

    def __init__(
        self,
        host: str,
        port: int = 5000,
        timeout: float = 5.0,
    ) -> None:
        self._host = host
        self._port = port
        self._timeout = timeout

        self._socket: Optional[socket.socket] = None
        self._reader = None
        self._writer = None

    @property
    def connected(self) -> bool:
        """Return whether the client is connected."""

        return (
            self._socket is not None
            and self._reader is not None
            and self._writer is not None
        )

    def connect(self) -> None:
        """Connect to the camera controller."""

        if self.connected:
            return

        self._socket = socket.create_connection(
            (self._host, self._port),
            timeout=self._timeout,
        )

        self._reader = self._socket.makefile(
            "r",
            encoding="utf-8",
        )

        self._writer = self._socket.makefile(
            "w",
            encoding="utf-8",
        )

    def disconnect(self) -> None:
        """Disconnect from the camera controller."""

        if self._reader is not None:
            self._reader.close()

        if self._writer is not None:
            self._writer.close()

        if self._socket is not None:
            self._socket.close()

        self._reader = None
        self._writer = None
        self._socket = None

    def ping(self) -> Dict[str, Any]:
        """Ping the camera controller."""

        return self._send_command(
            "PING"
        )

    def get_status(self) -> Dict[str, Any]:
        """Retrieve camera status."""

        return self._send_command(
            "GET_CAMERA_STATUS"
        )

    def capture_image(self) -> Dict[str, Any]:
        """Capture an image."""

        return self._send_command(
            "CAPTURE_IMAGE"
        )

    def _send_command(
        self,
        command: str,
        parameters: Optional[
            Dict[str, Any]
        ] = None,
    ) -> Dict[str, Any]:
        """Send a JSON command and receive a JSON response."""

        self._ensure_connected()

        request = {
            "version": self.PROTOCOL_VERSION,
            "command": command,
            "parameters": parameters or {},
        }

        message = json.dumps(
            request,
            separators=(",", ":"),
        )

        self._writer.write(
            message + "\n"
        )

        self._writer.flush()

        response = self._reader.readline()

        if not response:
            raise ConnectionError(
                "Camera controller closed the connection."
            )

        response = response.strip()

        if not response:
            raise ValueError(
                "Camera controller returned an empty response."
            )

        return json.loads(response)

    def _ensure_connected(self) -> None:
        """Ensure the client is connected."""

        if not self.connected:
            raise RuntimeError(
                "Camera client is not connected."
            )