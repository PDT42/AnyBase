"""
:Author: PDT
:Since: 2020/07/26

This is an abstract implementation of an asset manager. It is supposed to act as an
interface and provide a rule as to what an asset manager must look like to be operated
by the system.
"""

from abc import abstractmethod
from typing import Any, List, Mapping, MutableMapping, Optional, Sequence

from asset import Asset, AssetType
from asset.asset_type_manager import AssetTypeManager
from database import Column, DataType, DataTypes
from database.db_connection import DbConnection


class AAssetManager:
    """This is the abstract class for asset managers."""

    _conversions: Mapping[DataType, callable] = None

    asset_type_manager: AssetTypeManager = None
    db_connection: DbConnection = None

    @abstractmethod
    def create_asset(self, asset_type: AssetType, asset: Asset) -> Optional[Asset]:
        """Create an asset in the database."""
        pass

    @abstractmethod
    def delete_asset(self, asset_type: AssetType, asset: Asset) -> None:
        """Delete an asset from the system."""
        pass

    @abstractmethod
    def update_asset(self, asset_type: AssetType, asset: Asset) -> None:
        """Update the information on an asset in the database."""
        pass

    @abstractmethod
    def get_one(self, asset_id: int, asset_type: AssetType, depth: int = 0) -> Optional[Asset]:
        """Get the ``Asset`` with ``asset_id`` from the database."""
        pass

    @abstractmethod
    def get_all(self, asset_type: AssetType) -> List[Asset]:
        """Get all assets of ``AssetType`` from the database."""
        pass

    @abstractmethod
    def get_all_filtered(
            self, asset_type: AssetType,
            depth: int = None,
            and_filters: Sequence[str] = None,
            or_filters: Sequence[str] = None) -> List[Asset]:
        """Get all assets of ``AssetType`` from the database."""
        pass

    @abstractmethod
    def get_batch(
            self, asset_type: AssetType,
            offset: int, limit: int,
            depth: int = None) \
            -> List[Asset]:
        """Get all assets of ``AssetType`` from the database."""
        pass

    @abstractmethod
    def count(self, asset_type: AssetType):
        """Count the number of assets of the given type."""
        pass

    def convert_row_to_data(
            self, row: MutableMapping[str, Any],
            columns: List[Column],
            depth: int = 0) \
            -> MutableMapping[str, Any]:
        """Convert a row to a valid data entry of an ``Asset``."""

        received_data: MutableMapping[str, Any] = {}

        for column in columns:

            field = self._conversions[column.datatype](row[column.db_name])

            if column.datatype is DataTypes.ASSET.value and depth > 0:
                asset_type = self.asset_type_manager.get_one(column.asset_type_id)
                asset = self.get_one(field, asset_type, depth - 1)

                received_data[column.db_name] = asset

            elif column.datatype is DataTypes.ASSETLIST.value and depth > 0:
                asset_type = self.asset_type_manager.get_one(column.asset_type_id)

                received_data[column.db_name] = [
                    self.get_one(int(asset), asset_type, depth - 1) for asset in field
                ]

            else:
                received_data[column.db_name] = field
        return received_data
