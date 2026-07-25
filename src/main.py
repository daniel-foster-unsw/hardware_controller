"""
Application entry point.
"""

from application import Application


def main():

    application = Application()

    try:

        application.initialise()

        application.run()
        
    except Exception as ex:

        print(f"Fatal Error: {ex}")

    finally:

        application.shutdown()


if __name__ == "__main__":
    main()