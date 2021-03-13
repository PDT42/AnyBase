"""
:Author: PDT
:Since: 2020/08/27

These are tests for the ``NotesPluginServer``.
"""
from shutil import rmtree
from unittest import TestCase

from asset import Asset
from asset_type import AssetType
from asset.asset_manager import AssetManager
from asset_type.asset_type_manager import AssetTypeManager
from database import Column, DataTypes
from plugins import Plugin, PluginRegister
from plugins.notes_plugin import NotesPluginServer
from test.test_util import init_test_db


class TestAssetManager(TestCase):

    def setUp(self) -> None:
        """Set up before tests."""

        self.tempdir, self.db_connection = init_test_db()
        # print(f"Tempdir used in this tests: {self.tempdir}")

        # Initializing managers
        # ---------------------

        self.asset_type_manager: AssetTypeManager = AssetTypeManager()
        self.asset_manager: AssetManager = AssetManager()

        # Creating a new AssetType to create Notes on
        # -------------------------------------------

        self.asset_type = AssetType(
            asset_name='Person',
            columns=[
                Column('name', 'name', DataTypes.VARCHAR.value, required=True),
            ])
        self.asset_type = self.asset_type_manager.create_asset_type(self.asset_type)

        # Creating a new Asset to create Notes on
        # ---------------------------------------

        self.asset = Asset(
            asset_id=None,
            data={
                "name": "Olaf"
            })
        self.asset = self.asset_manager.create_asset(self.asset_type, self.asset)

        # Initializing a plugin for both Asset and AssetType
        # --------------------------------------------------

        plugin: Plugin = PluginRegister.BASIC_NOTES.value

        self.notes_server_at: NotesPluginServer = NotesPluginServer.get() \
            .initialize(plugin.name, self.asset_type)

        self.notes_server_a: NotesPluginServer = NotesPluginServer.get() \
            .initialize(plugin.name, self.asset_type, self.asset)

    def tearDown(self) -> None:
        """Clean up after each test."""

        self.db_connection.kill()
        rmtree(self.tempdir)
