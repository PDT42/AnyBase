"""
:Author: PDT
:Since: 2020/06/12

This is the module for the ``AssetTypePageManager``.
"""
import json
from datetime import datetime
from typing import Any
from typing import List
from typing import Mapping
from typing import MutableMapping
from typing import Optional
from typing import Union

from quart import logging

from database import Column
from database import DataTypes
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from exceptions.common import IllegalStateException
from exceptions.common import OutdatedDataException
from exceptions.page import ColumnInfoDoesNotExistError
from exceptions.page import PageLayoutDoesNotExist
from pages import ColumnInfo
from pages import PageLayout
from pages.abstract_page_manager import APageManager
from plugins import PluginRegister


class PageManager(APageManager):
    """This is the ``PageManager``."""

    # Defining constants
    PRIMARY_KEY = 'primary_key'
    ASSET_TYPE_ID = 'asset_type_id'
    ASSET_PAGE_LAYOUT = 'asset_page_layout'

    asset_type_layout_table_name: str = 'abintern_layouts'
    layout_plugin_table_name: str = 'abintern_plugins'

    # Defining headers for the table
    # the layouts are stored in

    layout_table_headers: List[str] = [
        PRIMARY_KEY, ASSET_TYPE_ID, ASSET_PAGE_LAYOUT, 'layout',
        'field_mappings', 'created', 'updated', 'sources'
    ]

    # Defining headers for the table the
    # plugins the layouts use are stored in.

    layout_plugin_table_headers: List[str] = [
        'plugin_id', 'column_width', 'field_mappings',
        'column_offset', 'primary_key', 'sources'
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

        created: datetime = datetime.now().replace(microsecond=0)
        page_layout.created = created
        page_layout.updated = created

        for row in page_layout.layout:

            # Creating a query dict from each column
            # and storing it in a separate database
            for column in row:

                # TODO: I dont like the expression column. The
                # TODO: name should differ more from asset column.
                # TODO: Change asset.column name to field

                # Creating a default field mappings dict.
                field_mappings: Optional[Union[MutableMapping[str, str], str]] = {}

                # First use the plugins default field mappings
                # if there are any. This way the user does not
                # have to configure a setting for every field.

                if default_mappings := column.plugin.default_field_mappings:
                    field_mappings.update(default_mappings)

                # If the selected plugin allows custom field
                # mappings, check if the user supplied any.

                if column.plugin.allow_custom_mappings and column.field_mappings:
                    field_mappings.update(column.field_mappings)

                if not field_mappings:
                    raise IllegalStateException(
                        "If allow_custom_mappings is False or you don't provide " +
                        "any custom field mappings, you need at least provide " +
                        "default field mappings!"
                    )

                if field_mappings_str := json.dumps(field_mappings):
                    field_mappings_str = field_mappings_str.replace('"', "'")

                if sources_str := json.dumps(column.sources) if column.sources else None:
                    sources_str = sources_str.replace('"', "'")

                column_row: Mapping[str: Any] = {
                    'primary_key': None,
                    'column_width': column.column_width,
                    'column_offset': column.column_offset,
                    'plugin_id': column.plugin.id.replace('-', '_').upper(),
                    'field_mappings': field_mappings_str,
                    'sources': sources_str
                }

                # Storing the column and getting its pk
                column_id: int = self.db_connection.write_dict(
                    self.layout_plugin_table_name, column_row)

                # Updating the column id, so we can build
                # a connection between layout and plugin

                column.column_id = column_id

        layout_row = self.convert_layout_to_row(page_layout)

        page_layout.layout_id = self.db_connection.write_dict(
            self.asset_type_layout_table_name, layout_row)

        self.db_connection.commit()

        page_layout = self.get_page(
            page_layout.asset_type_id,
            page_layout.asset_page_layout
        )
        return page_layout

    def update_page(self, page_layout: PageLayout):
        """Update an ``AssetPage`` in the database."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        asset_type_id: int = page_layout.asset_type_id
        asset_page_layout: bool = page_layout.asset_page_layout

        if not (db_page_layout := self.get_page(asset_type_id, asset_page_layout)):
            raise PageLayoutDoesNotExist()

        # Checking if there have been updates in the mean time
        if page_layout.updated < db_page_layout.updated:
            raise OutdatedDataException("There has been an update in the mean time!")

        page_layout.updated = datetime.now().replace(microsecond=0)
        layout_row = self.convert_layout_to_row(page_layout)

        page_layout.layout_id = self.db_connection.update(
            self.asset_type_layout_table_name, layout_row)

        return

    def check_page_exists(self, asset_type_id: int, asset_page_layout: bool) -> bool:
        """Check if a ``PageLayout`` exists for a given item."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        query_filters: List[str] = [
            f'{self.ASSET_TYPE_ID} = {asset_type_id}',
            f'{self.ASSET_PAGE_LAYOUT} = {int(asset_page_layout)}'
        ]

        count: int = self.db_connection.count(
            self.asset_type_layout_table_name,
            query_filters=query_filters)

        if count == 0:
            return False
        return True

    def delete_page(self, asset_type_id: int, asset_page_layout: bool):
        """Delete the ``PageLayout`` of a given ``item``."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        if (db_page_layout := self.get_page(asset_type_id, asset_page_layout)) is None:
            raise PageLayoutDoesNotExist(f"The page layout you are trying to delete does not exist!")

        for row in db_page_layout.layout:
            for column in row:
                filters = [f'primary_key = {column.column_id}']
                self.db_connection.delete(self.layout_plugin_table_name, and_filters=filters)

        filters = [f'asset_type_id = {asset_type_id}', f'asset_page_layout = {asset_page_layout}']
        self.db_connection.delete(self.asset_type_layout_table_name, and_filters=filters)

    def get_page(self, asset_type_id: int, asset_type_page: bool) -> Optional[PageLayout]:
        """Get the ``PageLayout`` for ``item`` from the database"""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        result = self.db_connection.read(
            self.asset_type_layout_table_name,
            headers=self.layout_table_headers,
            and_filters=[
                f'{self.ASSET_TYPE_ID} = {asset_type_id}',
                f'{self.ASSET_PAGE_LAYOUT} = {int(asset_type_page)}'
            ])

        if len(result) < 1:
            logger = logging.getLogger('quart.serving')
            logger.warning(
                f"There is no page for the asset type id: " +
                f"{asset_type_id} with detail-view: {asset_type_page}")
            return None

        return self.convert_row_data_to_layout(result[0])

    #
    # PRIVATE METHODS
    # ---------------
    #

    def _get_column_info(self, column_id: int) -> ColumnInfo:
        """Get Column info on column with ``column_id``."""

        # Ensuring the required database tables exist
        self._init_page_layout_tables()

        result = self.db_connection.read(
            self.layout_plugin_table_name,
            self.layout_plugin_table_headers,
            and_filters=[f'primary_key = {column_id}'])

        if len(result) < 1:
            raise ColumnInfoDoesNotExistError()

        result = result[0]

        # Extract the field mappings from fm string
        field_mappings: Optional[Mapping[str, str]] = None
        if field_mappings_string := result['field_mappings']:
            field_mappings_string = field_mappings_string.replace("'", '"')
            field_mappings = json.loads(field_mappings_string)

        sources: MutableMapping[str, str] = {}
        if sources_str := result['sources'] if result['sources'] else None:
            sources_str = sources_str.replace("'", '"')
            sources = json.loads(sources_str)

        column_info: ColumnInfo = ColumnInfo(
            plugin=PluginRegister[result['plugin_id']].value,
            column_width=result.get('column_width', 3),
            column_offset=result.get('column_offset', 0),
            column_id=result['primary_key'],
            field_mappings=field_mappings,
            sources=sources)

        return column_info

    def _init_page_layout_tables(self):
        """Initialize required tables in the database."""

        if not self.db_connection.check_table_exists(self.asset_type_layout_table_name):
            columns = [
                # The column primary_key will be created automatically -> layout_id
                Column('asset_type_id', 'asset_type_id', DataTypes.INTEGER.value, True),
                Column('asset_page_layout', 'asset_page_layout', DataTypes.BOOLEAN.value, True),
                Column('layout', 'layout', DataTypes.VARCHAR.value, True),
                Column('field_mappings', 'field_mappings', DataTypes.VARCHAR.value, False),
                Column('created', 'created', DataTypes.DATETIME.value, True),
                Column('updated', 'updated', DataTypes.DATETIME.value, True),
                Column('sources', 'sources', DataTypes.VARCHAR.value, False)
            ]

            self.db_connection.create_table(self.asset_type_layout_table_name, columns)

        if not self.db_connection.check_table_exists(self.layout_plugin_table_name):
            columns = [
                # The column primary_key will be created automatically -> column_id
                Column('plugin_id', 'plugin_id', DataTypes.VARCHAR.value, True),
                Column('column_width', 'column_width', DataTypes.INTEGER.value, True),
                Column('column_offset', 'column_offset', DataTypes.INTEGER.value, True),
                Column('field_mappings', 'field_mappings', DataTypes.VARCHAR.value, True),
                Column('sources', 'sources', DataTypes.VARCHAR.value, False)
            ]

            self.db_connection.create_table(self.layout_plugin_table_name, columns)
