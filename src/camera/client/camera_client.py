"""
Client for communicating with a Raspberry Pi camera controller.
"""

import json
import socket

from typing import (
    Any,
    Dict,
    Optional,
)


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

        self._socket: Optional[
            socket.socket
        ] = None

        self._receive_buffer = bytearray()

    @property
    def connected(self) -> bool:
        """Return whether the client is connected."""

        return self._socket is not None

    def connect(self) -> None:
        """Connect to the camera controller."""

        if self.connected:
            return

        self._socket = socket.create_connection(
            (
                self._host,
                self._port,
            ),
            timeout=self._timeout,
        )

        self._socket.settimeout(
            self._timeout
        )

        self._receive_buffer.clear()

    def disconnect(self) -> None:
        """Disconnect from the camera controller."""

        if self._socket is not None:
            try:
                self._socket.shutdown(
                    socket.SHUT_RDWR
                )
            except OSError:
                pass

            self._socket.close()

        self._socket = None
        self._receive_buffer.clear()

    def ping(
        self,
    ) -> Dict[str, Any]:
        """Ping the camera controller."""

        return self._send_command(
            "PING"
        )

    def get_status(
        self,
    ) -> Dict[str, Any]:
        """Retrieve camera status."""

        return self._send_command(
            "GET_CAMERA_STATUS"
        )

    def start_scan(
        self,
    ) -> Dict[str, Any]:
        """Start a camera scan."""

        return self._send_command(
            "START_SCAN"
        )

    def stop_scan(
        self,
    ) -> Dict[str, Any]:
        """Stop the active camera scan."""

        return self._send_command(
            "STOP_SCAN"
        )

    def capture_image(
        self,
    ) -> Dict[str, Any]:
        """Capture an image during an active scan."""

        return self._send_command(
            "CAPTURE_IMAGE"
        )

    def download_image(
        self,
        filename: str,
    ) -> Dict[str, Any]:
        """
        Download an image from the camera controller.

        Returns
        -------
        dict
            Dictionary containing the transfer header and
            raw image data under the ``data`` key.
        """

        if not filename:
            raise ValueError(
                "Filename cannot be empty."
            )

        header = self._send_command(
            "DOWNLOAD_IMAGE",
            {
                "filename": filename,
            },
        )

        data = header.get(
            "data"
        )

        if not isinstance(
            data,
            dict,
        ):
            raise ValueError(
                "Invalid image transfer response."
            )

        transfer_filename = data.get(
            "filename"
        )

        filesize = data.get(
            "filesize"
        )

        if not transfer_filename:
            raise ValueError(
                "Image transfer response "
                "did not contain a filename."
            )

        if not isinstance(
            filesize,
            int,
        ):
            raise ValueError(
                "Image transfer response "
                "did not contain a valid filesize."
            )

        image_data = self._receive_exactly(
            filesize
        )

        return {
            "version":
                header.get(
                    "version"
                ),

            "status":
                header.get(
                    "status"
                ),

            "message":
                header.get(
                    "message"
                ),

            "filename":
                transfer_filename,

            "filesize":
                filesize,

            "data":
                image_data,
        }

    def _send_command(
        self,
        command: str,
        parameters: Optional[
            Dict[str, Any]
        ] = None,
    ) -> Dict[str, Any]:
        """
        Send a JSON command and receive
        a JSON response.
        """

        self._ensure_connected()

        request = {
            "version":
                self.PROTOCOL_VERSION,

            "command":
                command,

            "parameters":
                parameters or {},
        }

        message = json.dumps(
            request,
            separators=(
                ",",
                ":",
            ),
        )

        self._socket.sendall(
            (
                message + "\n"
            ).encode(
                "utf-8"
            )
        )

        return self._receive_json()

    def _receive_json(
        self,
    ) -> Dict[str, Any]:
        """Receive one newline-delimited JSON message."""

        response = self._receive_line()

        if not response:
            raise ConnectionError(
                "Camera controller closed "
                "the connection."
            )

        try:
            result = json.loads(
                response.decode(
                    "utf-8"
                )
            )
        except json.JSONDecodeError as exception:
            raise ValueError(
                "Camera controller returned "
                "invalid JSON."
            ) from exception

        if not isinstance(
            result,
            dict,
        ):
            raise ValueError(
                "Camera controller returned "
                "an invalid response."
            )

        return result

    def _receive_line(
        self,
    ) -> bytes:
        """
        Receive bytes until a newline is found.

        Any bytes received after the newline are retained
        in the internal buffer for a subsequent binary
        transfer.
        """

        while True:

            newline_index = (
                self._receive_buffer.find(
                    b"\n"
                )
            )

            if newline_index >= 0:

                line = bytes(
                    self._receive_buffer[
                        :newline_index
                    ]
                )

                del self._receive_buffer[
                    :newline_index + 1
                ]

                return line.rstrip(
                    b"\r"
                )

            self._receive_from_socket()

    def _receive_exactly(
        self,
        size: int,
    ) -> bytes:
        """
        Receive exactly ``size`` bytes.
        """

        if size < 0:
            raise ValueError(
                "Receive size cannot be negative."
            )

        while len(
            self._receive_buffer
        ) < size:

            self._receive_from_socket()

        data = bytes(
            self._receive_buffer[
                :size
            ]
        )

        del self._receive_buffer[
            :size
        ]

        return data

    def _receive_from_socket(
        self,
    ) -> None:
        """Receive another block from the socket."""

        self._ensure_connected()

        data = self._socket.recv(
            4096
        )

        if not data:
            raise ConnectionError(
                "Camera controller closed "
                "the connection."
            )

        self._receive_buffer.extend(
            data
        )

    def _ensure_connected(
        self,
    ) -> None:
        """Ensure the client is connected."""

        if not self.connected:
            raise RuntimeError(
                "Camera client is not connected."
            )