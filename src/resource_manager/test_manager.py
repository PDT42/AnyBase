"""
:Author: PDT
:Since: 2020/06/02

Tests for the manager module.
"""

import unittest

from resource_manager.resource_manager import ResourceManager


class TestResourceManager(unittest.TestCase):
    """Tests for the ``ResourceManager``."""

    def test_create_resource_type(self):
        """Test :meth:`~resource_manager.manager.ResourceManager.create_resource_type`."""

        # TODO
