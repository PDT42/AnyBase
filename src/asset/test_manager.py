"""
:Author: PDT
:Since: 2020/06/02

Tests for the manager module.
"""

import unittest

from asset.asset_manager import AssetManager


class TestResourceManager(unittest.TestCase):
    """Tests for the ``ResourceManager``."""

    def test_create_resource_type(self):
        """Test :meth:`~asset.manager.ResourceManager.create_asset_type`."""

        # TODO
