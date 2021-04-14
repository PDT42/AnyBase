"""
:Author: PDT
:Since: 2020/09/30

This is the CalendarServer. All hail Gregor.
"""

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
from plugins.abstract_booking_plugin import ABookingPlugin


class CalendarServer(ABookingPlugin):
    """This is the ``CalendarServer``."""

    _instance: 'CalendarServer' = None

    # This is the plugin name.
    # The names of plugins must unique
    # within the initialized plugins.
    PLUGIN_NAME = 'basic-calendar'
    PLUGIN_TYPE = PluginType.HYBRID

    @staticmethod
    def get() -> 'CalendarServer':
        """Get the instance of this singleton."""

        if not CalendarServer._instance:
            CalendarServer._instance = CalendarServer()
        return CalendarServer._instance

    def __init__(self):
        """Create a new ``CalendarServer``."""

        self.asset_type_manager: AAssetTypeManager = AssetTypeManager()
        self.asset_manager: AAssetManager = AssetManager()

        self.table_mappings = {}

    def as_dict(self):
        """Get a dict rep of the plugin."""

        raise NotImplementedError()

    def initialize(self, asset_type: AssetType, asset: Asset = None) -> MutableMapping[str, str]:
        """Initialize the Plugins requirements."""

        appointment_type_name: str = self._generate_plugin_asset_name(
            self.PLUGIN_NAME, asset_type.asset_type_id, asset)

        if not self.asset_type_manager.check_asset_type_exists(appointment_type_name):
            # Define the type of the appointment asset for this asset/type
            appointment_type: AssetType = AssetType(
                asset_name=appointment_type_name,
                columns=[
                    Column('title', 'title', DataTypes.VARCHAR.value, required=True),
                    Column('bookings', 'bookings', DataTypes.ASSETLIST.value, required=True)
                ], owner_id=asset_type.asset_type_id
            )

            self.asset_type_manager.create_asset_type(appointment_type)

        appointment_asset_type: AssetType = self.asset_type_manager \
            .get_one_by_name(appointment_type_name)

        # Create required mappings
        # ~~~~~~~~~~~~~~~~~~~~~~~~

        create_appointment_key: str = f'create-plugin-asset'
        create_action: str = f'/asset-type:{asset_type.asset_type_id}'
        if asset is not None and isinstance(asset, Asset):
            create_action = f'{create_action}/asset:{asset.asset_id}'
        create_appointment_url = f'{create_action}/{CalendarServer.PLUGIN_NAME}' + \
                                 f'/create-appointment'

        stream_appointments_key = f'stream-{appointment_type_name}'
        stream_appointments_url = f"/asset-type:{appointment_asset_type.asset_type_id}" + \
                                  f"/stream/stream-{appointment_type_name}"

        action_mappings: MutableMapping[str, str] = {
            stream_appointments_key: stream_appointments_url,
            create_appointment_key: create_appointment_url
        }

        return action_mappings
