import json
from copy import deepcopy
from shutil import rmtree
from time import sleep
from unittest import TestCase

from asset_type import AssetType
from asset_type.asset_type_manager import AssetTypeManager
from database import Column, DataTypes
from exceptions.asset import AssetTypeAlreadyExistsException, AssetTypeChangedException, AssetTypeInconsistencyException
from test.test_util import init_test_db


class TestAssetTypeManager(TestCase):

    def setUp(self) -> None:
        self.tempdir, self.db_connection = init_test_db()
        # print(f"Tempdir used in this tests: {self.tempdir}")

        self.asset_type_manager: AssetTypeManager = AssetTypeManager()

        self.asset_type = AssetType(
            'TestAsset',
            [
                Column('TestText', 'testtext', DataTypes.VARCHAR.value, required=True),
                Column('TextNumber', 'textnumber', DataTypes.NUMBER.value, required=True)
            ])

    def tearDown(self) -> None:
        self.db_connection.kill()
        rmtree(self.tempdir)

    def test_create_asset_type(self):
        self.asset_type_manager.create_asset_type(self.asset_type)
        self.assertEqual('TestAsset', self.asset_type_manager.get_one_by_id(1).asset_name)
        self.assertRaises(AssetTypeAlreadyExistsException, self.asset_type_manager.create_asset_type, self.asset_type)

    def test_delete_asset_type(self):
        self.asset_type_manager.create_asset_type(self.asset_type)
        self.asset_type = self.asset_type_manager.get_one_by_id(1)
        self.assertEqual('TestAsset', self.asset_type.asset_name)
        self.asset_type_manager.delete_asset_type(self.asset_type)
        self.asset_type = self.asset_type_manager.get_one_by_id(1)
        self.assertIsNone(self.asset_type)

    def test_update_asset_type(self):
        # Trying to update and asset type, that does not exist
        self.assertRaises(AttributeError, self.asset_type_manager.update_asset_type, self.asset_type)

        # Creating an asset type
        self.asset_type = self.asset_type_manager.create_asset_type(self.asset_type)

        # Ensuring differing timestamps
        sleep(1)

        # Updating the AssetType
        update_asset_type = AssetType(
            asset_name='UpdatedAssetType',
            columns=[
                Column('TestText', 'testtext', DataTypes.VARCHAR.value, required=True),
                Column('renamed_column', 'renamed_column', DataTypes.NUMBER.value, required=True),
            ],
            asset_type_id=1,
            created=self.asset_type.created,
            updated=self.asset_type.updated)
        self.asset_type_manager.update_asset_type(update_asset_type)

        updated_asset_type = self.asset_type_manager.get_one_by_id(1)
        self.assertEqual(update_asset_type.asset_name, updated_asset_type.asset_name)
        self.assertEqual(update_asset_type.columns, updated_asset_type.columns)
        self.assertFalse(self.asset_type_manager.check_asset_type_exists(self.asset_type))

        # Updating again, without reloading self.asset_type after
        # the previous update. This is basically the scenario:
        # -------------------------------------------------------
        # User1 opens edit asset type at time 1
        # User2 opens edit asset type at time 2
        # User2 stores his changes in the database at time 3
        # User1 stores his changes in the database at time 4
        # User1 receives an error, since the asset type he
        # is trying to edit, has been updated in the meantime.

        invalid_update = AssetType(
            asset_name='UpdatedAssetType',
            columns=[
                Column('TestText', 'testtext', DataTypes.VARCHAR.value, required=True),
                Column('invalid_rename', 'invalid_rename', DataTypes.NUMBER.value, required=True),
            ],
            asset_type_id=1,
            created=self.asset_type.created,
            updated=self.asset_type.updated)
        self.assertRaises(AssetTypeChangedException, self.asset_type_manager.update_asset_type, invalid_update)

        invalid_update.updated = updated_asset_type.updated
        valid_asset_type = self.asset_type_manager.update_asset_type(invalid_update)

        # Creating 'another' AssetType
        self.asset_type = self.asset_type_manager.create_asset_type(self.asset_type)

        update_asset_type.asset_type_id = self.asset_type.asset_type_id
        update_asset_type.created = self.asset_type.created
        update_asset_type.updated = self.asset_type.updated

        self.assertRaises(AssetTypeAlreadyExistsException, self.asset_type_manager.update_asset_type, update_asset_type)

    def test_check_asset_type_exists(self):
        self.asset_type_manager.create_asset_type(self.asset_type)
        self.asset_type = self.asset_type_manager.get_one_by_id(1)
        self.assertTrue(self.asset_type_manager.check_asset_type_exists(self.asset_type))
        self.asset_type_manager.delete_asset_type(self.asset_type)
        self.assertFalse(self.asset_type_manager.check_asset_type_exists(self.asset_type))

    def test_get_all(self):
        self.asset_type = self.asset_type_manager.create_asset_type(self.asset_type)
        all_asset_types = self.asset_type_manager.get_all()
        self.assertEqual([self.asset_type], all_asset_types)

    def test_get_all_filtered(self):

        self.create_twenty_samples()
        self.assertEqual(20, len(self.asset_type_manager.get_all()))

        and_filters = ["super_type > 0"]
        self.assertEqual(10, len(self.asset_type_manager.get_all_filtered(and_filters=and_filters)))

        or_filters = [f'asset_name = "{self.asset_type.asset_name}_0"']

        asset_names = ", ".join([f'"{self.asset_type.asset_name}_{i}"' for i in range(4, 12)])
        or_filters.append(f'asset_name in ({asset_names})')
        self.assertEqual(9, len(self.asset_type_manager.get_all_filtered(or_filters=or_filters)))

    def test_get_batch(self):

        self.create_twenty_samples()
        self.assertEqual(20, len(self.asset_type_manager.get_all()))

        asset_types = self.asset_type_manager.get_batch(10, 20)
        self.assertEqual(10, len(asset_types))
        self.assertEqual(11, asset_types[0].asset_type_id)

    def test_get_type_children(self):

        person_type: AssetType = AssetType(
            asset_name="Person",
            columns=[
                # Varchar and Text can be used interchangeably
                Column('name', 'name', DataTypes.TEXT.value, required=True),
                Column('age', 'age', DataTypes.INTEGER.value, required=True),
                Column('city_of_birth', 'city_of_birth', DataTypes.VARCHAR.value, required=True)
            ]
        )
        created_person_type: AssetType = self.asset_type_manager.create_asset_type(person_type)

        # Each student is a person, but unlike other
        # people a student has a subject of study.
        student_type: AssetType = AssetType(
            asset_name="Student",
            columns=[
                Column('subject', 'subject', DataTypes.VARCHAR.value, required=True)
            ],
            super_type=created_person_type.asset_type_id
        )
        created_student_type: AssetType = self.asset_type_manager.create_asset_type(student_type)

        professor_type: AssetType = AssetType(
            asset_name="Professor",
            columns=[
                Column('faculty', 'faculty', DataTypes.VARCHAR.value, required=True)
            ],
            super_type=created_person_type.asset_type_id
        )
        created_professor_type: AssetType = self.asset_type_manager.create_asset_type(professor_type)

        children = self.asset_type_manager.get_type_children(created_person_type)

        self.assertEqual(children, [created_student_type, created_professor_type])

    def create_twenty_samples(self):

        for iterator in range(0, 10):
            asset_type = deepcopy(self.asset_type)
            asset_type.asset_name = f"{asset_type.asset_name}_{iterator}"
            self.asset_type_manager.create_asset_type(asset_type)

        self.assertEqual(10, len(self.asset_type_manager.get_all()))

        for iterator in range(10, 20):
            asset_type = deepcopy(self.asset_type)
            asset_type.asset_name = f"{asset_type.asset_name}_{iterator}"
            asset_type.super_type = 1
            self.asset_type_manager.create_asset_type(asset_type)

    def test_get_one(self):
        self.asset_type = self.asset_type_manager.create_asset_type(self.asset_type)
        asset_type = self.asset_type_manager.get_one_by_id(1)
        self.assertEqual(self.asset_type, asset_type)

    def test__check_asset_type_consistency(self):
        self.asset_type = self.asset_type_manager.create_asset_type(self.asset_type)
        asset_type = self.asset_type_manager.get_one_by_id(1)
        self.asset_type.asset_type_id = 1
        self.asset_type.asset_table_name = 'abasset_table_testasset'
        self.assertEqual(self.asset_type, asset_type)
        self.db_connection.delete_table(self.asset_type.asset_table_name)
        self.assertRaises(AssetTypeInconsistencyException, self.asset_type_manager._check_asset_type_consistency)

    def test_jsonable(self):
        self.asset_type = self.asset_type_manager.create_asset_type(self.asset_type)

        json.dumps(self.asset_type.as_dict())
