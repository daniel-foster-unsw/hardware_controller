from src.configuration.configuration_manager import ConfigurationManager


def test_configuration_loads():

    config = ConfigurationManager()

    config.initialise()

    assert config.application_name == "Scanner Controller"

    assert config.transport == "mock"

    assert config.motor_count == 5