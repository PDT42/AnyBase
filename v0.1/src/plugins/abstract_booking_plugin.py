"""
:Author: PDT
:Since: 2020/09/30

This is the abstract super class for plugin servers that employ bookings.
"""

from typing import MutableMapping

from quart import Quart

from asset import Asset
from asset_type import AssetType
from asset_type.abstract_asset_type_manager import AAssetTypeManager
from asset_type.asset_type_manager import AssetTypeManager
from database import DataTypes
from plugins.abstract_plugin import APluginServer


class ABookingPlugin(APluginServer):
    """This is ``ABookingPlugin``."""

    _instance: 'ABookingPlugin' = None
    _initialized: bool = False

    PLUGIN_NAME = 'a-booking-plugin'

    MAX_SUB_LOAD_DEPTH = 2

    @staticmethod
    def get() -> 'APluginServer':
        """Get the instance of this singleton."""

        if not ABookingPlugin._instance:
            ABookingPlugin._instance = ABookingPlugin()
        return ABookingPlugin._instance

    @staticmethod
    def register_routes(app: Quart) -> None:
        """Register this plugins routes in the app."""
        pass

    def initialize(self, asset_type: AssetType, asset: Asset = None) -> MutableMapping[str, str]:
        """Initialize the Plugins requirements."""

        asset_type_manager: AAssetTypeManager = AssetTypeManager()

        action_mappings: MutableMapping[str, str] = {}

        # Create a stream action mapping for each
        # Booking type a booking plugin could need
        # to stream in this asset types context.

        for column in asset_type.columns:
            if column.datatype in [DataTypes.ASSET.value, DataTypes.ASSETLIST.value]:
                column_type: AssetType = asset_type_manager.get_one_by_id(asset_type.booking_type_id)

                mapping_name: str = f'stream-booking-{column.asset_type_id}'
                mapping_url: str = ""

        return action_mappings
