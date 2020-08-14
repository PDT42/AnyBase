"""
:Author: PDT
:Since: 2020/08/14

These are tests for the PageManager.
"""
from shutil import rmtree
from typing import Any, Mapping
from unittest import TestCase

from asset import Asset, AssetType
from asset.asset_manager import AssetManager
from asset.asset_type_manager import AssetTypeManager
from database import Column, DataTypes
from pages import ColumnInfo, PageLayout
from pages.abstract_page_manager import APageManager
from pages.page_manager import PageManager
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
        self.asset_type = self.asset_type_manager.get_one(1)

        self.asset = Asset(asset_id=None, data={"testtext": "Test Asset Test", "testnumber": 5})
        self.asset_manager.create_asset(self.asset_type, self.asset)
        self.asset = self.asset_manager.get_one(1, self.asset_type)

        # Defining a Page Layout with asset = None
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.asset_type_layout: PageLayout = PageLayout(
            asset_type=self.asset_type,
            items_url=f'/asset-type/{self.asset_type.asset_type_id}/items',
            layout=[[
                ColumnInfo(
                    plugin_name='list-assets',
                    plugin_path='plugins/list-assets-plugin.html',
                    column_width=12,
                    employed_columns=['name'],
                    column_id=0
                )]
            ]
        )
        self.asset_type_layout_row: Mapping[str, Any] = {
            'primary_key': None,
            'items_url': '/asset-type/1/items',
            'asset_id': None,
            'asset_type_id': 1,
            'layout': '[{12, 0}]'
        }

        # Defining a Page Layout with asset = self.asset
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.asset_layout: PageLayout = PageLayout(
            asset_type=self.asset_type,
            items_url=f'/asset-type/{self.asset_type.asset_type_id}/items',
            asset=self.asset,
            layout=[[
                ColumnInfo(
                    plugin_name='list-assets',
                    plugin_path='plugins/list-assets-plugin.html',
                    column_width=12,
                    employed_columns=['name'],
                    column_id=0
                )]
            ]
        )
        self.asset_layout_row: Mapping[str, Any] = {
            'primary_key': None,
            'items_url': '/asset-type/1/items',
            'asset_id': 1,
            'asset_type_id': 1,
            'layout': '[{12, 0}]'
        }

    def tearDown(self) -> None:
        """Clean up after each test."""
        self.db_connection.kill()
        rmtree(self.tempdir)

    def test_convert_layout_to_row(self):
        """Test superclass method ``convert_layout_to_row``."""

        self.assertEqual(
            self.page_manager.convert_layout_to_row(self.asset_type_layout),
            self.asset_type_layout_row
        )
        self.assertEqual(
            self.page_manager.convert_layout_to_row(self.asset_layout),
            self.asset_layout_row
        )

    def test_create_page_get_page(self):
        """Test Create Page."""

        self.asset_type_layout.layout_id = self.page_manager.create_page(self.asset_type_layout)
        self.assertEqual(self.page_manager.get_page(self.asset_type), self.asset_type_layout)

