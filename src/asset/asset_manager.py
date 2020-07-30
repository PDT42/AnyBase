"""
:Author: PDT
:Since: 2020/05/28

This is the the module for the AssetManager.
"""

from typing import Any, List, MutableMapping, Optional, Sequence

from asset import Asset, AssetType
from asset.abstract_asset_manager import AAssetManager
from asset.asset_type_manager import AssetTypeManager
from database import Column
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from exceptions.asset import AssetTypeDoesNotExistException
from exceptions.common import KeyConstraintException


class AssetManager(AAssetManager):
    """This is the ``AssetManager``."""

    # TODO: Make this a singleton? Might be necessary for db concurrency.

    # Required fields
    asset_type_manager: AssetTypeManager = None
    db_connection: DbConnection = None

    def __init__(self):
        """Create a new ``AssetManager``."""

        self.db_connection: DbConnection = SqliteConnection.get()
        self.asset_type_manager: AssetTypeManager = AssetTypeManager()

    def create_asset(self, asset_type: AssetType, asset: Asset):
        """Create an asset in the database."""

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            return 0

        values = (self.convert_data_to_row(asset.data, asset_type.columns))
        values.update({'primary_key': None})

        self.db_connection.write_dict(asset_type.asset_table_name, values)
        self.db_connection.commit()

    def delete_asset(self, asset_type: AssetType, asset: Asset):
        """Delete an asset from the system."""

        self.db_connection.delete(
            self.asset_type_manager.generate_asset_table_name(asset_type),
            [f"primary_key = {asset.asset_id}"]
        )
        self.db_connection.commit()

    def update_asset(self, asset_type: AssetType, asset: Asset):
        """Update the information on an asset in the database."""

        # Making sure the asset exists in the database
        if not asset.asset_id:
            raise AttributeError("The asset_id parameter of the asset you try to update must be set!")

        # Making sure the asset_type table is set
        if not asset_type.asset_table_name:
            raise AttributeError("The asset_type_table parameter of asset_type must be set!")

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            raise AssetTypeDoesNotExistException(f"The asset type {asset_type} does not exist!")

        data = self.convert_data_to_row(asset.data, asset_type.columns)
        data.update({'primary_key': asset.asset_id})

        self.db_connection.update(asset_type.asset_table_name, data)

    def get_all(self, asset_type: AssetType) -> List[Asset]:
        """Get all assets of ``AssetType`` from the database."""

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            raise AssetTypeDoesNotExistException()

        result: Sequence[MutableMapping[str, Any]] = self.db_connection.read(
            self.asset_type_manager.generate_asset_table_name(asset_type),
            [column.db_name for column in asset_type.columns])

        assets = []
        for asset_row in result:
            assets.append(Asset(
                asset_id=asset_row.pop('primary_key'),
                data=self.convert_row_to_data(asset_row, asset_type.columns)
            ))

        return assets

    def get_one(self, asset_id: int, asset_type: AssetType) -> Optional[Asset]:
        """Get the ``Asset`` with ``asset_id`` from the database."""

        result: Sequence[MutableMapping[str, Any]] = self.db_connection.read(
            table_name=self.asset_type_manager.generate_asset_table_name(asset_type),
            headers=[column.db_name for column in asset_type.columns],
            and_filters=[f'primary_key = {asset_id}']
        )

        if len(result) < 1:
            return None

        if len(result) > 1:
            raise KeyConstraintException(
                "There is a real big problem here! Real biggy - trust me." +
                "The primary key constraint is broken!"
            )

        asset = Asset(
            asset_id=result[0].pop('primary_key'),
            data=self.convert_row_to_data(result[0], asset_type.columns)
        )
        return asset

    # TODO: Move these to the abstract super class?

    @staticmethod
    def convert_row_to_data(
            row: MutableMapping[str, Any],
            columns: Sequence[Column]) \
            -> MutableMapping[str, Any]:
        """Convert a row to a valid data entry of an ``Asset``."""

        data: MutableMapping[str, Any] = {
            column.db_name: column.datatype.convert_from_db_type(row[column.db_name])
            for column in columns
        }

        return data

    @staticmethod
    def convert_data_to_row(
            data: MutableMapping[str, Any],
            columns: Sequence[Column]) \
            -> MutableMapping[str, Any]:
        """Convert a data mapping as contained in an asset to a valid database query input."""

        row: MutableMapping[str, Any] = {
            column.db_name: column.datatype.convert_to_dbtype(data[column.db_name])
            for column in columns
        }

        return row
