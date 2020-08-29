"""
:Author: PDT
:Since: 2020/06/02

This is the module for the AssetTypeManager.
"""
import warnings
from datetime import datetime
from typing import Any, List, Mapping, Optional, Sequence

from asset import AssetType
from asset.abstract_asset_type_manager import AAssetTypeManager
from database import Column, DataTypes
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from exceptions.asset import AssetTypeAlreadyExistsException, AssetTypeChangedException, AssetTypeDoesNotExistException, \
    AssetTypeInconsistencyException
from exceptions.common import KeyConstraintException


class AssetTypeManager(AAssetTypeManager):
    """This is the ``AssetTypeManager``."""

    # Required fields
    db_connection: DbConnection = None

    ASSET_TYPE_HEADERS: Sequence[str] = None
    _asset_types_table_name: str = None

    def __init__(self):
        """Create a new ``AssetTypeManager``."""

        self.PRIMARY_KEY = 'primary_key'
        self.CREATED = 'abintern_created'
        self.UPDATED = 'abintern_updated'

        self.ASSET_TYPE_HEADERS = [
            'asset_name',  # The name of the asset e.g: DVD, Book, Yacht, ...
            'asset_columns',  # A string generated by method in abstract superclass
            'asset_table_name',  # Name of the database table - also generated in abstract super class
            'super_type',  # Id of the asset type this one is 'sub' to
            'owner_id',  # Id of this asset types owner
            self.CREATED,  # Datetime this asset type was created
            self.UPDATED,  # Datetime this asset type was last updated
            self.PRIMARY_KEY  # Db Primary key of this type. Pk is generated by the db and is used as uid of the type
        ]
        self._asset_types_table_name = 'abintern_asset_types'

        self.db_connection = SqliteConnection.get()

    def create_asset_type(self, asset_type: AssetType) -> AssetType:
        """Create a new ``asset_type_id`` in the asset type registry."""

        # Ensuring the table, to store the asset types in, exists
        self._init_asset_types_table()

        # Assuring one can't create more than one asset type with the same name
        if self.check_asset_type_exists(asset_type):
            raise AssetTypeAlreadyExistsException(
                f"The asset type {asset_type.asset_name} already exists!")

        # Now, is when this asset type was created
        created: datetime = datetime.now().replace(microsecond=0)

        # Creating a query dict (as required by write_dict),
        # from the asset type and handing it to the database.

        asset_table_name = AssetTypeManager.generate_asset_table_name(asset_type)

        query_dict = {
            self.PRIMARY_KEY: asset_type.asset_type_id,
            'asset_name': asset_type.asset_name,
            'asset_table_name': asset_table_name,
            self.CREATED: int(created.timestamp()),
            self.UPDATED: int(created.timestamp()),
            'asset_columns': self.generate_column_str_from_columns(asset_type.columns),
            'super_type': asset_type.get_super_type_id(),
            'owner_id': asset_type.owner_id
        }

        asset_type_id = self.db_connection.write_dict(self._asset_types_table_name, query_dict)

        # Adding obligatory columns to the asset_table
        asset_table_columns = asset_type.columns + [
            Column('created', self.CREATED, DataTypes.DATETIME.value, required=True),
            Column('updated', self.UPDATED, DataTypes.DATETIME.value, required=True),
            Column('extended_by_id', 'abintern_extended_by_id', DataTypes.INTEGER.value, required=True)
        ]

        # Creating the asset table
        self.db_connection.create_table(asset_table_name, asset_table_columns)
        self.db_connection.commit()

        return AssetType(
            asset_name=asset_type.asset_name,
            columns=asset_type.columns,
            created=created,
            updated=created,
            asset_table_name=asset_table_name,
            asset_type_id=asset_type_id,
            super_type=asset_type.super_type
        )

    def delete_asset_type(self, asset_type: AssetType) -> None:
        """Delete ``asset_type_id`` and all it's assets from the system."""

        # Ensuring the table to delete
        # the asset types from exists

        self._init_asset_types_table()

        self.db_connection.delete(self._asset_types_table_name, [f"primary_key = {asset_type.asset_type_id}"])
        self.db_connection.delete_table(self.generate_asset_table_name(asset_type))
        self.db_connection.commit()

    def update_asset_type(self, asset_type: AssetType) -> AssetType:
        """Update an ``asset_type_id`` in the database."""

        # Making sure one is not trying to update an asset type without an id
        if not asset_type.asset_type_id:
            raise AttributeError(
                "The asset_type_id parameter of an AssetType " +
                "you are trying to update must exist!"
            )

        # Ensuring the table, to update the asset types in exists
        self._init_asset_types_table()

        # Getting the old asset type from the database
        db_asset_type = self.get_one(asset_type.asset_type_id)

        if not db_asset_type:
            raise AssetTypeDoesNotExistException(
                "The asset type you are trying to update does not exist!")

        # Check if the asset_type has been updated
        # by someone else in the meantime
        if db_asset_type.updated > asset_type.updated:
            raise AssetTypeChangedException(
                "The AssetType you are trying to update, has been changed!")

        # Generating the updated table name
        updated_table_name = self.generate_asset_table_name(asset_type)

        # Updating the "abasset.." tables name
        if db_asset_type.asset_name != asset_type.asset_name:

            # Making sure one can't update to a name that already exists
            if self.check_asset_type_exists(asset_type):
                raise AssetTypeAlreadyExistsException(
                    "Can't perform update - AssetType with that name already exists!")

            self.db_connection.update_table_name(
                db_asset_type.asset_table_name,
                updated_table_name)

        # Updating the "abasset.." tables columns
        if len(db_asset_type.columns) != len(asset_type.columns):
            # TODO: implement remove, append columns
            raise NotImplementedError(
                "Removing, appending columns to asset " +
                "type is not yet implemented!")

        update_columns: Mapping[str, Column] = {
            col.db_name: asset_type.columns[index]
            for index, col in enumerate(db_asset_type.columns)
        }

        self.db_connection.update_columns(updated_table_name, update_columns)

        updated: datetime = datetime.now().replace(microsecond=0)

        # Creating a query dict as required by update
        values = {
            self.PRIMARY_KEY: asset_type.asset_type_id,
            'asset_name': asset_type.asset_name,
            'asset_table_name': updated_table_name,
            self.CREATED: int(asset_type.created.timestamp()),
            self.UPDATED: int(updated.timestamp()),
            'asset_columns': self.generate_column_str_from_columns(asset_type.columns),
            'super_type': asset_type.super_type
        }
        self.db_connection.update(self._asset_types_table_name, values)

        # TODO: extend columns here?
        return self.get_one(asset_type.asset_type_id, extend_columns=True)

    def check_asset_type_exists(self, asset_type: AssetType) -> bool:
        """Check if ``asset_type_id`` with that name already exists."""

        # Making sure we aren't wandering blindly into the night
        self._init_asset_types_table()

        or_filters = [f"asset_name = '{asset_type.asset_name}'"]
        if asset_type.asset_type_id:
            or_filters = [f"primary_key = {asset_type.asset_type_id}"]

        db_response = self.db_connection.read(
            table_name=self._asset_types_table_name,
            headers=[self.PRIMARY_KEY, 'asset_name'],
            or_filters=or_filters
        )

        table_exists = self.db_connection.check_table_exists(
            AssetTypeManager.generate_asset_table_name(asset_type))
        return bool(db_response) and table_exists

    def get_one(self, asset_type_id: int, extend_columns: bool = False) -> Optional[AssetType]:
        """Get the ``AssetType`` with ident ``asset_type_id``."""

        # Ensuring the table to get asset types from exists
        self._init_asset_types_table()

        # Reading asset types from the database
        result: Sequence[Mapping[str, Any]] = self.db_connection.read(
            table_name=self._asset_types_table_name,
            headers=self.ASSET_TYPE_HEADERS,
            and_filters=[f'primary_key = {asset_type_id}']
        )

        if len(result) < 1:
            return None

        if len(result) > 1:
            raise KeyConstraintException(
                "There is a real big problem here! Real biggy - trust me." +
                "The primary key constraint is broken!"
            )

        asset_type_columns: List[Column] = \
            self.generate_columns_from_columns_str(result[0]['asset_columns'])

        if (super_type_id := int(result[0]['super_type'])) > 0 and extend_columns:
            super_type: AssetType = self.get_one(super_type_id, extend_columns=True)
            asset_type_columns.extend(super_type.columns)

        return self._convert_result_to_asset_type(result[0])

    def get_all(self, ignore_slaves: bool = True) -> List[AssetType]:
        """Get all ``AssetTypes`` registered in the database."""

        # Ensuring the table to get asset types from exists
        self._init_asset_types_table()

        and_filters: List[str] = []

        if ignore_slaves is True:
            and_filters.append('owner_id <= 0')

        # Reading asset types from the database
        results: Sequence[Mapping[str, Any]] = self.db_connection.read(
            table_name=self._asset_types_table_name,
            headers=self.ASSET_TYPE_HEADERS,
            and_filters=and_filters
        )

        return self._convert_results_to_asset_types(results)

    def get_all_filtered(
            self, and_filters: List[str] = None,
            or_filters: Sequence[str] = None,
            ignore_slaves: bool = True
    ) -> List[AssetType]:
        """Get all ``AssetTypes`` for which the given filters apply."""

        if not and_filters and not or_filters:
            warnings.warn("Call to 'get_all_filtered()' without any filters. Use 'get_all()'!")
            return self.get_all()

        and_filters = and_filters if and_filters else []
        or_filters = or_filters if or_filters else []

        if ignore_slaves is True:
            and_filters.append('owner_id <= 0')

        # Ensuring the table to get asset types from exists
        self._init_asset_types_table()

        # Reading asset types from the database
        result: Sequence[Mapping[str, Any]] = self.db_connection.read(
            table_name=self._asset_types_table_name,
            headers=self.ASSET_TYPE_HEADERS,
            and_filters=and_filters,
            or_filters=or_filters
        )

        return self._convert_results_to_asset_types(result)

    def get_batch(
            self, offset: int, limit: int,
            and_filters: List[str] = None,
            or_filters: Sequence[str] = None,
            ignore_slaves: bool = True
    ) -> List[AssetType]:
        """Get a batch of ``AssetTypes`` from offset until limit."""

        # Ensuring the table to get asset types from exists
        self._init_asset_types_table()

        and_filters = and_filters if and_filters else []
        or_filters = or_filters if or_filters else []

        if ignore_slaves is True:
            and_filters.append('owner_id <= 0')

        # Reading asset types from the database
        result: Sequence[Mapping[str, Any]] = self.db_connection.read(
            table_name=self._asset_types_table_name,
            headers=self.ASSET_TYPE_HEADERS,
            and_filters=and_filters,
            or_filters=or_filters,
            limit=limit,
            offset=offset
        )

        return self._convert_results_to_asset_types(result)

    def get_type_children(self, asset_type: AssetType):
        """Get the children tree of an asset_type."""

        children: List[AssetType] = self.get_all_filtered(
            and_filters=[f'super_type = {asset_type.asset_type_id}'])

        return children

    def get_slaves(self, asset_type: AssetType) -> List[AssetType]:
        """Get the slaves of this ``asset_type``."""

        slaves: List[AssetType] = self.get_all_filtered(
            and_filters=[f'owner_id = {asset_type.asset_type_id}'], ignore_slaves=False)

        return slaves

    def _convert_result_to_asset_type(self, result: Mapping) -> AssetType:
        """Convert one result row to an asset type."""
        return AssetType(
            asset_name=result['asset_name'],
            columns=AssetTypeManager.generate_columns_from_columns_str(result['asset_columns']),
            created=datetime.fromtimestamp(result[self.CREATED]),
            updated=datetime.fromtimestamp(result[self.UPDATED]),
            asset_table_name=result.get('asset_table_name', None),
            asset_type_id=result[self.PRIMARY_KEY],
            super_type=result['super_type'],
            owner_id=result['owner_id']
        )

    def _convert_results_to_asset_types(self, results: Sequence[Mapping]) -> List[AssetType]:
        """Convert the db results to a list of AssetTypes."""

        assets_types: List[AssetType] = []
        for result in results:
            assets_types.append(self._convert_result_to_asset_type(result))
        return assets_types

    #####################
    #  PRIVATE METHODS  #
    #####################

    def _init_asset_types_table(self) -> None:
        """Initialize the required table ``abintern_asset_types``."""

        if not self.db_connection.check_table_exists(self._asset_types_table_name):
            columns = [
                # The column primary_key will be created automatically
                Column('asset_name', 'asset_name', DataTypes.VARCHAR.value, required=True, unique=True),
                Column('asset_table_name', 'asset_table_name', DataTypes.VARCHAR.value, required=True, unique=True),
                Column('asset_columns', 'asset_columns', DataTypes.VARCHAR.value, required=True),
                Column('created', self.CREATED, DataTypes.DATETIME.value, required=True),
                Column('updated', self.UPDATED, DataTypes.DATETIME.value, required=True),
                Column('super_type', 'super_type', DataTypes.INTEGER.value, required=True),
                Column('owner_id', 'owner_id', DataTypes.INTEGER.value, required=True)
            ]
            self.db_connection.create_table(self._asset_types_table_name, columns)

    def _check_asset_type_consistency(self) -> None:
        """Check if a database table exists for all the AssetTypes
        stored in ``abintern_asset_types``."""

        asset_types: Sequence[AssetType] = self.get_all()

        if not all([self.check_asset_type_exists(asset_type) for asset_type in asset_types]):
            raise AssetTypeInconsistencyException()
