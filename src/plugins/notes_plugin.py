"""
:Author: PDT
:Since: 2020/08/26

This is the NotesPluginServer. It does stuff TODO: ╰(*°▽°*)╯.
"""

from collections import MutableMapping

from asset import Asset
from asset.abstract_asset_manager import AAssetManager
from asset.asset_manager import AssetManager
from asset_type import AssetType
from asset_type.abstract_asset_type_manager import AAssetTypeManager
from asset_type.asset_type_manager import AssetTypeManager
from database import Column
from database import DataTypes
from exceptions.server import ServerAlreadyInitializedError
from plugins.abstract_plugin import APluginServer


class NotesPluginServer(APluginServer):
    """This is the ``NotesPluginServer``."""

    _instance: 'NotesPluginServer' = None
    _initialized: bool = False

    PLUGIN_NAME = 'basic-notes'

    # Urls to call this plugins actions
    action_mappings: MutableMapping[str, str] = {}

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

    @staticmethod
    def register_routes(app):
        """Register the routes of this server in the ``app``."""

        if NotesPluginServer.get()._initialized:
            raise ServerAlreadyInitializedError("AssetServer already initialized!")

        # Create rule and url based on PLUGIN_NAME.
        post_rule_url = f'/{NotesPluginServer.PLUGIN_NAME}/create-asset'
        post_rule_name = f'post-create-{NotesPluginServer.PLUGIN_NAME}'
        post_rule_outlet = NotesPluginServer.post_create_note

        # Add the rule to the app and to the plugins set of actions.
        app.add_url_rule(post_rule_url, post_rule_name, post_rule_outlet, methods=['POST'])
        NotesPluginServer.get().action_mappings[post_rule_name] = post_rule_url

        # Finally set the initialized flag of this singleton.
        NotesPluginServer.get()._initialized = True

    def initialize(self, asset_type: AssetType, asset: Asset = None):
        """Initialize the Plugins requirements"""

        # Generate the id of this plugins private assets
        notes_asset_name: str = self._generate_plugin_asset_name(
            self.PLUGIN_NAME, asset_type, asset)

        # Adding action mappings using functions of other servers

        self.action_mappings = {
            'stream-notes': f"/asset-type:{asset_type.asset_type_id}/stream/{notes_asset_name}",
        }

        if not self.asset_type_manager.check_asset_type_exists(notes_asset_name):
            notes_type: AssetType = AssetType(
                asset_name=notes_asset_name,
                columns=[
                    Column('title', 'title', DataTypes.VARCHAR.value, required=True),
                    Column('note', 'note', DataTypes.VARCHAR.value, required=True),
                    Column('author', 'author', DataTypes.VARCHAR.value, required=True)
                ], owner_id=asset_type.asset_type_id  # Notes have an owner
            )

            return self.asset_type_manager.create_asset_type(notes_type)

        # TODO: Store notes_asset_name
        return self.asset_type_manager.get_one_by_name(notes_asset_name)

    @staticmethod
    def post_create_note():
        """Handle POST requests to ``post-create-{PLUGIN_NAME}``"""


