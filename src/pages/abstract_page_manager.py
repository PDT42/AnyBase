"""
:Author: PDT
:Since: 2020/08/10

This is the abstract super class for the implementations of a PageManager.
"""

from abc import abstractmethod
from re import findall
from typing import Any, List, Mapping, Optional

from asset import Asset, AssetType
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
    asset_type_plugin_table_name: str = None

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
    def check_page_exists(self, page_layout: PageLayout):
        """Check if an ``AssetPage`` for ``asset_type_id`` exists in the database."""
        pass

    @abstractmethod
    def get_page(self, asset_type: AssetType, asset: Asset):
        """Get the ``AssetPage`` for ``asset_type_id`` from the database"""
        pass

    @abstractmethod
    def get_column_info(self, column_id: int):
        """Get the plugin with ``column_id``. """
        pass

    @abstractmethod
    def get_editor(self, page_layout: PageLayout):
        """Get the editor for a given ``asset_type_id``."""
        pass

    @staticmethod
    def convert_layout_to_row(page_layout: PageLayout) -> Mapping[str, Any]:
        """Convert a PageLayout Type to a row."""

        # Constructing the layout string
        layout_str: str = "["

        for row_info in page_layout.layout:
            columns = ";".join([
                f"{col.column_width}, {col.column_id}"
                for col in row_info
            ])
            layout_str += "{" + str(columns) + "}"
        layout_str += "]"

        asset_id = None
        if isinstance(page_layout.asset, Asset):
            asset_id = page_layout.asset.asset_id

        # Creating a dict as required by db query
        layout_row: Mapping[str, Any] = {
            'primary_key': page_layout.layout_id,
            'items_url': page_layout.items_url,
            'asset_id': asset_id,
            'asset_type_id': page_layout.asset_type.asset_type_id,
            'layout': str(layout_str)
        }
        return layout_row

    def convert_row_data_to_layout(self, row_data: Mapping[str, Any]):
        """Convert a row to a PageLayout."""

        layout: List[List[ColumnInfo]] = []

        # Using the create syntax used in convert_layout_to_row
        # to extract ColumnInfo objects from db row.

        # row_data: "[{column_width, column_id; ...}, ...]"

        # row: "{column_width, column_id; ...}"
        for row in findall("{([^}]*)}", row_data['layout']):

            row_info: List[ColumnInfo] = []

            # column: "column_width, column_id"
            for column in row.split(';'):
                column_width, column_id = column.split(', ')
                row_info.append(self.get_column_info(int(column_id)))

            layout.append(row_info)

        # Getting the asset type using the manager
        # filled by the child of this superclass.

        asset_type: AssetType = self.asset_type_manager \
            .get_one(row_data['asset_type_id'])

        asset: Optional[Asset] = None

        if asset_id := row_data['asset_id']:
            asset = self.asset_manager.get_one(asset_id, asset_type)

        # Finally returning a PageLayout

        return PageLayout(
            layout=layout,
            asset_type=asset_type,
            items_url=row_data['items_url'],
            asset=asset,
            layout_id=row_data['primary_key']
        )
