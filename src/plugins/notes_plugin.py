"""
:Author: PDT
:Since: 2020/08/26

This is the NotesPluginServer. It does stuff TODO.
"""

from asset import Asset
from asset_type import AssetType
from asset.abstract_asset_manager import AAssetManager
from asset_type.abstract_asset_type_manager import AAssetTypeManager
from asset.asset_manager import AssetManager
from asset_type.asset_type_manager import AssetTypeManager
from database import Column, DataTypes
from plugins.abstract_plugin import APluginServer


class NotesPluginServer(APluginServer):
    """This is the ``NotesPluginServer``."""

    _instance: 'NotesPluginServer' = None

    table_mappings = None

    @staticmethod
    def get() -> 'NotesPluginServer':
        """Get the instance of this singleton."""

        if not NotesPluginServer._instance:
            NotesPluginServer._instance = NotesPluginServer()
        return NotesPluginServer._instance

    def __init__(self):
        """Create a new ``NotesPluginServer``."""

        self.asset_manager: AAssetManager = AssetManager()
        self.asset_type_manager: AAssetTypeManager = AssetTypeManager()

    def initialize(self, plugin_name: str, asset_type: AssetType, asset: Asset = None):
        """Initialize the Plugins requirements"""

        notes_asset_name: str = self._generate_plugin_asset_name(
            plugin_name, asset_type, asset)

        if not self.asset_type_manager.check_asset_type_exists(notes_asset_name):

            notes_type: AssetType = AssetType(
                asset_name=notes_asset_name,
                columns=[
                    Column('title', 'title', DataTypes.VARCHAR.value, required=True),
                    Column('note', 'note', DataTypes.VARCHAR.value, required=True),
                    Column('author', 'author', DataTypes.VARCHAR.value, required=True)
                ], owner_id=asset_type.asset_type_id
            )

            notes_type = self.asset_type_manager.create_asset_type(notes_type)

        else:
            notes_type = self.asset_type_manager.get_one_by_name(notes_asset_name)

        return notes_type
