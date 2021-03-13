"""
:Author: PDT
:Since: 2020/08/26

This is the NotesPluginServer. It does stuff TODO: ╰(*°▽°*)╯.
"""

from typing import Mapping
from typing import MutableMapping

from asset import Asset
from asset.abstract_asset_manager import AAssetManager
from asset.asset_manager import AssetManager
from asset_type import AssetType
from asset_type.abstract_asset_type_manager import AAssetTypeManager
from asset_type.asset_type_manager import AssetTypeManager
from database import Column
from database import DataTypes
from plugins import PluginType
from plugins.abstract_plugin import APluginServer


class NotesPluginServer(APluginServer):
    """This is the ``NotesPluginServer``."""

    _instance: 'NotesPluginServer' = None

    # This is the plugin name.
    # The names of plugins must unique
    # within the initialized plugins.
    PLUGIN_NAME = 'basic-notes'
    PLUGIN_TYPE = PluginType.HYBRID

    @staticmethod
    def get() -> 'NotesPluginServer':
        """Get the instance of this singleton."""

        if not NotesPluginServer._instance:
            NotesPluginServer._instance = NotesPluginServer()
        return NotesPluginServer._instance

    def __init__(self):
        """Create a new ``NotesPluginServer``."""

        self.asset_type_manager: AAssetTypeManager = AssetTypeManager()
        self.asset_manager: AAssetManager = AssetManager()

        self.table_mappings = {}

    def as_dict(self):
        """Get a dict rep of the plugin."""

        raise NotImplementedError()

    def initialize(self, asset_type: AssetType, asset: Asset = None) -> Mapping[str, str]:
        """Initialize the Plugins requirements"""

        # Generate the id of this plugins private assets
        notes_type_name: str = self._generate_plugin_asset_name(
            self.PLUGIN_NAME, asset_type.asset_type_id, None)

        if asset is not None and isinstance(asset, Asset):
            notes_type_name = self._generate_plugin_asset_name(
                self.PLUGIN_NAME, asset_type.asset_type_id, asset.asset_id)

        # CHECKOUT: Do this with one asset type and a per
        # CHECKOUT: note asset 'on topic' reference.
        # CHECKOUT: This would probably make the database
        # CHECKOUT: less messy, but would it provide any
        # CHECKOUT: advantages? ㄟ(≧◇≦)ㄏ

        # Create the required note asset_type if required
        if not self.asset_type_manager.check_asset_type_exists(notes_type_name):
            # Define the type of the notes asset for this asset/type
            notes_type: AssetType = AssetType(
                asset_name=notes_type_name,
                columns=[
                    Column('title', 'title', DataTypes.VARCHAR.value, required=True),
                    Column('note', 'note', DataTypes.VARCHAR.value, required=True),
                    Column('author', 'author', DataTypes.VARCHAR.value, required=False)
                ], owner_id=asset_type.asset_type_id  # Notes have an owner
            )

            self.asset_type_manager.create_asset_type(notes_type)

        notes_asset_type: AssetType = self.asset_type_manager \
            .get_one_by_name(notes_type_name)

        # Adding table mappings.
        self.table_mappings[asset_type.asset_type_id, asset.asset_id if asset else None] = {
            notes_type_name: notes_asset_type.asset_type_id
        }

        # NOTE: The action mappings a plugin hands to the server
        # NOTE: represent a catalog of actions. The key of the
        # NOTE: mapping is the name of the action, the url that
        # NOTE: must be called to execute the action. An action
        # NOTE: can either be executed by the asset/type server
        # NOTE: or by a plugin specific function. In the latter
        # NOTE: the plugin must register the actions url in its
        # NOTE: register_routes function. Stream actions, must
        # NOTE: be marked as such by using the prefix 'stream-'.

        # Create 'create' action mappings. We use the
        # mapping for post_create_note we registered
        # in the register routes static method.

        create_key: str = f'create-plugin-asset'
        create_action: str = f'/asset-type:{asset_type.asset_type_id}'
        if asset is not None and isinstance(asset, Asset):
            create_action = f'{create_action}/asset:{asset.asset_id}'
        create_action = f'{create_action}/{NotesPluginServer.PLUGIN_NAME}/create-{notes_type_name}'

        # Create an action that lets us stream assets
        # of the notes type from the server.
        # → We delegate this action to the asset_server
        # by using an url as the stream_notes_url,
        # that is registered in the asset_types server.

        stream_notes_key = f'stream-{notes_type_name}'
        stream_notes_url = f"/asset-type:{notes_asset_type.asset_type_id}" + \
                           f"/stream/stream-{notes_type_name}"

        # Adding action mappings.
        action_mappings: MutableMapping[str, str] = {
            stream_notes_key: stream_notes_url,
            create_key: create_action
        }

        return action_mappings
