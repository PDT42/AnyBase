"""
:Author: PDT
:Since: 2020/09/18

This is a test runner for servers.
"""

from shutil import rmtree
from time import sleep
from unittest import TestLoader
from unittest import TestSuite
from unittest import TextTestRunner

from database.sqlite_connection import SqliteConnection
from test.api_test_server import th_run_app


def create_test_suite():
    """Create a test suite for the API tests."""

    # Creating test suite
    test_suite = TestSuite()
    test_loader = TestLoader()

    # Adding tests to suite
    test_suite.addTest(test_loader.loadTestsFromName('test.test_asset_type_server'))

    return test_suite


if __name__ == '__main__':

    try:

        # Running an api test server
        app, thread, tempdir = th_run_app()
        sleep(1)  # Wait for the server to start

        SqliteConnection.get(f"{tempdir}\\database.db")

        # Creating a test runner
        runner = TextTestRunner()
        runner.run(create_test_suite())

        # Deleting the temp files.
        SqliteConnection.get().close()
        rmtree(tempdir)

    except RuntimeError:
        pass
