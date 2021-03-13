"""
:Author: PDT
:Since: 2020/08/10

This is the abstract super class for the implementations of a PageManager.
"""

import json
from abc import abstractmethod
from datetime import datetime
from re import findall
from typing import Any
from typing import List
from typing import Mapping
from typing import MutableMapping
from typing import Optional

from asset.asset_manager import AssetManager
from asset_type import AssetType
from asset_type.asset_type_manager import AssetTypeManager
from database.db_connection import DbConnection
from exceptions.database import MissingValueException
from pages import ColumnInfo
from pages import PageLayout
from plugins.abstract_plugin import APluginServer
from plugins import PluginRegister


class APageManager:
    """This is an APageManager."""

    # Variables filled by the implementation
    db_connection: DbConnection = None
    asset_type_manager: AssetTypeManager = None
    asset_manager: AssetManager = None

    asset_type_layout_table_name: str = None
    plugin_table_name: str = None

    # Constants.
    MAX_FIELD_NUMBER: int = 10

    @abstractmethod
    def create_page(self, page_layout: PageLayout):
        """Create a new ``PageLayout`` in the database."""
        pass

    @abstractmethod
    def delete_page(self, asset_type_id: int, asset_page_layout: bool):
        """Delete the ``AssetPage`` of a given ``asset_type_id``."""
        pass

    @abstractmethod
    def update_page(self, page_layout: PageLayout):
        """Update an ``AssetPage`` in the database."""
        pass

    @abstractmethod
    def check_page_exists(self, asset_type_id: int, asset_page: bool) -> bool:
        """Check if an ``AssetPage`` for ``asset_type_id`` exists in the database."""
        pass

    @abstractmethod
    def get_page(self, asset_type_id: int, asset_type_page: bool):
        """Get the ``AssetPage`` for ``asset_type_id`` from the database"""
        pass

    @abstractmethod
    def _get_column_info(self, column_id: int) -> ColumnInfo:
        """Get the plugin with ``column_id``. """
        pass

    @staticmethod
    def convert_layout_to_row(page_layout: PageLayout) -> Mapping[str, Any]:
        """Convert a PageLayout Type to a row."""

        # Constructing the layout string
        layout_str: str = ""

        # Formatting column info and appending it to layout_str
        for row_info in page_layout.layout:
            columns = ";".join([
                f"{col.column_width}, {col.column_id}"
                for col in row_info
            ])

            layout_str += '{' + str(columns) + '}'

        if field_mappings := json.dumps(page_layout.field_mappings) \
                if page_layout.field_mappings else None:
            field_mappings = field_mappings.replace('"', "'")

        if sources_str := json.dumps(page_layout.sources) if page_layout.sources else None:
            sources_str = sources_str.replace('"', "'")

        # Creating a dict as required by db query
        layout_row: Mapping[str, Any] = {
            'asset_type_id': page_layout.asset_type_id,
            'asset_page_layout': int(page_layout.asset_page_layout),
            'layout': str(layout_str),
            'field_mappings': field_mappings,
            'created': int(page_layout.created.timestamp()) if page_layout.updated else None,
            'updated': int(page_layout.updated.timestamp()) if page_layout.updated else None,
            'sources': sources_str,
            'primary_key': page_layout.layout_id
        }
        return layout_row

    def convert_row_data_to_layout(self, row_data: Mapping[str, Any]):
        """Convert a row to a PageLayout."""

        layout: List[List[ColumnInfo]] = []
        sources_str = row_data.get('sources')
        sources_str = sources_str if sources_str else '{}'
        sources_str = sources_str.replace("'", '"')
        sources = json.loads(sources_str)

        # Using the create syntax used in convert_layout_to_row
        # to extract ColumnInfo objects from db row.

        # row_data: "[{column_width, column_id; ...}, ...]"

        for row in findall("{([^}]*)}", row_data['layout']):

            # row: "{column_width, column_id; ...}"

            row_info: List[ColumnInfo] = []

            for column in row.split(';'):

                # column: "column_width, column_id"

                column_width, column_id = column.split(', ')
                column_info = self._get_column_info(int(column_id))
                row_info.append(column_info)

                if column_info.sources and not sources:
                    sources = column_info.sources

                elif column_info.sources:
                    sources.update(column_info.sources)

            layout.append(row_info)

        # Getting the asset type using the manager
        # filled by the child of this superclass.

        field_mappings: Optional[MutableMapping[str, str]] = None
        if field_mappings_string := row_data['field_mappings']:
            field_mappings_string = field_mappings_string.replace("'", '"')
            field_mappings = json.loads(field_mappings_string)

        return PageLayout(
            asset_type_id=int(row_data['asset_type_id']),
            asset_page_layout=bool(row_data['asset_page_layout']),
            created=datetime.fromtimestamp(row_data.get('created')),
            updated=datetime.fromtimestamp(row_data.get('updated')),
            layout_id=row_data['primary_key'],
            field_mappings=field_mappings,
            sources=sources,
            layout=layout)

    @staticmethod
    def get_page_layout_from_form_data(asset_type: AssetType, detail_view: bool, form_data: Mapping):
        """Get a ``PageLayout`` from form data."""

        layout: List[List[ColumnInfo]] = []
        sources: MutableMapping[str, str] = {}
        field_mappings: MutableMapping[str, str] = {}

        if detail_view:

            title_selector_id: str = 'detail-view-title'

            if title_selector_id not in form_data:
                raise MissingValueException()

            field_mappings['title'] = form_data[title_selector_id]

        for row_number in range(0, 15):

            # Generate id from row number
            row_id = f'row-{row_number}'

            if f'{row_id}-col-0-plugin' not in form_data.keys():
                break

            layout.append([])

            for column_number in range(0, 3):

                # Generate id from column number
                col_id = f'{row_id}-col-{column_number}'

                # Check whether the required
                # values are present.
                plugin_id = f'{col_id}-plugin'
                if plugin_id not in form_data.keys():
                    break

                # Getting required values from sync-form
                plugin_id = str(form_data.get(plugin_id))
                column_width = int(form_data.get(f'{col_id}-width'))
                column_offset = int(form_data.get(f'{col_id}-offset'))

                # Getting plugin info and field_mappings
                plugin = PluginRegister[plugin_id.upper().replace('-', '_')].value

                column_field_mappings = {}
                for field in plugin.fields:
                    column_field_str = f'{col_id}-field-{field}'
                    column_field_mappings[field] = str(form_data.get(column_field_str))

                # Add custom mappings if allowed.
                if plugin.allow_custom_mappings:

                    # CHECKOUT: This uses a constant to define a maximum allowed number
                    # CHECKOUT: of custom field mappings. This might be done differently.

                    for custom_field_number in range(0, APageManager.MAX_FIELD_NUMBER):
                        custom_field_name = f'custom-field-{custom_field_number}'
                        custom_field_key = f'{col_id}-{custom_field_name}'
                        if custom_mapping := form_data.get(custom_field_key):
                            column_field_mappings[custom_field_name] = custom_mapping

                # Getting dependant values
                column_sources: MutableMapping[str, str] = {}
                if plugin.server and isinstance(plugin.server, APluginServer):
                    # IMPORTANT: Here the the plugin server is initialized!
                    column_sources = plugin.server.get().initialize(asset_type, None)
                    sources.update(column_sources)

                # Creating ColumnInfo object
                column_info: ColumnInfo = ColumnInfo(
                    plugin=plugin, column_width=column_width,
                    column_offset=column_offset, field_mappings=column_field_mappings,
                    sources=column_sources)

                # Adding the column info into the layout
                layout[row_number].append(column_info)

        # Creating the PageLayout object
        page_layout: PageLayout = PageLayout(
            asset_type_id=asset_type.asset_type_id,
            asset_page_layout=detail_view,
            layout=layout,
            field_mappings=field_mappings,
            sources=sources)

        return page_layout
