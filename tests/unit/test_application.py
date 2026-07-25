from src.application import Application


def test_application_initialises():

    application = Application()

    application.initialise()

    assert application.logger is not None

    assert application.configuration.application_name == "Scanner Controller"