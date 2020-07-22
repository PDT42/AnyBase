"""
:Author: PDT
:Since: 2020/07/05

These are tests for the asset manager.
"""

from shutil import rmtree
from unittest import TestCase

from asset import Asset, AssetType
from asset.asset_manager import AssetManager
from asset.asset_type_manager import AssetTypeManager
from database import Column, DataTypes
from exceptions.asset import AssetTypeDoesNotExistException
from test.test_util import init_test_db


class TestAssetManager(TestCase):

    def setUp(self) -> None:
        """Set up before tests."""
        self.tempdir, self.db_connection = init_test_db()
        self.asset_type_manager: AssetTypeManager = AssetTypeManager()
        self.asset_manager: AssetManager = AssetManager()

        self.asset_type = AssetType(
            'TestAsset',
            [
                Column('TestText', 'testtext', DataTypes.VARCHAR.value, required=True),
                Column('TestNumber', 'testnumber', DataTypes.NUMBER.value, required=True)
            ])
        self.asset_type_manager.create_asset_type(self.asset_type)
        self.asset_type = self.asset_type_manager.get_one(1)

        self.test_asset = Asset(
            asset_id=None, data={"testtext": "Test Asset Test", "testnumber": 5}
        )

    def tearDown(self) -> None:
        """Clean up after each test."""
        self.db_connection.kill()
        rmtree(self.tempdir)

    def test_create_asset(self):
        # Creating an asset
        self.asset_manager.create_asset(self.asset_type, self.test_asset)

        # Updating asset data
        self.test_asset.asset_id = 1

        # Checking if asset exists in the databased
        asset = self.asset_manager.get_one(1, self.asset_type)
        self.assertEqual(asset, self.test_asset)

    def test_delete_asset(self):
        # Creating an asset
        self.asset_manager.create_asset(self.asset_type, self.test_asset)

        # Updating asset data
        self.test_asset.asset_id = 1

        # Checking if asset exists in the database
        asset = self.asset_manager.get_one(1, self.asset_type)
        self.assertEqual(asset, self.test_asset)

        # Deleting asset and checking if it no longer exists
        self.asset_manager.delete_asset(self.asset_type, asset)
        self.assertIsNone(self.asset_manager.get_one(1, self.asset_type))

    def test_update_asset(self):
        # Creating an asset
        self.asset_manager.create_asset(self.asset_type, self.test_asset)
        self.test_asset.asset_id = 1

        # Getting the asset from the database
        asset = self.asset_manager.get_one(1, self.asset_type)

        # Updating data
        asset.data["testtext"] = "Updated Text"
        self.test_asset.data["testtext"] = "Updated Text"

        # Writing changes to database
        self.asset_manager.update_asset(self.asset_type, asset)
        asset = self.asset_manager.get_one(1, self.asset_type)
        self.assertEqual(asset, self.test_asset)

    def test_get_all(self):
        # Creating new asset type to
        asset_type: AssetType = AssetType("DoesNotExist", [Column("test", 'test', DataTypes.VARCHAR.value)])
        self.assertRaises(AssetTypeDoesNotExistException, self.asset_manager.get_all, asset_type)

        # Creating 10 assets in the database
        for iterator in range(0, 10):
            self.test_asset.data["testnumber"] = iterator
            self.asset_manager.create_asset(self.asset_type, self.test_asset)

        # Check if 10 assets exist in the database
        self.assertEqual(10, len(self.asset_manager.get_all(self.asset_type)))

    def test_get_one(self):
        # Create an assetType
        self.asset_manager.create_asset(self.asset_type, self.test_asset)

        # Updating asset data
        self.test_asset.asset_id = 1

        # Checking if asset exists in database
        asset = self.asset_manager.get_one(1, self.asset_type)
        self.assertEqual(asset, self.test_asset)
