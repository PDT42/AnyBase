"""
:Author: PDT
:Since: 2020/08/26

This is the abstract super class for a APluginServer. A APluginServer
works basically just the same as the Asset and AssetType Servers do.
It is a singleton, that provides static methods alongside an
initialization method, that binds these static methods to routes.
"""

from abc import abstractmethod
from typing import Any
from typing import Dict
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
from exceptions.asset import AssetTypeDoesNotExistException
from exceptions.database import MissingValueException
from exceptions.server import ServerAlreadyInitializedError
from plugins import PluginType


class APluginServer:
    """This is a ``APluginServer``."""

    # Make this a singleton
    _instance: 'APluginServer' = None
    _initialized: bool = False

    # Required Managers
    asset_manager: AAssetManager = None
    asset_type_manager: AAssetTypeManager = None

    # Variables

    # Map to hold info on the plugins served by this server
    # AssetTypeId, AssetId -> (InternalTypeName, AssetTypeId)
    table_mappings: Dict[Tuple[int, Optional[int]], Dict[str, int]] = None

    # Constants
    PLUGIN_NAME: str
    PLUGIN_TYPE: PluginType

    @staticmethod
    @abstractmethod
    def get() -> 'APluginServer':
        """Get the instance of this singleton."""
        pass

    @abstractmethod
    def initialize(self, asset_type: AssetType, asset: Asset = None) -> MutableMapping[str, str]:
        """Initialize everything this server requires."""
        pass

    @staticmethod
    def _generate_plugin_asset_name(plugin_name: str, asset_type_id: int, asset_id: int = None) -> str:
        """Generate an appropriate asset_name for a given plugin."""

        plugin_name = plugin_name.replace('-', '_').lower()

        asset_name: str = f'{plugin_name}_at{asset_type_id}'
        asset_name += f'_a{asset_id}' if asset_id else ''

        return asset_name

    def as_dict(self):
        """Get a dict representation of the server."""

        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def register_routes(cls, app):
        """Register the routes of this server in the ``app``."""

        # TODO: Implement this as a class method of the parent class?
        if cls.get()._initialized:
            raise ServerAlreadyInitializedError("AssetServer already initialized!")

        if cls.get().PLUGIN_TYPE in [PluginType.ASSET_TYPE, PluginType.HYBRID]:
            # Create name and url based on PLUGIN_NAME.
            asset_type_post_rule_url = f'/asset-type:<int:asset_type_id>/{cls.PLUGIN_NAME}/create-plugin-asset'
            asset_type_post_rule_name = f'post-create-asset-{cls.PLUGIN_NAME}'
            asset_type_post_rule_outlet = cls.post_create_plugin_asset

            # Add the rule to the app.

            app.add_url_rule(
                asset_type_post_rule_url,
                asset_type_post_rule_name,
                asset_type_post_rule_outlet,
                methods=['POST'])

        if cls.get().PLUGIN_TYPE in [PluginType.ASSET, PluginType.HYBRID]:
            # Create name and url based on PLUGIN_NAME.
            asset_post_rule_url = f'/asset-type:<int:asset_type_id>/asset:<int:asset_id>' \
                                  f'/{cls.PLUGIN_NAME}/create-note'
            asset_post_rule_name = f'post-create-asset-type-{cls.PLUGIN_NAME}'
            asset_post_rule_outlet = cls.post_create_plugin_asset

            # Add the rule to the app.

            app.add_url_rule(
                asset_post_rule_url,
                asset_post_rule_name,
                asset_post_rule_outlet,
                methods=['POST'])

        # Finally set the initialized flag of this singleton.
        cls.get()._initialized = True

    @classmethod
    async def post_create_plugin_asset(cls, asset_type_id: int, asset_id: int = None):
        """Handle POST requests to ``post-create-{_generate_plugin_asset_name}``."""

        # TODO: Put this into abstract plugin?
        # Getting the id of the table the notes
        # on this asset/type are stored in.
        item_key: str = cls._generate_plugin_asset_name(
            cls.PLUGIN_NAME, asset_type_id, asset_id)
        plugin_asset_type_id: int = cls.get() \
            .table_mappings[asset_type_id, asset_id][item_key]

        # Using it to get the notes asset type.
        asset_type_manager: AssetTypeManager = AssetTypeManager()
        plugin_asset_type: AssetType = asset_type_manager \
            .get_one_by_id(plugin_asset_type_id)

        # Check if an asset type with the specified type exists
        if not plugin_asset_type:
            return AssetTypeDoesNotExistException(
                f"Error in Post to 'post-create-' - "
                f"There is no AssetType with the the id: {asset_type_id}!")

        sync_form = await request.form
        plugin_asset_data: MutableMapping[str, Any] = {}

        for field in plugin_asset_type.columns:

            if field_data := sync_form.get(field.db_name):
                plugin_asset_data[field.db_name] = field_data

            elif not field.required:
                continue

            else:
                raise MissingValueException(
                    f"The field {field.db_name} is missing in the received form!")

        # Init new Asset and store it in the database
        plugin_asset = Asset(data=plugin_asset_data)

        asset_manager: AssetManager = AssetManager()
        asset_manager.create_asset(plugin_asset_type, plugin_asset)

        # Redirecting to the page this plugin is used in
        redirect_url = f'/asset-type:{asset_type_id}'
        if asset_id:
            redirect_url = f'{redirect_url}/asset:{asset_id}'

        return redirect(redirect_url)
