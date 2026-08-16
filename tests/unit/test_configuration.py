from src.configuration.configuration_manager import (
    ConfigurationManager,
)


def test_configuration_loads():

    config = ConfigurationManager()

    config.initialise()

    assert config.application_name == "Scanner Controller"

    assert config.transport == "mock"

    assert config.motor_count == 5


def test_scanner_configuration_loads():

    try:

        config = ConfigurationManager()

        config.initialise()

        assert (
            config.scanner_host
            == "0.0.0.0"
        )

        assert (
            config.scanner_port
            == 5000
        )

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_camera_configuration_loads():

    config = ConfigurationManager()

    config.initialise()

    assert len(
        config.cameras
    ) == 5


def test_camera_enabled_configuration():

    config = ConfigurationManager()

    config.initialise()

    assert config.cameras[1].enabled

    assert not config.cameras[2].enabled

    assert config.cameras[3].enabled

    assert config.cameras[4].enabled

    assert not config.cameras[5].enabled


def test_camera_hosts():

    config = ConfigurationManager()

    config.initialise()

    assert (
        config.cameras[1].host
        == "192.168.7.11"
    )

    assert (
        config.cameras[3].host
        == "192.168.7.13"
    )

    assert (
        config.cameras[4].host
        == "192.168.7.14"
    )


def test_camera_ports():

    config = ConfigurationManager()

    config.initialise()

    for camera in config.cameras.values():

        assert camera.port == 5000