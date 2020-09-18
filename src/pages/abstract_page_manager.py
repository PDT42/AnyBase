"""
:Author: PDT
:Since: 2020/08/10

This is the abstract super class for the implementations of a PageManager.
"""

from abc import abstractmethod
from datetime import datetime
from re import findall
from typing import Any, Dict, List, Mapping, Optional, Set

from asset.asset_manager import AssetManager
from asset_type.asset_type_manager import AssetTypeManager
from database.db_connection import DbConnection
from pages import ColumnInfo, PageLayout


class APageManager:
    """This is an APageManager."""

    # Variables filled by the implementation
    db_connection: DbConnection = None
    asset_type_manager: AssetTypeManager = None
    asset_manager: AssetManager = None

    asset_type_layout_table_name: str = None
    plugin_table_name: str = None

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

        # Creating a dict as required by db query
        layout_row: Mapping[str, Any] = {
            'asset_type_id': page_layout.asset_type_id,
            'asset_page_layout': int(page_layout.asset_page_layout),
            'layout': str(layout_str),
            'field_mappings': str(page_layout.field_mappings),
            'created': int(page_layout.created.timestamp()) if page_layout.updated else None,
            'updated': int(page_layout.updated.timestamp()) if page_layout.updated else None,
            'sources': ";".join(page_layout.sources) if page_layout.sources else None,
            'primary_key': page_layout.layout_id
        }
        return layout_row

    def convert_row_data_to_layout(self, row_data: Mapping[str, Any]):
        """Convert a row to a PageLayout."""

        layout: List[List[ColumnInfo]] = []
        sources: Optional[Set[str]] = row_data.get('sources')

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

        field_mappings_str = row_data['field_mappings'][1:-2]\
            .replace("'", '').split(', ')

        field_mappings: Dict[str, str] = {
            key: value for key, value in [
                item.split(': ') for item in field_mappings_str if len(item) > 0
            ]
        }

        return PageLayout(
            asset_type_id=int(row_data['asset_type_id']),
            asset_page_layout=bool(row_data['asset_page_layout']),
            created=datetime.fromtimestamp(row_data.get('created')),
            updated=datetime.fromtimestamp(row_data.get('updated')),
            layout=layout,
            layout_id=row_data['primary_key'],
            field_mappings=field_mappings,
            sources=sources
        )
