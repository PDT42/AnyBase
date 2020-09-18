"""
:Author: PDT
:Since: 2020/09/18

This is a test runner for the unittests.
"""

from unittest import TestLoader
from unittest import TestSuite
from unittest import TextTestRunner


def create_test_suite():
    """Create a test suite for the API tests."""

    # Creating test suite
    test_suite = TestSuite()
    test_loader = TestLoader()

    # Adding tests to suite
    test_suite.addTest(test_loader.loadTestsFromName('test.test_sqlite_connection'))
    test_suite.addTest(test_loader.loadTestsFromName('test.test_asset_type_manager'))
    test_suite.addTest(test_loader.loadTestsFromName('test.test_asset_manager'))
    test_suite.addTest(test_loader.loadTestsFromName('test.test_page_manager'))

    return test_suite


if __name__ == '__main__':

    # Creating a test runner
    runner = TextTestRunner()
    runner.run(create_test_suite())
