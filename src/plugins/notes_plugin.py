"""
:Author: PDT
:Since: 2020/08/26

This is the NotesPluginServer. It does stuff TODO: ╰(*°▽°*)╯.
"""

from typing import Any
from typing import Dict
from typing import Mapping
from typing import MutableMapping
from typing import Optional
from typing import Tuple

from quart import redirect
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
from exceptions.database import MissingValueException
from exceptions.server import ServerAlreadyInitializedError
from plugins.abstract_plugin import APluginServer


class NotesPluginServer(APluginServer):
    """This is the ``NotesPluginServer``."""

    _instance: 'NotesPluginServer' = None
    _initialized: bool = False

    PLUGIN_NAME = 'basic-notes'

    # Map to hold info on the plugins served by this server
    # AssetTypeId, AssetId -> (InternalTypeName, AssetTypeId)

    table_mappings: Dict[Tuple[int, Optional[int]], Dict[str, int]] = None

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

    @staticmethod
    def register_routes(app):
        """Register the routes of this server in the ``app``."""

        if NotesPluginServer.get()._initialized:
            raise ServerAlreadyInitializedError("AssetServer already initialized!")

        # Create name and url based on PLUGIN_NAME.
        asset_type_post_rule_url = f'/asset-type:<int:asset_type_id>/' \
                                   f'{NotesPluginServer.PLUGIN_NAME}/create-note'
        asset_type_post_rule_name = f'post-create-asset-{NotesPluginServer.PLUGIN_NAME}'
        asset_type_post_rule_outlet = NotesPluginServer.post_create_note

        # Add the rule to the app.

        app.add_url_rule(
            asset_type_post_rule_url,
            asset_type_post_rule_name,
            asset_type_post_rule_outlet,
            methods=['POST'])

        # Create name and url based on PLUGIN_NAME.
        asset_post_rule_url = f'/asset-type:<int:asset_type_id>/asset:<int:asset_id>' \
                              f'/{NotesPluginServer.PLUGIN_NAME}/create-note'
        asset_post_rule_name = f'post-create-asset-type-{NotesPluginServer.PLUGIN_NAME}'
        asset_post_rule_outlet = NotesPluginServer.post_create_note

        # Add the rule to the app.

        app.add_url_rule(
            asset_post_rule_url,
            asset_post_rule_name,
            asset_post_rule_outlet,
            methods=['POST'])

        # Finally set the initialized flag of this singleton.
        NotesPluginServer.get()._initialized = True

    def initialize(self, asset_type: AssetType, asset: Asset = None) -> Mapping[str, str]:
        """Initialize the Plugins requirements"""

        # Generate the id of this plugins private assets
        notes_type_name: str = self._generate_plugin_asset_name(
            self.PLUGIN_NAME, asset_type, asset)

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
            "notes": notes_asset_type.asset_type_id
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

        create_action: str = f'/asset-type:{asset_type.asset_type_id}'
        if asset is not None and isinstance(asset, Asset):
            create_action = f'{create_action}/asset:{asset.asset_id}'
        create_action = f'{create_action}/{NotesPluginServer.PLUGIN_NAME}/create-note'

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
            'create-note': create_action
        }

        return action_mappings

    @staticmethod
    async def post_create_note(asset_type_id: int, asset_id: int = None):
        """Handle POST requests to ``post-create-{PLUGIN_NAME}``"""

        # Getting the id of the table the notes
        # on this asset/type are stored in.
        notes_type_id: int = NotesPluginServer.get() \
            .table_mappings[asset_type_id, asset_id]['notes']

        # Using it to get the notes asset type.
        asset_type_manager: AssetTypeManager = AssetTypeManager()
        notes_type: AssetType = asset_type_manager \
            .get_one_by_id(notes_type_id)

        # Check if an asset type with the specified type exists
        if not notes_type:
            return AssetTypeDoesNotExistException(
                f"Error in Post to 'post-create-[PLUGIN_NAME]' - "
                f"There is no AssetType with the the id: {asset_type_id}!")

        sync_form = await request.form
        note_data: MutableMapping[str, Any] = {}

        for field in notes_type.columns:

            if field_data := sync_form.get(field.db_name):
                note_data[field.db_name] = field_data

            elif not field.required:
                continue

            else:
                raise MissingValueException(
                    f"The field {field.db_name} is missing in the received form!")

        # Init new Asset and store it in the database
        note_asset = Asset(data=note_data)

        asset_manager: AssetManager = AssetManager()
        asset_manager.create_asset(notes_type, note_asset)

        # Redirecting to the page this plugin is used in
        # TODO: This is should and should be done another way!
        redirect_url = f'/asset-type:{asset_type_id}'
        if asset_id:
            redirect_url = f'{redirect_url}/asset:{asset_id}'

        return redirect(redirect_url)
