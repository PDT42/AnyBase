"""
:Author: PDT
:Since: 2020/07/26

This is an abstract implementation of an asset manager. It is supposed to act as an
interface and provide a rule as to what an asset manager must look like to be operated
by the system.
"""

from abc import abstractmethod
from typing import Any, List, MutableMapping, Optional, Sequence

from asset import Asset, AssetType
from asset.asset_type_manager import AssetTypeManager
from database import Column
from database.db_connection import DbConnection


class AAssetManager:
    """This is the abstract class for asset managers."""

    asset_type_manager: AssetTypeManager = None
    db_connection: DbConnection = None

    @abstractmethod
    def create_asset(self, asset_type: AssetType, asset: Asset) -> None:
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
    def get_all(self, asset_type: AssetType) -> List[Asset]:
        """Get all assets of ``AssetType`` from the database."""
        pass

    @abstractmethod
    def get_one(self, asset_id: int, asset_type: AssetType) -> Optional[Asset]:
        """Get the ``Asset`` with ``asset_id`` from the database."""
        pass

    @abstractmethod
    def convert_row_to_data(
            self, row: MutableMapping[str, Any],
            columns: Sequence[Column],
            depth: int = 0) \
            -> MutableMapping[str, Any]:
        """Convert a row to a valid data entry of an ``Asset``."""
        pass
