"""
:Author: PDT
:Since: 2020/06/12

This is the module for the ``AssetTypePageManager``.
"""
from asset import AssetType
from database import Column, DataTypes
from database.sqlite_connection import SqliteConnection
from pages import AssetTypePage


class AssetTypePageManager:
    """This is the ``AssetTypePageManager``."""

    def __init__(self):
        """Create a new ``AssetTypePageManager``."""

        self.asset_type_layout_table_name = 'abintern_asset_type_layouts'
        self.asset_type_plugin_table_name = 'abintern_asset_type_plugins'

        self.db_connection = SqliteConnection.get()

    def create_page(self, asset_page: AssetTypePage):
        """Create a new ``AssetPage`` in the database."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        # TODO
        pass

    def delete_page(self, asset_type: AssetType):
        """Delete the ``AssetPage`` of a given ``asset_type``."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        # TODO
        pass

    def update_page(self, asset_page: AssetTypePage):
        """Update an ``AssetPage`` in the database."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        # TODO
        pass

    def check_page_exists(self, asset_type: AssetType):
        """Check if an ``AssetPage`` for ``asset_type`` exists in the database."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        # TODO
        pass

    def get_page(self, asset_type: AssetType):
        """Get the ``AssetPage`` for ``asset_type`` from the database"""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        # TODO
        pass

    def get_editor(self, asset_type: AssetType):
        """Get the editor for a given ``asset_type``."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        # TODO
        pass

    #####################
    #  PRIVATE METHODS  #
    #####################

    def _init_page_layout_tables(self):
        """Initialize required tables in the database."""

        if not self.db_connection.check_table_exists(self.asset_type_layout_table_name):
            columns = [
                # The column primary_key will be created automatically
                Column('asset_type_id', DataTypes.INTEGER, True),
                Column('page_layout_macro', DataTypes.VARCHAR, True),
                Column('created', DataTypes.DATETIME, True)
            ]
            self.db_connection.create_table(self.asset_type_layout_table_name, columns)

        if not self.db_connection.check_table_exists(self.asset_type_plugin_table_name):
            columns = [
                # The column primary_key will be created automatically
                Column('page_layout_id', DataTypes.INTEGER, True),
                Column('plugin_macro', DataTypes.VARCHAR, True),
                Column('position_in_layout', DataTypes.INTEGER, True),
                Column('employed_columns', DataTypes.VARCHAR, True),
                Column('created', DataTypes.VARCHAR, True)
            ]
            self.db_connection.create_table(self.asset_type_plugin_table_name, columns)
