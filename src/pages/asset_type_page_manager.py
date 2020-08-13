"""
:Author: PDT
:Since: 2020/06/12

This is the module for the ``AssetTypePageManager``.
"""
from typing import Any, List, Mapping

from asset import AssetType
from asset.asset_type_manager import AssetTypeManager
from database import Column, DataTypes
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from exceptions.asset import AssetTypeDoesNotExistException
from exceptions.plugins import PageDoesNotExistException
from pages import AssetTypePage, ColumnInfo
from pages.abstract_page_manager import APageManager


class AssetTypePageManager(APageManager):
    """This is the ``AssetTypePageManager``."""

    asset_type_layout_table_name: str = 'abintern_asset_type_layouts'
    asset_type_layout_table_columns: List[str] = [
        'primary_key',
        'item_id',
        'layout'
    ]
    asset_type_plugin_table_name: str = 'abintern_asset_type_plugins'
    asset_type_plugin_table_columns: List[str] = [
        'primary_key',
        'plugin_name',
        'plugin_path',
        'column_width',
        'employed_columns'
    ]

    db_connection: DbConnection = None
    asset_type_manager: AssetTypeManager = None

    def __init__(self):
        """Create a new ``AssetTypePageManager``."""

        self.db_connection = SqliteConnection.get()
        self.asset_type_manager = AssetTypeManager()

    def create_page(self, asset_page: AssetTypePage):
        """Create a new ``AssetPage`` in the database."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        # Check if the asset type the requested page
        # is supposed to be used for, even exists
        if not self.asset_type_manager.check_asset_type_exists(asset_page.asset_type):
            raise AssetTypeDoesNotExistException()

        # Deconstruct the page layout into a valid
        # query dict format for the database
        for row in asset_page.layout:
            for column in row.columns:
                column_row: Mapping[str: Any] = {
                    'primary_key': None,
                    'column_width': column.column_width,
                    'plugin_name': column.plugin_name,
                    'plugin_path': column.plugin_path,
                    'employed_columns': ";".join(column.employed_columns),
                }

                # Storing the column and getting its pk
                column_id: int = self.db_connection.write_dict(
                    self.asset_type_plugin_table_name, column_row)

                # Updating the column id, so we can build
                # a connection between layout and plugin
                column.column_id = column_id

        # The layout id is required so it needs
        # to be set to 0, when creating a page
        # in the backend. That shouldn't be done
        primary_key = asset_page.layout_id \
            if asset_page.layout_id > 0 else None

        layout_row = self.convert_layout_to_row(asset_page)
        layout_row.update({'primary_key': primary_key})

        self.db_connection.write_dict(
            self.asset_type_layout_table_name, layout_row)
        self.db_connection.commit()

    def update_page(self, asset_page: AssetTypePage):
        """Update an ``AssetPage`` in the database."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        # TODO
        pass

    def check_page_exists(self, asset_type: AssetType):
        """Check if an ``AssetPage`` for ``asset_type_id`` exists in the database."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        # TODO
        pass

    def delete_page(self, asset_type: AssetType):
        """Delete the ``AssetPage`` of a given ``asset_type_id``."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        # TODO
        pass

    def get_page(self, asset_type: AssetType):
        """Get the ``AssetPage`` for ``asset_type_id`` from the database"""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        result = self.db_connection.read(
            self.asset_type_layout_table_name,
            headers=self.asset_type_layout_table_columns,
            and_filters=[f'item_id = {asset_type.asset_type_id}']
        )[0]

        if not result:
            raise PageDoesNotExistException(
                "There is no page for the item_id you entered!")

        page: AssetTypePage = AssetTypePage(
            layout_id=result['primary_key'],
            asset_type=asset_type,
            assets=[],
            layout=self.convert_row_data_to_layout(result['layout'])
        )

        return page

    def get_plugin(self, column_id: int):
        """Convert a row to a PageLayout."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        result = self.db_connection.read(
            self.asset_type_plugin_table_name,
            self.asset_type_plugin_table_columns,
            and_filters=[f'primary_key = {column_id}']
        )[0]

        column_info: ColumnInfo = ColumnInfo(
            column_width=result['column_width'],
            plugin_name=result['plugin_name'],
            plugin_path=result['plugin_path'],
            employed_columns=result['employed_columns'].split(';'),
            column_id=result['primary_key']
        )

        return column_info

    def get_editor(self, asset_type: AssetType):
        """Get the editor for a given ``asset_type_id``."""

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
                # The column primary_key will be created automatically -> layout_id
                Column('item_id', 'item_id', DataTypes.INTEGER.value, True),
                Column('layout', 'layout', DataTypes.VARCHAR.value, True)  # <- {[(col_w, column_id), ...],[...],...}
            ]
            self.db_connection.create_table(self.asset_type_layout_table_name, columns)

        if not self.db_connection.check_table_exists(self.asset_type_plugin_table_name):
            columns = [
                # The column primary_key will be created automatically -> column_id
                Column('plugin_name', 'plugin_name', DataTypes.VARCHAR.value, True),
                Column('plugin_path', 'plugin_path', DataTypes.VARCHAR.value, True),
                Column('column_width', 'column_width', DataTypes.INTEGER.value, True),
                Column('employed_columns', 'employed_columns', DataTypes.VARCHAR.value, True),
            ]
            self.db_connection.create_table(self.asset_type_plugin_table_name, columns)
