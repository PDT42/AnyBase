"""
:Author: PDT
:Since: 2020/08/10

This is the abstract super class for the implementations of a PageManager.
"""

from abc import abstractmethod
from re import findall
from typing import Any, Dict, List, Mapping

from asset import AssetType
from asset.asset_manager import AssetManager
from asset.asset_type_manager import AssetTypeManager
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
    def delete_page(self, page_layout: PageLayout):
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
    def _get_column_info(self, column_id: int):
        """Get the plugin with ``column_id``. """
        pass

    @staticmethod
    def convert_layout_to_row(page_layout: PageLayout) -> Mapping[str, Any]:
        """Convert a PageLayout Type to a row."""

        # Constructing the layout string
        layout_str: str = ""

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
            'primary_key': page_layout.layout_id,
        }
        return layout_row

    def convert_row_data_to_layout(self, row_data: Mapping[str, Any]):
        """Convert a row to a PageLayout."""

        layout: List[List[ColumnInfo]] = []

        # Using the create syntax used in convert_layout_to_row
        # to extract ColumnInfo objects from db row.

        # row_data: "[{column_width, column_id; ...}, ...]"

        for row in findall("{([^}]*)}", row_data['layout']):

            # row: "{column_width, column_id; ...}"

            row_info: List[ColumnInfo] = []

            for column in row.split(';'):
                # column: "column_width, column_id"

                column_width, column_id = column.split(', ')
                row_info.append(self._get_column_info(int(column_id)))

            layout.append(row_info)

        # Getting the asset type using the manager
        # filled by the child of this superclass.

        field_mappings: Dict[str, str] = {
            key: value for key, value in [
                item.split(': ') for item in row_data['field_mappings']
                    .replace('{', '').replace('}', '').replace("'", '').split(', ')]
        }

        return PageLayout(
            asset_type_id=row_data['asset_type_id'],
            asset_page_layout=bool(row_data['asset_page_layout']),
            layout=layout,
            layout_id=row_data['primary_key'],
            field_mappings=field_mappings
        )
