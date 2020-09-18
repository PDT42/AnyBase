"""
:Author: PDT
:Since: 2020/08/14

These are tests for the PageManager.
"""
from shutil import rmtree
from typing import Any
from typing import MutableMapping
from unittest import TestCase

from asset import Asset
from asset.asset_manager import AssetManager
from asset_type import AssetType
from asset_type.asset_type_manager import AssetTypeManager
from database import Column
from database import DataTypes
from pages import ColumnInfo
from pages import PageLayout
from pages.abstract_page_manager import APageManager
from pages.page_manager import PageManager
from plugins import PluginRegister
from test.test_util import init_test_db


class TestPageManager(TestCase):

    def setUp(self) -> None:
        """Set up before tests."""

        self.tempdir, self.db_connection = init_test_db()
        # print(f"Tempdir used in this tests: {self.tempdir}")

        self.page_manager: APageManager = PageManager()
        self.asset_type_manager: AssetTypeManager = AssetTypeManager()
        self.asset_manager: AssetManager = AssetManager()

        self.asset_type = AssetType(
            'TestAsset',
            [
                Column('TestText', 'testtext', DataTypes.VARCHAR.value, required=True),
                Column('TestNumber', 'testnumber', DataTypes.NUMBER.value, required=True)
            ])
        self.asset_type_manager.create_asset_type(self.asset_type)
        self.asset_type = self.asset_type_manager.get_one_by_id(1)

        self.asset = Asset(asset_id=None, data={"testtext": "Test Asset Test", "testnumber": 5})
        self.asset_manager.create_asset(self.asset_type, self.asset)
        self.asset = self.asset_manager.get_one(1, self.asset_type)

        # Defining a Page Layout with asset_type_page = False
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.asset_type_layout: PageLayout = PageLayout(
            asset_type_id=self.asset_type.asset_type_id,
            asset_page_layout=False,
            layout=[[
                ColumnInfo(
                    plugin=PluginRegister.LIST_ASSETS.value,
                    field_mappings={'header': 'name'},
                    column_width=12,
                    column_id=0
                )]
            ], field_mappings={
                'header': 'name'
            }
        )

        self.asset_type_layout_row: MutableMapping[str, Any] = {
            'asset_type_id': 1,
            'asset_page_layout': 0,
            'layout': '{12, 0}',
            'field_mappings': "{'header': 'name'}",
            'created': None,
            'updated': None,
            'primary_key': None,
            'sources': None
        }

        # Defining a Page Layout with asset_type_page = True
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.asset_layout: PageLayout = PageLayout(
            asset_type_id=self.asset_type.asset_type_id,
            asset_page_layout=True,
            layout=[[
                ColumnInfo(
                    plugin=PluginRegister.ASSET_DETAILS.value,
                    column_width=12,
                    field_mappings={'header': 'name'},
                    column_id=1
                )]
            ], field_mappings={
                'header': 'name'
            })

        self.asset_layout_row: MutableMapping[str, Any] = {
            'asset_type_id': 1,
            'asset_page_layout': 1,
            'layout': '{12, 1}',
            'field_mappings': "{'header': 'name'}",
            'created': None,
            'updated': None,
            'primary_key': None,
            'sources': None
        }

    def tearDown(self) -> None:
        """Clean up after each test."""
        self.db_connection.kill()
        rmtree(self.tempdir)

    def test_convert_layout_to_row(self):
        """Test superclass method ``convert_layout_to_row``."""

        asset_type_layout_row = self.page_manager \
            .convert_layout_to_row(self.asset_type_layout)

        self.asset_type_layout_row['created'] = asset_type_layout_row['created']
        self.asset_type_layout_row['updated'] = asset_type_layout_row['updated']

        self.assertEqual(
            asset_type_layout_row,
            self.asset_type_layout_row
        )

        asset_layout_row = self.page_manager \
            .convert_layout_to_row(self.asset_layout)

        self.assertEqual(
            asset_layout_row,
            self.asset_layout_row
        )

    def test_create_page_get_page(self):
        """Test Create Page."""

        created_asset_type_layout: PageLayout = self.page_manager \
            .create_page(self.asset_type_layout)

        gotten_asset_type_layout: PageLayout = self.page_manager \
            .get_page(self.asset_type.asset_type_id, False)

        # Let's not compare timestamps
        gotten_asset_type_layout.created = created_asset_type_layout.created
        gotten_asset_type_layout.updated = created_asset_type_layout.updated

        self.assertEqual(
            gotten_asset_type_layout,
            created_asset_type_layout
        )

    def test_delete_page(self):
        """Test delete_page."""

        created_asset_type_layout: PageLayout = self.page_manager \
            .create_page(self.asset_type_layout)

        self.assertTrue(self.page_manager.check_page_exists(1, False))

        gotten_asset_type_layout: PageLayout = self.page_manager \
            .get_page(self.asset_type.asset_type_id, False)

        # Let's not compare timestamps
        gotten_asset_type_layout.created = created_asset_type_layout.created
        gotten_asset_type_layout.updated = created_asset_type_layout.updated

        self.assertEqual(
            gotten_asset_type_layout,
            created_asset_type_layout
        )

        self.page_manager.delete_page(1, False)
        self.assertFalse(self.page_manager.check_page_exists(1, False))

    def test_update_page(self):
        """Test update_page."""

        created_asset_type_layout: PageLayout = self.page_manager \
            .create_page(self.asset_type_layout)

        self.assertTrue(self.page_manager.check_page_exists(1, False))

        gotten_asset_type_layout: PageLayout = self.page_manager \
            .get_page(self.asset_type.asset_type_id, False)

        self.assertEqual(gotten_asset_type_layout, created_asset_type_layout)

        gotten_asset_type_layout.field_mappings['header'] = "updated"

        self.page_manager.update_page(gotten_asset_type_layout)

        updated_asset_type_layout: PageLayout = self.page_manager \
            .get_page(self.asset_type.asset_type_id, False)

        self.assertEqual(updated_asset_type_layout, gotten_asset_type_layout)
