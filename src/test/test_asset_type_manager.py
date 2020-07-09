from shutil import rmtree
from unittest import TestCase

from asset import AssetType
from asset.asset_type_manager import AssetTypeManager
from database import Column, DataTypes
from exceptions.asset import AssetTypeAlreadyExistsException, AssetTypeInconsistencyException
from test.test_util import init_test_db


class TestAssetTypeManager(TestCase):

    def setUp(self) -> None:
        self.tempdir, self.db_connection = init_test_db()
        self.asset_type_manager: AssetTypeManager = AssetTypeManager()

        self.asset_type = AssetType(
            'TestAsset',
            [
                Column('TestText', DataTypes.VARCHAR, True),
                Column('TextNumber', DataTypes.NUMBER, True)
            ])

    def tearDown(self) -> None:
        self.db_connection.kill()
        rmtree(self.tempdir)

    def test_create_asset_type(self):
        self.asset_type_manager.create_asset_type(self.asset_type)
        self.assertEqual('TestAsset', self.asset_type_manager.get_one(1).asset_name)
        self.assertRaises(AssetTypeAlreadyExistsException, self.asset_type_manager.create_asset_type, self.asset_type)

    def test_delete_asset_type(self):
        self.asset_type_manager.create_asset_type(self.asset_type)
        self.asset_type = self.asset_type_manager.get_one(1)
        self.assertEqual('TestAsset', self.asset_type.asset_name)
        self.asset_type_manager.delete_asset_type(self.asset_type)
        self.asset_type = self.asset_type_manager.get_one(1)
        self.assertIsNone(self.asset_type)

    def test_update_asset_type(self):
        self.asset_type_manager.create_asset_type(self.asset_type)
        self.assertRaises(AttributeError, self.asset_type_manager.update_asset_type, self.asset_type)
        self.asset_type = self.asset_type_manager.get_one(1)
        self.assertEqual('TestAsset', self.asset_type.asset_name)

        update_asset_type = AssetType(
            asset_name='UpdatedAssetType',
            columns=[
                Column('TestText', DataTypes.VARCHAR, True),
                Column('TextNumber', DataTypes.NUMBER, True),
                Column("AppendedColumn", DataTypes.VARCHAR, False)
            ],
            asset_type_id=1
        )
        self.asset_type_manager.update_asset_type(update_asset_type)

        updated_asset_type = self.asset_type_manager.get_one(1)
        self.assertEqual(update_asset_type.asset_name, updated_asset_type.asset_name)
        self.assertEqual(update_asset_type.columns, updated_asset_type.columns)
        self.assertFalse(self.asset_type_manager.check_asset_type_exists(self.asset_type))

        self.asset_type.asset_type_id = None
        self.asset_type_manager.create_asset_type(self.asset_type)
        update_asset_type.asset_type_id = 2
        self.assertRaises(AssetTypeAlreadyExistsException, self.asset_type_manager.update_asset_type, update_asset_type)

    def test_check_asset_type_exists(self):
        self.asset_type_manager.create_asset_type(self.asset_type)
        self.asset_type = self.asset_type_manager.get_one(1)
        self.assertTrue(self.asset_type_manager.check_asset_type_exists(self.asset_type))
        self.asset_type_manager.delete_asset_type(self.asset_type)
        self.assertFalse(self.asset_type_manager.check_asset_type_exists(self.asset_type))

    def test_get_all(self):
        self.asset_type_manager.create_asset_type(self.asset_type)
        all_asset_types = self.asset_type_manager.get_all()
        self.asset_type.asset_type_id = 1
        self.asset_type.asset_table_name = 'abasset_table_TestAsset'
        self.assertEqual([self.asset_type], all_asset_types)

    def test_get_one(self):
        self.asset_type_manager.create_asset_type(self.asset_type)
        asset_type = self.asset_type_manager.get_one(1)
        self.asset_type.asset_type_id = 1
        self.asset_type.asset_table_name = 'abasset_table_TestAsset'
        self.assertEqual(self.asset_type, asset_type)

    def test__check_asset_type_consistency(self):
        self.asset_type_manager.create_asset_type(self.asset_type)
        asset_type = self.asset_type_manager.get_one(1)
        self.asset_type.asset_type_id = 1
        self.asset_type.asset_table_name = 'abasset_table_TestAsset'
        self.assertEqual(self.asset_type, asset_type)
        self.db_connection.delete_table(self.asset_type.asset_table_name)
        self.assertRaises(AssetTypeInconsistencyException, self.asset_type_manager._check_asset_type_consistency)
