"""
:Author: PDT
:Since: 2020/07/26

This is the abstract implementation of an asset type manager. It is
to be thought of as a template for what an asset type manager should
look like. It also sets some standards of what such a manager must
be capable of for it to be operated by the system and what certain
infrastructural parts should be formed like, in order to maintain
interoperability.
"""

from abc import abstractmethod
from typing import List, Optional, Sequence

from asset import AssetType
from database import Column, DataTypes


class AAssetTypeManager:
    """This is the abstract class for AssetTypeManagers."""

    @abstractmethod
    def create_asset_type(self, asset_type: AssetType) -> None:
        """Create a new ``asset_type`` in the asset type registry."""
        pass

    @abstractmethod
    def delete_asset_type(self, asset_type: AssetType) -> None:
        """Delete ``asset_type`` and all it's assets from the system."""
        pass

    @abstractmethod
    def update_asset_type(self, asset_type: AssetType) -> None:
        """Update an ``asset_type`` in the database."""
        pass

    @abstractmethod
    def check_asset_type_exists(self, asset_type: AssetType) -> bool:
        """Check if ``asset_type`` with that name already exists."""
        pass

    @abstractmethod
    def get_all(self) -> List[AssetType]:
        """Get all ``AssetTypes`` registered in the database."""
        pass

    @abstractmethod
    def get_all_filtered(
            self, and_filters: Sequence[str] = None,
            or_filters: Sequence[str] = None) \
            -> List[AssetType]:
        """Get all ``AssetTypes`` for which the given filters apply."""
        pass

    @abstractmethod
    def get_batch(self, offset: int, limit: int):
        """Get a batch of ``AssetTypes`` from offset until limit."""
        pass

    @abstractmethod
    def get_one(self, asset_type_id: int) -> Optional[AssetType]:
        """Get the ``AssetType`` with ident ``asset_type_id``."""
        pass

    @staticmethod
    def generate_column_str_from_columns(columns: Sequence[Column]) -> str:
        """Generate a column str from a list of Columns. This method
        is part of the abstract asset type manager, to ensure
        interoperability of different implementations of asset type
        managers. The way an asset type store the columns of an asset
        is a basic concept of the software and should be the same
        everywhere."""

        column_str: str = ';'.join([
            f"{column.name}," +
            f"{column.datatype.typename}," +
            f"{int(column.asset_type)}," +
            f"{int(column.required)}"
            for column in columns
        ])

        return column_str

    @staticmethod
    def generate_columns_from_columns_str(column_str: str) -> List[Column]:
        """Create a ``AssetType`` object from parameters. This function
        is part of the abstract asset type manager for the same reasons
        as for generate_str_column_from_columns. This it's counterpart.
        """

        columns: List[Column] = []

        for column_str in column_str.split(';'):
            column_str = column_str.split(',')

            columns.append(Column(
                name=' '.join(column_str[:-3]),
                db_name='_'.join(column_str[:-3]).lower(),
                datatype=DataTypes[column_str[-3]].value,
                asset_type=int(column_str[-2]),
                required=bool(int(column_str[-1]))
            ))

        return columns

    @staticmethod
    def generate_asset_table_name(asset_type: AssetType) -> str:
        """Generate an ``asset_table_name`` from the ``asset type``.
        This method is part of the abstract asset type manager, to
        ensure, that future implementations still support the same
        naming convention."""

        asset_table_name = f"abasset_table_{asset_type.asset_name.replace(' ', '_').lower()}"
        return asset_table_name
