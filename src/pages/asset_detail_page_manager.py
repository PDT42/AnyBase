"""
:Author: PDT
:Since: 2020/06/12

This is the module for the ``AssetDetailPageManager``. It is responsible for storing, granting access on, updating etc.
information regarding the ``PageLayouts`` of AssetDetail Pages. It's supposed to translate AssetData into render ready
html pages.
"""
from asset import Asset
from database.db_connection import DbConnection
from pages import AssetDetailPage


class AssetDetailPageManager:
    """This is the ``AssetDetailPageManager``."""

    def __init__(self):
        """Create a new ``AssetDetailPageManager``."""

        self.db_connection = DbConnection.get()

    def create_page(self, asset_detail_page: AssetDetailPage):
        """Create an ``AssetDetailPage`` in the database."""
        # TODO
        pass

    def delete_page(self, asset: Asset):
        """Delete the ``AssetDetailPage`` of a give ``asset``."""
        # TODO
        pass

    def update_page(self, asset_detail_page: AssetDetailPage):
        """Update the ``asset_detail_page`` in the database."""
        # TODO
        pass

    def check_page_exists(self, asset: Asset):
        """Check if an ``AssetDetailPage`` exists for a given ``asset``."""
        # TODO
        pass

    def get_page(self, asset: Asset):
        """Get the ``AssetDetailPage`` for a given ``asset``."""
        # TODO
        pass

    def get_editor(self, asset: Asset):
        """Get the editor for ``AssetDetailPages``."""
        # TODO
        pass
