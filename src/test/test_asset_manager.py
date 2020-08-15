"""
:Author: PDT
:Since: 2020/07/05

These are tests for the asset manager.
"""
import json
from datetime import date, datetime
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
        # print(f"Tempdir used in this tests: {self.tempdir}")

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

    def test_data_types(self):
        """Test creating an asset with one field of each available data type."""

        columns = [
            Column("text_column", "text_column", DataTypes.TEXT.value, required=True),
            Column("number_column", "number_column", DataTypes.NUMBER.value, required=True),
            Column("integer_column", "integer_column", DataTypes.INTEGER.value, required=True),
            Column("bool_column", "bool_column", DataTypes.BOOLEAN.value, required=True),
            Column("datetime_col", "datetime_col", DataTypes.DATETIME.value, required=True),
            Column("date_column", "date_column", DataTypes.DATE.value, required=True),
            # --
            Column("asset_column", "asset_column", DataTypes.ASSET.value, asset_type_id=1, required=True),
            Column("asset_list_col", "asset_list_col", DataTypes.ASSETLIST.value, asset_type_id=1, required=True)
        ]

        asset_type = AssetType(
            asset_name="DatatypeTestAsset",
            columns=columns
        )

        self.asset_type_manager.create_asset_type(asset_type)
        self.assertEqual(2, len(self.asset_type_manager.get_all()))
        asset_type = self.asset_type_manager.get_one(2)
        self.assertEqual("DatatypeTestAsset", asset_type.asset_name)

        self.asset_manager.create_asset(self.asset_type, self.test_asset)
        self.test_asset = self.asset_manager.get_one(1, self.asset_type)

        asset = Asset(data={
            "text_column": "Test Text",
            "number_column": 42.24,
            "integer_column": 5,
            "bool_column": True,
            "datetime_col": datetime.now(),
            "date_column": datetime.now().date(),
            "asset_column": self.test_asset,
            "asset_list_col": [self.test_asset, self.test_asset],
        })
        self.asset_manager.create_asset(asset_type, asset)
        self.assertEqual(1, len(self.asset_manager.get_all(asset_type)))
        asset = self.asset_manager.get_one(1, asset_type)

        self.assertTrue(isinstance(asset.data["text_column"], str))
        self.assertTrue(isinstance(asset.data["number_column"], float))
        self.assertTrue(isinstance(asset.data["integer_column"], int))
        self.assertTrue(isinstance(asset.data["bool_column"], bool))
        self.assertTrue(isinstance(asset.data["datetime_col"], datetime))
        self.assertTrue(isinstance(asset.data["date_column"], date))
        self.assertTrue(isinstance(asset.data["asset_column"], int))
        self.assertTrue(all([isinstance(at, int) for at in asset.data["asset_list_col"]]))

        asset = self.asset_manager.get_one(1, asset_type, 1)
        self.assertTrue(isinstance(asset.data["asset_column"], Asset))
        self.assertTrue(all([isinstance(at, Asset) for at in asset.data["asset_list_col"]]))

    def test_jsonable(self):
        self.test_asset.asset_id = 1

        json.dumps(self.test_asset.as_dict())
