"""
:Author: PDT
:Since: 2020/06/12

This is the module for the ``AssetPageManager``.
"""
from asset import AssetType
from database.db_connection import DbConnection
from pages import AssetPage


class AssetPageManager:
    """This is the ``AssetPageManager``."""

    def __init__(self):
        """Create a new ``AssetPageManager``."""

        self.db_connection = DbConnection.get()

    def create_page(self, asset_page: AssetPage):
        """Create a new ``AssetPage`` in the database."""
        # TODO
        pass

    def delete_page(self, asset_type: AssetType):
        """Delete the ``AssetPage`` of a given ``asset_type``."""
        # TODO
        pass

    def update_page(self, asset_page: AssetPage):
        """Update an ``AssetPage`` in the database."""
        # TODO
        pass

    def check_page_exists(self, asset_type: AssetType):
        """Check if an ``AssetPage`` for ``asset_type`` exists in the database."""
        # TODO
        pass

    def get_page(self, asset_type: AssetType):
        """Get the ``AssetPage`` for ``asset_type`` from the database"""
        # TODO
        pass

    def get_editor(self, asset_type: AssetType):
        """Get the editor for a given ``asset_type``."""
        # TODO
        pass
