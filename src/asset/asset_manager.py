"""
:Author: PDT
:Since: 2020/05/28

This is the the module for the resource manager.
"""
from typing import Any, MutableMapping, Optional, Sequence

from asset import Asset, AssetType
from asset.asset_type_manager import AssetTypeManager
from database import Column
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection


class AssetManager:
    """This is the ``AssetManager``."""

    def __init__(self):
        """Create a new ``AssetManager``."""

        self.db_connection: DbConnection = SqliteConnection.get()
        self.asset_type_manager: AssetTypeManager = AssetTypeManager()

    def create_asset(self, asset_type: AssetType, asset: Asset):
        """Create an asset in the database."""

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            return 0

        asset.data.update({'primary_key': None})

        self.db_connection.write_dict(asset_type.asset_table_name, asset.data)
        self.db_connection.commit()

    def delete_asset(self, asset_type: AssetType, asset: Asset):
        """Delete an asset from the system."""

        self.db_connection.delete(
            self.asset_type_manager.generate_asset_table_name(asset_type),
            [f"primary_key = {asset.asset_id}"]
        )
        self.db_connection.commit()

    def update_asset(self, asset: Asset):
        """Update the information on an asset in the database."""
        # TODO
        pass

    def get_all(self, asset_type: AssetType) -> Sequence[Asset]:
        """Get all assets of ``AssetType`` from the database."""

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            return []

        result: Sequence[MutableMapping[str, Any]] = self.db_connection.read(
            self.asset_type_manager.generate_asset_table_name(asset_type),
            [column.name for column in asset_type.columns])

        assets = []
        for asset_row in result:
            assets.append(Asset(
                asset_id=asset_row.pop('primary_key'),
                data=self._convert_row_to_data(asset_row, asset_type.columns)
            ))

        return assets

    def get_one(self, asset_id: int, asset_type: AssetType) -> Optional[Asset]:
        """Get the ``Asset`` with ``asset_id`` from the database."""

        result: Sequence[MutableMapping[str, Any]] = self.db_connection.read(
            table_name=self.asset_type_manager.generate_asset_table_name(asset_type),
            headers=[column.name for column in asset_type.columns],
            and_filters=[f'primary_key = {asset_id}']
        )

        if len(result) < 1:
            return None

        asset = Asset(
            asset_id=result[0].pop('primary_key'),
            data=self._convert_row_to_data(result[0], asset_type.columns)
        )
        return asset

    ###################
    # private methods #
    ###################

    @staticmethod
    def _convert_row_to_data(
            row: MutableMapping[str, Any],
            columns: Sequence[Column]) \
            -> MutableMapping[str, Any]:
        """Convert a row to a valid data entry of an ``Asset``."""

        data: MutableMapping[str, Any] = {column.name: row[column.name] for column in columns}

        return data
