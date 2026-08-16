"""
Real integration tests for CameraCaptureService.
"""

from __future__ import annotations

import os

from dataclasses import replace
from types import SimpleNamespace

from src.camera.services.camera_capture_service import (
    CameraCaptureService,
)

from tests.helpers.scan_context_factory import (
    create_scan_context,
)


CAMERA_HOST = os.environ.get(
    "CAM01_HOST",
)

CAMERA_PORT = 5000


def create_camera_config():
    """Create the CAM01 configuration."""

    assert CAMERA_HOST is not None

    return {
        "CAM01": SimpleNamespace(
            enabled=True,
            host=CAMERA_HOST,
            port=CAMERA_PORT,
        ),
    }


def create_camera_service():
    """Create a CameraCaptureService for CAM01."""

    return CameraCaptureService(
        cameras=create_camera_config(),
        port=CAMERA_PORT,
    )


def create_cam01_context():
    """Create a scan context with only CAM01 enabled."""

    context = create_scan_context()

    configuration = replace(
        context.configuration,
        enabled_cameras=(1,),
    )

    context.configuration = configuration

    return context


def test_cam01_service_initialise():
    """CAM01 service can initialise."""

    service = create_camera_service()

    context = create_cam01_context()

    try:

        service.initialise(
            context,
        )

        assert service.initialised

        assert service.camera_count == 1

    finally:

        service.shutdown(
            context,
        )


def test_cam01_service_capture_position():
    """CAM01 service captures a real image."""

    service = create_camera_service()

    context = create_cam01_context()

    try:

        service.initialise(
            context,
        )

        record = service.capture_position(
            context,
        )

        assert record is not None

        assert record.capture_index == 1

        assert record.camera_count == 1

        assert record.successful_captures == 1

        assert record.failed_captures == 0

        assert record.successful

        camera_pose = (
            record.camera_poses[0]
        )

        assert camera_pose.image_name

        assert (
            camera_pose.capture_successful
        )

    finally:

        service.shutdown(
            context,
        )


def test_cam01_service_multiple_captures():
    """CAM01 service captures multiple positions."""

    service = create_camera_service()

    context = create_cam01_context()

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

        assert first.successful

        assert second.successful

        assert (
            first.image_names[0]
            != second.image_names[0]
        )

    finally:

        service.shutdown(
            context,
        )