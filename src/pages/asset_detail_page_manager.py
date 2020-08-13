"""
:Author: PDT
:Since: 2020/06/12

This is the module for the ``AssetDetailPageManager``. It is responsible for storing, granting access on, updating etc.
information regarding the ``PageLayouts`` of AssetDetail Pages. It's supposed to translate AssetData into render ready
html pages.
"""

from asset import Asset, AssetType
from database.db_connection import DbConnection
from pages import AssetDetailPage, AssetTypePage
from pages.abstract_page_manager import APageManager


class AssetDetailPageManager(APageManager):
    """This is the ``AssetDetailPageManager``."""

    def create_page(self, asset_page: AssetTypePage):
        """Create a new ``AssetPage`` in the database."""
        pass

    def delete_page(self, asset_type: AssetType):
        """Delete the ``AssetPage`` of a given ``asset_type_id``."""
        pass

    def update_page(self, asset_page: AssetTypePage):
        """Update an ``AssetPage`` in the database."""
        pass

    def check_page_exists(self, asset_type: AssetType):
        """Check if an ``AssetPage`` for ``asset_type_id`` exists in the database."""
        pass

    def get_page(self, asset_type: AssetType):
        """Get the ``AssetPage`` for ``asset_type_id`` from the database"""
        pass

    def get_editor(self, asset_type: AssetType):
        """Get the editor for a given ``asset_type_id``."""
        pass

