"""
Scanner TCP server.
"""

from __future__ import annotations

import json
import socket
import threading

from src.communication.scanner.scanner_command import (
    ScannerCommand,
)

from src.communication.scanner.scanner_command_handler import (
    ScannerCommandHandler,
)

from src.communication.scanner.scanner_request import (
    ScannerRequest,
)


class ScannerServer:
    """
    TCP server for communication with the Windows HMI.
    """

    def __init__(
        self,
        host: str,
        port: int,
        command_handler: ScannerCommandHandler,
        logger,
    ) -> None:

        self._logger = logger

        self._host = host

        self._port = port

        self._command_handler = (
            command_handler
        )

        self._server_socket: (
            socket.socket | None
        ) = None

        self._thread: (
            threading.Thread | None
        ) = None

        self._running = False

        self._lock = threading.Lock()

    @property
    def host(self) -> str:
        """Return the configured host."""

        return self._host

    @property
    def port(self) -> int:
        """Return the configured port."""

        if self._server_socket is not None:

            return self._server_socket.getsockname()[1]

        return self._port

    @property
    def running(self) -> bool:
        """Return whether the server is running."""

        with self._lock:

            return self._running

    def start(self) -> None:
        """
        Start the TCP server.

        The server runs on a background thread.
        """

        with self._lock:

            if self._running:

                raise RuntimeError(
                    "Scanner server is already running."
                )

            server_socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
            )

            server_socket.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                1,
            )

            server_socket.bind(
                (
                    self._host,
                    self._port,
                )
            )

            server_socket.listen(5)

            server_socket.settimeout(0.5)

            self._server_socket = (
                server_socket
            )

            self._running = True

            self._thread = threading.Thread(
                target=self._serve,
                name="ScannerServer",
                daemon=True,
            )

            self._thread.start()

    def stop(self) -> None:
        """
        Stop the TCP server.
        """

        with self._lock:

            if not self._running:

                return

            self._running = False

            server_socket = (
                self._server_socket
            )

            self._server_socket = None

        if server_socket is not None:

            server_socket.close()

        thread = self._thread

        if thread is not None:

            thread.join(
                timeout=2.0,
            )

        self._thread = None

    def wait_for_start(
        self,
        timeout: float = 2.0,
    ) -> bool:
        """
        Wait until the server reports as running.
        """

        event = threading.Event()

        def wait() -> None:

            while not event.is_set():

                if self.running:

                    event.set()

                    return

                event.wait(0.01)

        thread = threading.Thread(
            target=wait,
            daemon=True,
        )

        thread.start()

        thread.join(
            timeout=timeout,
        )

        return self.running

    def _serve(self) -> None:
        """
        Accept incoming TCP connections.
        """

        while self.running:

            server_socket = (
                self._server_socket
            )

            if server_socket is None:

                break

            try:

                client_socket, _ = (
                    server_socket.accept()
                )

            except socket.timeout:

                continue

            except OSError:

                if self.running:

                    continue

                break

            client_thread = (
                threading.Thread(
                    target=self._handle_client,
                    args=(client_socket,),
                    name="ScannerClient",
                    daemon=True,
                )
            )

            client_thread.start()

    def _handle_client(
        self,
        client_socket: socket.socket,
    ) -> None:
        """
        Handle a single HMI TCP connection.
        """

        try:

            client_socket.settimeout(
                30.0,
            )

            reader = (
                client_socket.makefile(
                    "r",
                    encoding="utf-8",
                )
            )

            writer = (
                client_socket.makefile(
                    "w",
                    encoding="utf-8",
                )
            )

            try:

                for line in reader:

                    line = line.strip()

                    if not line:

                        continue

                    response = (
                        self._handle_request(
                            line,
                        )
                    )

                    writer.write(
                        response
                        + "\n"
                    )

                    writer.flush()

            finally:

                reader.close()

                writer.close()

        except OSError:

            return

        finally:

            client_socket.close()

    def _handle_request(
        self,
        message: str,
    ) -> str:
        """
        Process one JSON request.
        """

        self._logger.info(
            "Received JSON: %s",
            message,
        )

        try:

            request_data = json.loads(
                message,
            )

            request = (
                self._create_request(
                    request_data,
                )
            )

            response = (
                self._command_handler.handle(
                    request,
                )
            )

            response_data = {
                "version":
                    response.version,

                "success":
                    response.success,

                "message":
                    response.message,

                "data":
                    response.data,
            }

            response_json = json.dumps(
                response_data,
                separators=(
                    ",",
                    ":",
                ),
            )

            self._logger.info(
                "Sending JSON: %s",
                response_json,
            )

            return response_json

        except Exception as exception:

            response_data = {
                "version": "1.0",

                "success": False,

                "message":
                    str(exception),

                "data": None,
            }

            response_json = json.dumps(
                response_data,
                separators=(
                    ",",
                    ":",
                ),
            )

            self._logger.warning(
                "Sending JSON: %s",
                response_json,
            )

            return response_json

    @staticmethod
    def _create_request(
        data: dict,
    ) -> ScannerRequest:
        """
        Convert JSON data into ScannerRequest.
        """

        version = data.get(
            "version",
            "1.0",
        )

        command_name = data.get(
            "command",
        )

        if command_name is None:

            raise ValueError(
                "Request is missing command."
            )

        try:

            command = ScannerCommand(
                command_name,
            )

        except ValueError as exception:

            raise ValueError(
                f"Unsupported command: "
                f"{command_name}"
            ) from exception

        parameters = data.get(
            "parameters",
            {},
        )

        if parameters is None:

            parameters = {}

        if not isinstance(
            parameters,
            dict,
        ):

            raise ValueError(
                "Request parameters must be an object."
            )

        return ScannerRequest(
            version=version,
            command=command,
            parameters=parameters,
        )