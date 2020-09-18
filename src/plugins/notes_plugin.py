"""
:Author: PDT
:Since: 2020/08/26

This is the NotesPluginServer. It does stuff TODO: ╰(*°▽°*)╯.
"""

from copy import deepcopy
from typing import Any
from typing import Dict
from typing import Mapping
from typing import MutableMapping
from typing import Optional
from typing import Tuple

from quart import request

from asset import Asset
from asset.abstract_asset_manager import AAssetManager
from asset.asset_manager import AssetManager
from asset_type import AssetType
from asset_type.abstract_asset_type_manager import AAssetTypeManager
from asset_type.asset_type_manager import AssetTypeManager
from database import Column
from database import DataTypes
from exceptions.asset import AssetTypeDoesNotExistException
from exceptions.server import ServerAlreadyInitializedError
from plugins.abstract_plugin import APluginServer


class NotesPluginServer(APluginServer):
    """This is the ``NotesPluginServer``."""

    _instance: 'NotesPluginServer' = None
    _initialized: bool = False

    PLUGIN_NAME = 'basic-notes'

    # Urls to call this plugins actions
    action_mappings: MutableMapping[str, str] = None

    # Map to hold info on the plugins served by this server
    # AssetTypeId, AssetId -> InternalTypeName, AssetTypeId

    table_mappings: Dict[Tuple[int, Optional[int]], Dict[str, int]] = None

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

        self.action_mappings = {}
        self.table_mappings = {}

    @staticmethod
    def register_routes(app):
        """Register the routes of this server in the ``app``."""

        if NotesPluginServer.get()._initialized:
            raise ServerAlreadyInitializedError("AssetServer already initialized!")

        # Create name and url based on PLUGIN_NAME.
        asset_type_post_rule_url = f'/asset-type:<asset_type_id: int>/' \
                                   f'{NotesPluginServer.PLUGIN_NAME}/create-note'
        asset_type_post_rule_name = f'post-create-asset-{NotesPluginServer.PLUGIN_NAME}'
        asset_type_post_rule_outlet = NotesPluginServer.post_create_note

        # Add the rule to the app and to the plugins set of actions.

        app.add_url_rule(
            asset_type_post_rule_url,
            asset_type_post_rule_name,
            asset_type_post_rule_outlet,
            methods=['POST'])
        NotesPluginServer.get().action_mappings[asset_type_post_rule_name] = \
            asset_type_post_rule_url

        # Create name and url based on PLUGIN_NAME.
        asset_post_rule_url = f'/asset-type:<asset_type_id: int>/asset:<asset_id: int>' \
                              f'/{NotesPluginServer.PLUGIN_NAME}/create-note'
        asset_post_rule_name = f'post-create-asset-type-{NotesPluginServer.PLUGIN_NAME}'
        asset_post_rule_outlet = NotesPluginServer.post_create_note

        # Add the rule to the app and to the plugins set of actions.

        app.add_url_rule(
            asset_post_rule_url,
            asset_post_rule_name,
            asset_post_rule_outlet,
            methods=['POST'])
        NotesPluginServer.get().action_mappings[asset_type_post_rule_name] = \
            asset_type_post_rule_url

        # Finally set the initialized flag of this singleton.
        NotesPluginServer.get()._initialized = True

    def initialize(self, asset_type: AssetType, asset: Asset = None) -> Mapping[str, str]:
        """Initialize the Plugins requirements"""

        # Generate the id of this plugins private assets
        notes_type_name: str = self._generate_plugin_asset_name(
            self.PLUGIN_NAME, asset_type, asset)

        # Define the type of the notes asset for this asset/type
        notes_type: AssetType = AssetType(
            asset_name=notes_type_name,
            columns=[
                Column('title', 'title', DataTypes.VARCHAR.value, required=True),
                Column('note', 'note', DataTypes.VARCHAR.value, required=True),
                Column('author', 'author', DataTypes.VARCHAR.value, required=True)
            ], owner_id=asset_type.asset_type_id  # Notes have an owner
        )

        if not self.asset_type_manager.check_asset_type_exists(notes_type_name):
            self.asset_type_manager.create_asset_type(notes_type)

        notes_asset_type: AssetType = self.asset_type_manager \
            .get_one_by_name(notes_type_name)

        # Adding table mapping
        self.table_mappings[asset_type.asset_type_id, asset.asset_id] = {
            "notes": notes_asset_type.asset_type_id
        }

        # Adding action mappings that use functions of other servers
        action_mappings = deepcopy(NotesPluginServer.action_mappings)
        action_mappings['stream-notes'] = \
            f"/asset-type:{asset_type.asset_type_id}/stream/{notes_type_name}"

        return action_mappings

    @staticmethod
    async def post_create_note(asset_type_id: int, asset_id: int = None):
        """Handle POST requests to ``post-create-{PLUGIN_NAME}``"""

        asset_type_manager: AssetTypeManager = AssetTypeManager()

        notes_type_id: int = NotesPluginServer.get() \
            .table_mappings[asset_type_id, asset_id]['notes']
        notes_type: AssetType = asset_type_manager \
            .get_one_by_id(notes_type_id)

        # Check if an asset type with the specified type exists
        if not notes_type:
            return AssetTypeDoesNotExistException(
                f"Error in Post to 'post-create-asset-type-[PLUGIN_NAME]'. "
                f"There is no AssetType with the the id: {asset_type_id}!")

        sync_form = await request.form
        note_data: MutableMapping[str, Any] = {}

        for field in notes_type.columns:
            note_data[field.db_name] = sync_form[field.db_name]

        # Init new Asset and store it in the database
        note_asset = Asset(data=note_data)

        asset_manager: AssetManager = AssetManager()
        asset_manager.create_asset(notes_type, note_asset)
