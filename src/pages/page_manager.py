"""
:Author: PDT
:Since: 2020/06/12

This is the module for the ``AssetTypePageManager``.
"""
from typing import Any, List, Mapping, Union

from asset import Asset, AssetType
from asset.asset_type_manager import AssetTypeManager
from database import Column, DataTypes
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from exceptions.asset import AssetTypeDoesNotExistException
from exceptions.plugins import PageDoesNotExistException
from pages import ColumnInfo, PageLayout
from pages.abstract_page_manager import APageManager


class PageManager(APageManager):
    """This is the ``PageManager``."""

    asset_type_layout_table_name: str = 'abintern_asset_type_layouts'
    asset_type_layout_table_columns: List[str] = [
        'primary_key',
        'asset_type_id',
        'items_url',
        'asset_id',
        'layout'
    ]
    asset_type_plugin_table_name: str = 'abintern_asset_type_plugins'
    asset_type_plugin_table_columns: List[str] = [
        'plugin_name',
        'plugin_path',
        'column_width',
        'employed_columns',
        'primary_key'
    ]

    db_connection: DbConnection = None
    asset_type_manager: AssetTypeManager = None

    def __init__(self):
        """Create a new ``AssetTypePageManager``."""

        self.db_connection = SqliteConnection.get()
        self.asset_type_manager = AssetTypeManager()

    def create_page(self, page_layout: PageLayout) -> int:
        """Create a new ``AssetPage`` in the database."""

        # TODO: Add check if layout already exists

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        # Check if the asset type the requested page_layout
        # is supposed to be used for, even exists
        if not self.asset_type_manager.check_asset_type_exists(page_layout.asset_type):
            raise AssetTypeDoesNotExistException()

        # Deconstruct the page_layout layout into a valid
        # query dict format for the database

        for row in page_layout.layout:
            for column in row:

                # Creating a query dict from the columns
                # and storing them in a separate database

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

        layout_row = self.convert_layout_to_row(page_layout)

        layout_id = self.db_connection.write_dict(
            self.asset_type_layout_table_name, layout_row)
        self.db_connection.commit()

        return layout_id

    def update_page(self, page_layout: PageLayout):
        """Update an ``AssetPage`` in the database."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        # TODO
        pass

    def check_page_exists(self, item: Union[AssetType, Asset]):
        """Check if an ``PageLayout`` exists for a given item."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        # TODO
        pass

    def delete_page(self, item: Union[AssetType, Asset]):
        """Delete the ``PageLayout`` of a given ``item``."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        # TODO
        pass

    def get_page(self, asset_type: AssetType, asset: Asset = None):
        """Get the ``PageLayout`` for ``item`` from the database"""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        query_filter: List[str] = [f'asset_type_id = {asset_type.asset_type_id}']

        if asset is not None:
            query_filter.append(f'asset_id = {asset.asset_id}')

        result = self.db_connection.read(
            self.asset_type_layout_table_name,
            headers=self.asset_type_layout_table_columns,
            and_filters=query_filter
        )

        if not result:
            return None

        result = result[0]

        return self.convert_row_data_to_layout(result)

    def get_column_info(self, column_id: int):
        """Get Column info on column with ``column_id``."""

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

    #####################
    #  PRIVATE METHODS  #
    #####################

    def _init_page_layout_tables(self):
        """Initialize required tables in the database."""

        if not self.db_connection.check_table_exists(self.asset_type_layout_table_name):
            columns = [
                # The column primary_key will be created automatically -> layout_id
                Column('asset_type_id', 'asset_type_id', DataTypes.INTEGER.value, True),
                Column('items_url', 'items_url', DataTypes.VARCHAR.value, True),
                Column('asset_id', 'asset_id', DataTypes.INTEGER.value, False),
                Column('layout', 'layout', DataTypes.VARCHAR.value, True)
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
