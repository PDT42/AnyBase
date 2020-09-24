"""
:Author: PDT
:Since: 2020/08/26

This is the abstract super class for a APluginServer. A APluginServer
works basically just the same as the Asset and AssetType Servers do.
It is a singleton, that provides static methods alongside an
initialization method, that binds these static methods to routes.
"""

from abc import abstractmethod
from typing import MutableMapping

from asset import Asset
from asset.abstract_asset_manager import AAssetManager
from asset_type import AssetType
from asset_type.abstract_asset_type_manager import AAssetTypeManager


class APluginServer:
    """This is a ``APluginServer``."""

    _instance: 'APluginServer' = None

    asset_manager: AAssetManager = None
    asset_type_manager: AAssetTypeManager = None

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
    def _generate_plugin_asset_name(plugin_name: str, asset_type: AssetType, asset: Asset = None) -> str:
        """Generate an appropriate asset_name for a given plugin."""

        plugin_name = plugin_name.replace('-', '_').lower()

        asset_name: str = f'{plugin_name}_at{asset_type.asset_type_id}'
        asset_name += f'a{asset.asset_id}' if asset else ''

        return asset_name

    def as_dict(self):
        """Get a dict representation of the server."""
