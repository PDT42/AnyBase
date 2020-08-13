"""
:Author: PDT
:Since: 2020/08/10

This is the abstract super class for the implementations of a PageManager.
"""

from abc import abstractmethod
from re import findall
from typing import Any, List, Mapping, Optional

from asset import AssetType
from database.db_connection import DbConnection
from exceptions.plugins import ItemNotFoundException
from pages import AssetDetailPage, AssetTypePage, ColumnInfo, PageLayout, RowInfo


class APageManager:
    """This is an APageManager."""

    # Variables filled by the implementation
    db_connection: DbConnection = None
    asset_type_layout_table_name: str = None
    asset_type_plugin_table_name: str = None

    @abstractmethod
    def create_page(self, asset_page: AssetTypePage):
        """Create a new ``AssetPage`` in the database."""
        pass

    @abstractmethod
    def delete_page(self, asset_type: AssetType):
        """Delete the ``AssetPage`` of a given ``asset_type_id``."""
        pass

    @abstractmethod
    def update_page(self, asset_page: AssetTypePage):
        """Update an ``AssetPage`` in the database."""
        pass

    @abstractmethod
    def check_page_exists(self, asset_type: AssetType):
        """Check if an ``AssetPage`` for ``asset_type_id`` exists in the database."""
        pass

    @abstractmethod
    def get_page(self, asset_type: AssetType):
        """Get the ``AssetPage`` for ``asset_type_id`` from the database"""
        pass

    @abstractmethod
    def get_plugin(self, column_id: int):
        """Get the plugin with ``column_id``. """
        pass

    @abstractmethod
    def get_editor(self, asset_type: AssetType):
        """Get the editor for a given ``asset_type_id``."""
        pass

    @staticmethod
    def convert_layout_to_row(page: PageLayout):
        """Convert a PageLayout Type to a row."""

        item_id: Optional[int] = None

        if isinstance(page, AssetTypePage):
            item_id = page.asset_type.asset_type_id
        elif isinstance(page, AssetDetailPage):
            item_id = page.asset.asset_id

        if not item_id:
            raise ItemNotFoundException("The item is unknown.")

        # Constructing the layout string
        layout: str = "["

        for row_info in page.layout:
            columns = ";".join([
                f"{col.column_width}, {col.column_id}"
                for col in row_info.columns
            ])
            layout += "{" + str(columns) + "}"
        layout += "]"

        # Creating a dict as required by db query
        layout_row: Mapping[str, Any] = {
            'item_id': page.asset_type.asset_type_id,
            'layout': str(layout)
        }
        return layout_row

    def convert_row_data_to_layout(self, row_data: str):
        """Convert a row to a PageLayout."""

        layout: List[RowInfo] = []

        for row in findall("{([^}]*)}", row_data):

            row_info: RowInfo = RowInfo(columns=[])

            for col in row.split(';'):
                column_width, column_id = col.replace('(', '') \
                    .replace(')', '').split(', ')

                row_info.columns.append(self.get_plugin(int(column_id)))

            layout.append(row_info)

        return layout
