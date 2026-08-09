from src.application import Application


def test_application_initialises():

    application = Application()

    application.initialise()

    assert application.logger is not None

    assert application.configuration.application_name == "Scanner Controller"





def test_application_creates_scan_manager():

    try:

        application = Application()

        application.initialise()

        assert (
            application.scan_manager
            is not None
        )

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )

    finally:

        application.shutdown()


def test_application_creates_scanner_geometry():

    try:

        application = Application()

        application.initialise()

        assert (
            application.scanner_geometry
            is not None
        )

        assert (
            application.scanner_geometry.camera_count
            == 5
        )

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )

    finally:

        application.shutdown()


def test_application_creates_scanner_command_handler():

    try:

        application = Application()

        application.initialise()

        assert (
            application.scanner_command_handler
            is not None
        )

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )

    finally:

        application.shutdown()


def test_application_creates_scanner_server():

    try:

        application = Application()

        application.initialise()

        assert (
            application.scanner_server
            is not None
        )

        assert (
            application.scanner_server.host
            == application.configuration.scanner_host
        )

        assert (
            application.scanner_server.port
            == application.configuration.scanner_port
        )

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )

    finally:

        application.shutdown()


def test_application_run_starts_scanner_server():

    try:

        application = Application()

        application.initialise()

        assert (
            application.scanner_server.running
            is False
        )

        application.run()

        assert (
            application.scanner_server.running
            is True
        )

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )

    finally:

        application.shutdown()


def test_application_shutdown_stops_scanner_server():

    try:

        application = Application()

        application.initialise()

        application.run()

        assert (
            application.scanner_server.running
            is True
        )

        application.shutdown()

        assert (
            application.scanner_server
            is None
        )

        assert (
            application.initialised
            is False
        )

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )

    finally:

        application.shutdown()