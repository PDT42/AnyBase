"""
:Author: PDT
:Since: 2020/05/28

This is the the module for the AssetManager.
"""

from datetime import datetime
from typing import Any, List, Mapping, MutableMapping, Optional, Sequence

from asset import Asset, AssetType
from asset.abstract_asset_manager import AAssetManager
from asset.asset_type_manager import AssetTypeManager
from database import DataType, DataTypes
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from exceptions.asset import AssetTypeDoesNotExistException
from exceptions.common import KeyConstraintException


class AssetManager(AAssetManager):
    """This is the ``AssetManager``."""

    _conversions: Mapping[DataType, callable] = {
        DataTypes.TEXT.value: str,
        DataTypes.NUMBER.value: float,
        DataTypes.INTEGER.value: int,
        DataTypes.BOOLEAN.value: bool,
        DataTypes.DATETIME.value: lambda timestamp: datetime.fromtimestamp(timestamp),
        DataTypes.DATE.value: lambda timestamp: datetime.fromtimestamp(timestamp).date(),
        DataTypes.ASSET.value: int,
        DataTypes.ASSETLIST.value: lambda al: [int(a) for a in al.split(';')]
    }

    # Required fields
    asset_type_manager: AssetTypeManager = None
    db_connection: DbConnection = None

    def __init__(self):
        """Create a new ``AssetManager``."""

        self.db_connection: DbConnection = SqliteConnection.get()
        self.asset_type_manager: AssetTypeManager = AssetTypeManager()

    def create_asset(self, asset_type: AssetType, asset: Asset) -> Optional[Asset]:
        """Create an asset in the database."""

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            return None

        created: datetime = datetime.now()
        values = (self.db_connection.convert_data_to_row(asset.data, asset_type.columns))
        values.update({'primary_key': None, 'abintern_created': int(created.timestamp())})

        asset_id = self.db_connection.write_dict(asset_type.asset_table_name, values)
        self.db_connection.commit()

        return Asset(data=asset.data, asset_id=asset_id, created=created.replace(microsecond=0))

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

        # Making sure the asset_type_id table is set
        if not asset_type.asset_table_name:
            raise AttributeError("The asset_type_table parameter of asset_type_id must be set!")

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            raise AssetTypeDoesNotExistException(f"The asset type {asset_type} does not exist!")

        data = self.db_connection.convert_data_to_row(asset.data, asset_type.columns)
        data.update({'primary_key': asset.asset_id})

        self.db_connection.update(asset_type.asset_table_name, data)

    def get_one(self, asset_id: int, asset_type: AssetType, depth: int = 0) -> Optional[Asset]:
        """Get the ``Asset`` with ``asset_id`` from the database."""

        result: Sequence[MutableMapping[str, Any]] = self.db_connection.read(
            table_name=self.asset_type_manager.generate_asset_table_name(asset_type),
            headers=[column.db_name for column in asset_type.columns] + ['primary_key', 'abintern_created'],
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
            data=self.convert_row_to_data(result[0], asset_type.columns, depth)
        )
        return asset

    def get_all(self, asset_type: AssetType, depth: int = 0) -> List[Asset]:
        """Get all assets of ``AssetType`` from the database."""

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            raise AssetTypeDoesNotExistException()

        results: Sequence[MutableMapping[str, Any]] = self.db_connection.read(
            self.asset_type_manager.generate_asset_table_name(asset_type),
            [column.db_name for column in asset_type.columns])

        return self._convert_results_to_assets(results, asset_type, depth)

    def get_all_filtered(
            self, asset_type: AssetType,
            depth: int = None,
            and_filters: Sequence[str] = None,
            or_filters: Sequence[str] = None) -> List[Asset]:
        """Get all (filtered) assets of ``AssetType`` from the database."""

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            raise AssetTypeDoesNotExistException()

        results: Sequence[MutableMapping[str, Any]] = self.db_connection.read(
            self.asset_type_manager.generate_asset_table_name(asset_type),
            [column.db_name for column in asset_type.columns],
            and_filters=and_filters, or_filters=or_filters
        )

        return self._convert_results_to_assets(results, asset_type, depth)

    def get_batch(
            self, asset_type: AssetType,
            offset: int, limit: int,
            depth: int = None) \
            -> List[Asset]:
        """Get a batch of assets of ``AssetType`` from the database."""

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            raise AssetTypeDoesNotExistException()

        results: Sequence[MutableMapping[str, Any]] = self.db_connection.read(
            self.asset_type_manager.generate_asset_table_name(asset_type),
            [column.db_name for column in asset_type.columns],
            limit=limit, offset=offset
        )

        return self._convert_results_to_assets(results, asset_type, depth)

    def count(self, asset_type: AssetType):
        """Count the number of assets of the given type."""

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            raise AssetTypeDoesNotExistException()

        count: int = self.db_connection.count(asset_type.asset_table_name)
        return count

    def _convert_results_to_assets(self, results, asset_type, depth):
        """Convert the db results to a list of Assets."""

        assets = []

        for asset_row in results:
            assets.append(Asset(
                asset_id=asset_row.pop('primary_key'),
                data=self.convert_row_to_data(asset_row, asset_type.columns, depth)
            ))

        return assets
