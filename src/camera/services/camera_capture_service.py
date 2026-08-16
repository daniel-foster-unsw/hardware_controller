"""
Camera capture service.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from typing import Callable

from src.camera.client.camera_client import (
    CameraClient,
)

from src.camera.services.capture_service import (
    CaptureService,
)

from src.scan.models.capture_record import (
    CaptureRecord,
)

from src.scan.models.scan_context import (
    ScanContext,
)

from src.scanner.builders.camera_pose_builder import (
    CameraPoseBuilder,
)

from src.scanner.enums.camera_id import (
    CameraID,
)

from src.scanner.models.scanner_pose import (
    ScannerPose,
)


class CameraCaptureService(CaptureService):
    """
    Real camera implementation of CaptureService.

    Manages the camera controllers used during a scan.
    """

    DEFAULT_PORT = 5000

    def __init__(
        self,
        camera_hosts: dict[int, str],
        port: int = DEFAULT_PORT,
        client_factory: Callable[
            [str, int],
            CameraClient,
        ] = CameraClient,
    ) -> None:
        """
        Create the camera capture service.

        Parameters
        ----------
        camera_hosts:
            Mapping of logical camera IDs to IP addresses.

            Example:
                {
                    1: "192.168.7.11",
                    2: "192.168.7.12",
                }

        port:
            Camera controller TCP port.

        client_factory:
            Factory used to create CameraClient instances.
            This allows the service to be unit tested without
            real cameras.
        """

        self._camera_hosts = dict(
            camera_hosts,
        )

        self._port = port

        self._client_factory = (
            client_factory
        )

        self._clients: dict[
            CameraID,
            CameraClient,
        ] = {}

        self._initialised = False

        self._capture_index = 0

    @property
    def initialised(self) -> bool:
        """Return whether the service is initialised."""

        return self._initialised

    @property
    def camera_count(self) -> int:
        """Return the number of connected cameras."""

        return len(
            self._clients,
        )

    @property
    def clients(
        self,
    ) -> dict[
        CameraID,
        CameraClient,
    ]:
        """
        Return the configured camera clients.

        The returned dictionary is a copy.
        """

        return dict(
            self._clients,
        )

    def initialise(
        self,
        context: ScanContext,
    ) -> None:
        """
        Connect to and initialise the enabled cameras.
        """

        if self._initialised:
            return

        self._capture_index = 0

        enabled_cameras = (
            context.configuration.enabled_cameras
        )

        try:
            for camera_number in enabled_cameras:

                camera_id = CameraID(
                    camera_number,
                )

                host = (
                    self._camera_hosts.get(
                        camera_number,
                    )
                )

                if host is None:
                    raise ValueError(
                        "No host configured for "
                        f"{camera_id.name}."
                    )

                client = (
                    self._client_factory(
                        host,
                        self._port,
                    )
                )

                client.connect()

                response = client.start_scan()

                if response.get(
                    "status",
                ) != "OK":
                    raise RuntimeError(
                        "Failed to start camera "
                        f"{camera_id.name} scan: "
                        f"{response.get('message', '')}"
                    )

                self._clients[
                    camera_id
                ] = client

            self._initialised = True

        except Exception:
            self._shutdown_clients()

            raise

    def capture_position(
        self,
        context: ScanContext,
    ) -> CaptureRecord:
        """
        Capture one image from every enabled camera.
        """

        if not self._initialised:
            raise RuntimeError(
                "Camera capture service is not initialised."
            )

        self._capture_index += 1

        scanner_pose = ScannerPose(
            arm_x_mm=float(
                self._capture_index * 50
            ),
            camera1_z_mm=320.0,
            camera2_z_mm=315.0,
            camera4_z_mm=305.0,
            camera5_z_mm=295.0,
        )

        camera_poses = CameraPoseBuilder.build(
            geometry=context.geometry,
            scanner_pose=scanner_pose,
            capture_index=self._capture_index,
        )

        enabled_cameras = {
            CameraID(camera)
            for camera
            in context.configuration.enabled_cameras
        }

        results = []

        for pose in camera_poses:

            if pose.camera_id not in enabled_cameras:
                continue

            client = self._clients.get(
                pose.camera_id,
            )

            if client is None:
                raise RuntimeError(
                    "No client configured for "
                    f"{pose.camera_id.name}."
                )

            response = client.capture_image()

            if response.get(
                "status",
            ) != "OK":
                results.append(
                    replace(
                        pose,
                        image_name="",
                        capture_successful=False,
                    )
                )

                continue

            data = response.get(
                "data"
            )

            if not isinstance(
                data,
                dict,
            ):
                results.append(
                    replace(
                        pose,
                        image_name="",
                        capture_successful=False,
                    )
                )

                continue

            image_name = data.get(
                "filename",
            )

            if not image_name:
                results.append(
                    replace(
                        pose,
                        image_name="",
                        capture_successful=False,
                    )
                )

                continue

            results.append(
                replace(
                    pose,
                    image_name=image_name,
                    capture_successful=True,
                )
            )

        return CaptureRecord(
            capture_index=self._capture_index,
            target_position_mm=scanner_pose.arm_x_mm,
            timestamp=datetime.now(),
            scanner_pose=scanner_pose,
            camera_poses=tuple(
                results,
            ),
        )

    def shutdown(
        self,
        context: ScanContext,
    ) -> None:
        """
        Stop the camera scans and disconnect.
        """

        self._shutdown_clients()

        self._initialised = False

    def _shutdown_clients(
        self,
    ) -> None:
        """Stop and disconnect all camera clients."""

        clients = list(
            self._clients.items()
        )

        self._clients.clear()

        for _, client in clients:

            try:
                client.stop_scan()
            except Exception:
                pass

            try:
                client.disconnect()
            except Exception:
                pass