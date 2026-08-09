from src.configuration.configuration_manager import ConfigurationManager


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