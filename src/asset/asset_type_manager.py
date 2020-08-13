"""
:Author: PDT
:Since: 2020/06/02

This is the module for the AssetTypeManager.
"""
import warnings
from typing import Any, List, Mapping, Optional, Sequence

from asset import AssetType
from asset.abstract_asset_type_manager import AAssetTypeManager
from database import Column, DataTypes
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from exceptions.asset import AssetTypeAlreadyExistsException, AssetTypeInconsistencyException
from exceptions.common import IllegalStateException, KeyConstraintException


class AssetTypeManager(AAssetTypeManager):
    """This is the ``AssetTypeManager``."""

    # TODO: Make this a singleton? Might be necessary for db concurrency.

    # Required fields
    db_connection: DbConnection = None

    _asset_headers: Sequence[str] = None
    _asset_types_table_name: str = None

    def __init__(self):
        """Create a new ``AssetTypeManager``."""

        self._asset_headers = [
            'asset_name',  # The name of the asset e.g: DVD, Book, Yacht, ...
            'asset_columns',  # A string generated by method in abstract superclass
            'asset_table_name',  # Name of the database table - also generated in abstract super class
            'is_subtype',  # Boolean field, that indicates, that this is a subtype - subtypes are special
            'super_type_id',  # Id of the asset type this one is 'sub' to
            'primary_key'  # Db Primary key of this type. Pk is generated by the db and is used as uid of the type
        ]
        self._asset_types_table_name = 'abintern_asset_types'

        self.db_connection = SqliteConnection.get()

    def create_asset_type(self, asset_type: AssetType) -> None:
        """Create a new ``asset_type_id`` in the asset type registry."""

        # Ensuring the table to store the asset types in exists
        self._init_asset_types_table()

        # Making sure one can't create more than one asset type with the same name
        if self.check_asset_type_exists(asset_type):
            raise AssetTypeAlreadyExistsException(f"The asset type {asset_type.asset_name} already exists!")

        # Making sure, that if this is a subtype, it has a parent
        if asset_type.is_subtype and not asset_type.super_type_id:
            raise IllegalStateException("If an asset type is_subtype, it needs another asset type to be sub to!")

        # If an asset type is a subtype, its assets will need
        # to reference the asset they are 'sub' to. For that
        # purpose, we add this required column.
        if asset_type.is_subtype:
            column_name = 'abintern_reference_asset_id'
            asset_type.columns.append(Column(
                column_name, column_name, DataTypes.BOOLEAN.value, required=True)
            )

        # Creating a query dict as required by write_dict
        asset_table_name = AssetTypeManager.generate_asset_table_name(asset_type)
        query_dict = {
            'primary_key': asset_type.asset_type_id,
            'asset_name': asset_type.asset_name,
            'asset_table_name': asset_table_name,
            'asset_columns': self.generate_column_str_from_columns(asset_type.columns),
            'is_subtype': asset_type.is_subtype,
            'super_type_id': asset_type.super_type_id
        }

        # Storing the type information in the appropriate table
        self.db_connection.write_dict(self._asset_types_table_name, query_dict)

        # Creating a table appropriate for the asset_type_id
        self.db_connection.create_table(asset_table_name, asset_type.columns)
        self.db_connection.commit()

    def delete_asset_type(self, asset_type: AssetType) -> None:
        """Delete ``asset_type_id`` and all it's assets from the system."""

        # Ensuring the table to delete the asset types from exists
        self._init_asset_types_table()

        self.db_connection.delete(self._asset_types_table_name, [f"primary_key = {asset_type.asset_type_id}"])
        self.db_connection.delete_table(self.generate_asset_table_name(asset_type))
        self.db_connection.commit()

    def update_asset_type(self, asset_type: AssetType) -> None:
        """Update an ``asset_type_id`` in the database."""

        # Making sure one is not trying to update an asset type without an id
        if not asset_type.asset_type_id:
            raise AttributeError("The asset_type_id parameter of an asset type you are trying to update must exist!")

        # Ensuring the table, to update the asset types in exists
        self._init_asset_types_table()

        # Getting the old asset type from the database
        db_asset_type = self.get_one(asset_type.asset_type_id)

        # Generating the updated table name
        updated_table_name = self.generate_asset_table_name(asset_type)

        # Updating the "abasset.." tables name
        if db_asset_type.asset_name != asset_type.asset_name:

            # Making sure one can't update to a name that already exists
            if self.check_asset_type_exists(asset_type):
                raise AssetTypeAlreadyExistsException("Can't perform update - AssetType with that name already exists!")

            self.db_connection.update_table_name(
                db_asset_type.asset_table_name,
                updated_table_name
            )

        # Updating the "abasset.." tables columns
        self.db_connection.update_table_columns(updated_table_name, asset_type.columns)

        # Creating a query dict as required by update
        values = {
            'primary_key': asset_type.asset_type_id,
            'asset_name': asset_type.asset_name,
            'asset_table_name': updated_table_name,
            'asset_columns': self.generate_column_str_from_columns(asset_type.columns),
            'is_subtype': asset_type.is_subtype,
            'super_type_id': asset_type.super_type_id
        }
        self.db_connection.update(self._asset_types_table_name, values)

    def check_asset_type_exists(self, asset_type: AssetType) -> bool:
        """Check if ``asset_type_id`` with that name already exists."""

        # Making sure we aren't wandering blindly into the night
        self._init_asset_types_table()

        or_filters = [f"asset_name = '{asset_type.asset_name}'"]
        if asset_type.asset_type_id:
            or_filters = [f"primary_key = {asset_type.asset_type_id}"]

        db_response = self.db_connection.read(
            table_name=self._asset_types_table_name,
            headers=['primary_key', 'asset_name'],
            or_filters=or_filters
        )

        table_exists = self.db_connection.check_table_exists(
            AssetTypeManager.generate_asset_table_name(asset_type))
        return bool(db_response) and table_exists

    def get_all(self) -> List[AssetType]:
        """Get all ``AssetTypes`` registered in the database."""

        # Ensuring the table to get asset types from exists
        self._init_asset_types_table()

        # Reading asset types from the database
        results: Sequence[Mapping[str, Any]] = self.db_connection.read(
            table_name=self._asset_types_table_name,
            headers=self._asset_headers,
        )

        return self._convert_result_to_asset_types(results)

    def get_all_filtered(
            self, and_filters: Sequence[str] = None,
            or_filters: Sequence[str] = None) \
            -> List[AssetType]:
        """Get all ``AssetTypes`` for which the given filters apply."""

        if not and_filters and not or_filters:
            warnings.warn("Call to 'get_all_filtered()' without any filters. Use 'get_all()'!")
            return self.get_all()

        # Ensuring the table to get asset types from exists
        self._init_asset_types_table()

        # Reading asset types from the database
        result: Sequence[Mapping[str, Any]] = self.db_connection.read(
            table_name=self._asset_types_table_name,
            headers=self._asset_headers,
            and_filters=and_filters,
            or_filters=or_filters
        )

        return self._convert_result_to_asset_types(result)

    def get_batch(self, offset: int, limit: int):
        """Get a batch of ``AssetTypes`` from offset until limit."""

        # Ensuring the table to get asset types from exists
        self._init_asset_types_table()

        # Reading asset types from the database
        result: Sequence[Mapping[str, Any]] = self.db_connection.read(
            table_name=self._asset_types_table_name,
            headers=self._asset_headers,
            limit=limit,
            offset=offset
        )

        return self._convert_result_to_asset_types(result)

    @staticmethod
    def _convert_result_to_asset_types(results):
        """Convert the db results to a list of AssetTypes."""

        assets_types = []
        for asset_type_row in results:
            assets_types.append(AssetType(
                asset_name=asset_type_row['asset_name'],
                columns=AssetTypeManager.generate_columns_from_columns_str(asset_type_row['asset_columns']),
                asset_table_name=asset_type_row.get('asset_table_name', None),
                asset_type_id=asset_type_row['primary_key'],
                is_subtype=asset_type_row['is_subtype'],
                super_type_id=asset_type_row['super_type_id']
            ))

        return assets_types

    def get_one(self, asset_type_id: int) -> Optional[AssetType]:
        """Get the ``AssetType`` with ident ``asset_type_id``."""

        # Ensuring the table to get asset types from exists
        self._init_asset_types_table()

        # Reading asset types from the database
        result: Sequence[Mapping[str, Any]] = self.db_connection.read(
            table_name=self._asset_types_table_name,
            headers=self._asset_headers,
            and_filters=[f'primary_key = {asset_type_id}']
        )

        if len(result) < 1:
            return None

        if len(result) > 1:
            raise KeyConstraintException(
                "There is a real big problem here! Real biggy - trust me." +
                "The primary key constraint is broken!"
            )

        asset_type = AssetType(
            asset_name=result[0]['asset_name'],
            columns=self.generate_columns_from_columns_str(result[0]['asset_columns']),
            asset_table_name=result[0].get('asset_table_name', None),
            asset_type_id=result[0]['primary_key'],
            is_subtype=result[0]['is_subtype'],
            super_type_id=result[0]['super_type_id']
        )

        return asset_type

    #####################
    #  PRIVATE METHODS  #
    #####################

    def _init_asset_types_table(self) -> None:
        """Initialize the required table ``abintern_asset_types``."""

        if not self.db_connection.check_table_exists(self._asset_types_table_name):
            columns = [
                # The column primary_key will be created automatically
                Column('asset_name', 'asset_name', DataTypes.VARCHAR.value, required=True),
                Column('asset_table_name', 'asset_table_name', DataTypes.VARCHAR.value, required=True),
                Column('asset_columns', 'asset_columns', DataTypes.VARCHAR.value, required=True),
                Column('is_subtype', 'is_subtype', DataTypes.BOOLEAN.value, required=True),
                Column('super_type_id', 'super_type_id', DataTypes.INTEGER.value, required=True)
            ]
            self.db_connection.create_table(self._asset_types_table_name, columns)

    def _check_asset_type_consistency(self) -> None:
        """Check if a database table exists for all the AssetTypes
        stored in ``abintern_asset_types``."""

        asset_types: Sequence[AssetType] = self.get_all()

        if not all([self.check_asset_type_exists(asset_type) for asset_type in asset_types]):
            raise AssetTypeInconsistencyException()
