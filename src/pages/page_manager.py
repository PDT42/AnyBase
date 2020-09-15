"""
:Author: PDT
:Since: 2020/06/12

This is the module for the ``AssetTypePageManager``.
"""
from typing import Any, List, Mapping, Optional, Union

from asset import Asset
from asset_type import AssetType
from database import Column, DataTypes
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from exceptions.page import ColumnInfoDoesNotExistError
from pages import ColumnInfo, PageLayout
from pages.abstract_page_manager import APageManager
from plugins import PluginRegister


class PageManager(APageManager):
    """This is the ``PageManager``."""

    asset_type_layout_table_name: str = 'abintern_layouts'
    layout_table_headers: List[str] = [
        'primary_key',
        'asset_type_id',
        'asset_page_layout',
        'layout',
        'field_mappings',
        'sources'
    ]
    plugin_table_name: str = 'abintern_plugins'
    asset_type_plugin_table_headers: List[str] = [
        'plugin_name',
        'column_width',
        'field_mappings',
        'primary_key',
        'sources'
    ]

    db_connection: DbConnection = None

    def __init__(self):
        """Create a new ``AssetTypePageManager``."""

        self.db_connection = SqliteConnection.get()

    def create_page(self, page_layout: PageLayout) -> PageLayout:
        """Create a new ``AssetPage`` in the database."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        # Deconstruct the page_layout layout into a valid
        # query dict format for the database

        for row in page_layout.layout:
            for column in row:
                # Creating a query dict from each column
                # and storing it in a separate database

                field_mappings = ";".join([
                    f"{field},{mapping}" for field, mapping in column.field_mappings.items()
                ])

                sources = set(";".join(column.sources)) if column.sources else None

                column_row: Mapping[str: Any] = {
                    'primary_key': None,
                    'column_width': column.column_width,
                    'plugin_name': column.plugin.name.replace('-', '_').upper(),
                    'field_mappings': field_mappings,
                    'sources': sources
                }

                # Storing the column and getting its pk
                column_id: int = self.db_connection.write_dict(
                    self.plugin_table_name, column_row)

                # Updating the column id, so we can build
                # a connection between layout and plugin

                column.column_id = column_id

        layout_row = self.convert_layout_to_row(page_layout)

        page_layout.layout_id = self.db_connection.write_dict(
            self.asset_type_layout_table_name, layout_row)
        self.db_connection.commit()

        return page_layout

    def update_page(self, page_layout: PageLayout):
        """Update an ``AssetPage`` in the database."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        raise NotImplementedError()

    def check_page_exists(self, asset_type_id: int, asset_page: bool) -> bool:
        """Check if an ``PageLayout`` exists for a given item."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        raise NotImplementedError()

    def delete_page(self, item: Union[AssetType, Asset]):
        """Delete the ``PageLayout`` of a given ``item``."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        raise NotImplementedError()

    def get_page(self, asset_type_id: int, asset_type_page: bool) -> Optional[PageLayout]:
        """Get the ``PageLayout`` for ``item`` from the database"""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        result = self.db_connection.read(
            self.asset_type_layout_table_name,
            headers=self.layout_table_headers,
            and_filters=[
                f'asset_type_id = {asset_type_id}',
                f'asset_page_layout = {int(asset_type_page)}'
            ])

        if len(result) < 1:
            return None

        return self.convert_row_data_to_layout(result[0])

    def _get_column_info(self, column_id: int) -> ColumnInfo:
        """Get Column info on column with ``column_id``."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        result = self.db_connection.read(
            self.plugin_table_name,
            self.asset_type_plugin_table_headers,
            and_filters=[f'primary_key = {column_id}'])

        if len(result) < 1:
            raise ColumnInfoDoesNotExistError()

        result = result[0]

        # Extract the field mappings from fm string
        field_mappings: Mapping[str, str] = {
            field: mapping for field, mapping in [
                fm.split(',') for fm in result['field_mappings'].split(';')
            ]}

        sources = set(result['sources'].split(';')) if result['sources'] else None

        column_info: ColumnInfo = ColumnInfo(
            plugin=PluginRegister[result['plugin_name']].value,
            column_width=result['column_width'],
            field_mappings=field_mappings,
            sources=sources,
            column_id=result['primary_key'])

        return column_info

    #
    # PRIVATE METHODS
    # ---------------
    #

    def _init_page_layout_tables(self):
        """Initialize required tables in the database."""

        if not self.db_connection.check_table_exists(self.asset_type_layout_table_name):
            columns = [
                # The column primary_key will be created automatically -> layout_id
                Column('asset_type_id', 'asset_type_id', DataTypes.INTEGER.value, True),
                Column('asset_page_layout', 'asset_page_layout', DataTypes.BOOLEAN.value, True),
                Column('layout', 'layout', DataTypes.VARCHAR.value, True),
                Column('field_mappings', 'field_mappings', DataTypes.VARCHAR.value, True),
                Column('sources', 'sources', DataTypes.VARCHAR.value, False)
            ]

            self.db_connection.create_table(self.asset_type_layout_table_name, columns)

        if not self.db_connection.check_table_exists(self.plugin_table_name):
            columns = [
                # The column primary_key will be created automatically -> column_id
                Column('plugin_name', 'plugin_name', DataTypes.VARCHAR.value, True),
                Column('column_width', 'column_width', DataTypes.INTEGER.value, True),
                Column('field_mappings', 'field_mappings', DataTypes.VARCHAR.value, True),
                Column('sources', 'sources', DataTypes.VARCHAR.value, False)
            ]

            self.db_connection.create_table(self.plugin_table_name, columns)
