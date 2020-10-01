"""
:Author: PDT
:Since: 2020/09/30

This is the CalendarServer. All hail Gregor.
"""

from typing import MutableMapping

from asset import Asset
from asset_type import AssetType
from plugins.abstract_booking_plugin import ABookingPlugin


class CalendarServer(ABookingPlugin):
    """This is the ``CalendarServer``."""

    _instance: 'CalendarServer' = None

    @staticmethod
    def get() -> 'CalendarServer':
        """Get the instance of this singleton."""

        if not CalendarServer._instance:
            CalendarServer._instance = CalendarServer()
        return CalendarServer._instance

    @staticmethod
    def register_routes(app) -> None:
        """Register the routes of this server in the ``app``."""
        pass

    def initialize(self, asset_type: AssetType, asset: Asset = None) -> MutableMapping[str, str]:
        """Initialize the Plugins requirements."""
        pass
