"""
:Author: PDT
:Since: 2020/05/28

This is the the module for the AssetManager.
"""

from collections import OrderedDict
from datetime import datetime
from typing import Any, List, Mapping, MutableMapping, Optional, Sequence, Set, Tuple

from asset import Asset, AssetType
from asset.abstract_asset_manager import AAssetManager
from asset.asset_type_manager import AssetTypeManager
from database import Column, DataType, DataTypes
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from exceptions.asset import AssetChangedException, AssetTypeDoesNotExistException, SuperAssetDoesNotExistException, \
    SuperTypeDoesNotExistException
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

        self.PRIMARY_KEY = 'primary_key'
        self.JOIN_ON: str = 'abintern_extended_by_id'
        self.CREATED: str = 'abintern_created'
        self.UPDATED: str = 'abintern_updated'

        self.ASSET_HEADERS = [self.PRIMARY_KEY, self.CREATED, self.JOIN_ON, self.UPDATED]

    def create_asset(self, asset_type: AssetType, asset: Asset) -> Optional[Asset]:
        """Create an asset in the database."""

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            return None

        # If the asset has a super type, we won't be able to store
        # all the data in asset.data in the asset database table.
        # We need to create a super type asset and let it handle
        # the additional data.

        if (super_id := asset_type.get_super_type_id()) > 0:

            super_type: AssetType = self.asset_type_manager.get_one_by_id(super_id)

            if not super_type:
                raise SuperTypeDoesNotExistException()

            # Passing all the data this asset won't be able to store
            # in its own database table up to the super asset.

            asset_headers: Set[str] = {col.db_name for col in asset_type.columns}
            super_headers: Set[str] = set(asset.data.keys()) - asset_headers
            super_data: MutableMapping[str, Any] = {
                header: asset.data[header] for header in super_headers
            }

            super_asset: Asset = self.create_asset(super_type, Asset(data=super_data))
            asset.extended_by_id = super_asset.asset_id

        created: datetime = datetime.now().replace(microsecond=0)

        values = self.db_connection.convert_data_to_row(asset.data, asset_type.columns)
        values.update({
            self.PRIMARY_KEY: None,
            self.CREATED: int(created.timestamp()),
            self.UPDATED: int(created.timestamp()),
            self.JOIN_ON: asset.extended_by_id
        })

        asset_id = self.db_connection.write_dict(asset_type.asset_table_name, values)
        self.db_connection.commit()

        return Asset(
            data=asset.data,
            asset_id=asset_id,
            created=created,
            updated=created,
            extended_by_id=asset.extended_by_id
        )

    def delete_asset(self, asset_type: AssetType, asset: Asset):
        """Delete an asset from the system."""

        # TODO: Ensure that AssetType does not contain extension columns

        if (super_id := asset_type.get_super_type_id()) > 0:
            super_type: AssetType = self.asset_type_manager.get_one_by_id(super_id)
            super_asset: Asset = self.get_one(asset.extended_by_id, super_type)
            self.delete_asset(super_type, super_asset)

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

        if (super_id := asset_type.get_super_type_id()) > 0:

            super_type: AssetType = self.asset_type_manager.get_one_by_id(super_id)

            if not super_type:
                raise SuperTypeDoesNotExistException()

            # Passing all the data this asset won't be able to store
            # in its own database table up to the super asset.

            asset_headers: Set[str] = {col.db_name for col in asset_type.columns}
            super_headers: Set[str] = set(asset.data.keys()) - asset_headers

            # Making sure, the super type of this asset exists
            if not (super_asset := self.get_one(asset.extended_by_id, super_type)):
                raise SuperAssetDoesNotExistException(
                    "The super asset of this asset does not exist! " +
                    "This means a constraint failure - that's shit!"
                )

            # Updating the super assets data
            super_asset.data = {
                header: asset.data[header] for header in super_headers
            }

            self.update_asset(super_type, super_asset)

        old_asset: Asset = self.get_one(asset.asset_id, asset_type)

        if old_asset.updated > asset.updated:
            raise AssetChangedException("The asset you are trying to update has changed!")

        updated: datetime = datetime.now().replace(microsecond=0)

        data = self.db_connection.convert_data_to_row(asset.data, asset_type.columns)
        data.update({
            self.PRIMARY_KEY: asset.asset_id,
            self.CREATED: int(asset.created.timestamp()),
            self.UPDATED: int(updated.timestamp()),
            self.JOIN_ON: asset.extended_by_id
        })

        self.db_connection.update(asset_type.asset_table_name, data)

        return Asset(
            data=asset.data,
            created=asset.created,
            updated=updated,
            asset_id=asset.asset_id,
            extended_by_id=asset.extended_by_id
        )

    def get_one(
            self, asset_id: int,
            asset_type: AssetType,
            depth: int = 0,
            extend: bool = True) \
            -> Optional[Asset]:
        """Get the ``Asset`` with ``asset_id`` from the database."""

        # Creating the list of headers required for this asset
        headers: List[str] = [column.db_name for column in asset_type.columns]
        headers.extend(self.ASSET_HEADERS)

        # Check if we need to supplement the asset
        # with additional data from a super asset.

        if asset_type.get_super_type_id() > 0:

            table_name, table_headers, result_columns = \
                self._extract_joined_parameters(asset_type)

            result: Sequence[MutableMapping[str, Any]] = \
                self.db_connection.read_joined(
                    and_filters=[f'{table_name}.primary_key = {asset_id}'],
                    table_headers=table_headers
                )

        # Or we don't need to use read_joined

        else:
            result_columns: List[Column] = asset_type.columns
            result: Sequence[MutableMapping[str, Any]] = self.db_connection.read(
                table_name=self.asset_type_manager.generate_asset_table_name(asset_type),
                headers=headers, and_filters=[f'primary_key = {asset_id}']
            )

        if not result:
            return None

        if len(result) > 1:
            raise KeyConstraintException(
                "There is a real big problem here! Real biggy - Trust me! " +
                "The primary key constraint is broken!"
            )

        return self._convert_result_to_asset(result[0], result_columns, depth)

    def get_all(self, asset_type: AssetType, depth: int = 0) -> List[Asset]:
        """Get all assets of ``AssetType`` from the database."""

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            raise AssetTypeDoesNotExistException()

        headers: List[str] = [column.db_name for column in asset_type.columns]
        headers.extend(self.ASSET_HEADERS)

        # Check if the requested asset type defines a super type.
        # If that is the case, we need to supplement the assets
        # data, with data from the super asset it references.
        # We also need to consider cases, in which multiple assets
        # are chained in child-parent/extension hierarchies.

        if asset_type.get_super_type_id() > 0:

            table_headers, result_columns = \
                self._extract_joined_parameters(asset_type)

            results: Sequence[MutableMapping[str, Any]] = self.db_connection.read_joined(
                table_headers=table_headers)

        else:
            result_columns: List[Column] = asset_type.columns
            results: Sequence[MutableMapping[str, Any]] = self.db_connection.read(
                table_name=self.asset_type_manager.generate_asset_table_name(asset_type),
                headers=headers
            )

        return self._convert_results_to_assets(results, result_columns, depth)

    def get_all_filtered(
            self, asset_type: AssetType,
            depth: int = None,
            and_filters: Sequence[str] = None,
            or_filters: Sequence[str] = None) -> List[Asset]:
        """Get all (filtered) assets of ``AssetType`` from the database."""

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            raise AssetTypeDoesNotExistException()

        headers: List[str] = [column.db_name for column in asset_type.columns]
        headers.extend(self.ASSET_HEADERS)

        if asset_type.get_super_type_id() > 0:

            table_headers, result_columns = \
                self._extract_joined_parameters(asset_type)

            results: Sequence[MutableMapping[str, Any]] = self.db_connection.read_joined(
                table_headers=table_headers, and_filters=and_filters, or_filters=or_filters)

        else:
            result_columns: List[Column] = asset_type.columns
            results: Sequence[MutableMapping[str, Any]] = self.db_connection.read(
                table_name=self.asset_type_manager.generate_asset_table_name(asset_type),
                headers=headers, and_filters=and_filters, or_filters=or_filters
            )

        return self._convert_results_to_assets(results, result_columns, depth)

    def get_batch(
            self, asset_type: AssetType,
            offset: int, limit: int,
            depth: int = None) -> List[Asset]:
        """Get a batch of assets of ``AssetType`` from the database."""

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            raise AssetTypeDoesNotExistException()

        headers: List[str] = [column.db_name for column in asset_type.columns]
        headers.extend(self.ASSET_HEADERS)

        if asset_type.get_super_type_id() > 0:

            table_headers, result_columns = \
                self._extract_joined_parameters(asset_type)

            results: Sequence[MutableMapping[str, Any]] = self.db_connection.read_joined(
                table_headers=table_headers, limit=limit, offset=offset)

        else:
            result_columns: List[Column] = asset_type.columns
            results: Sequence[MutableMapping[str, Any]] = self.db_connection.read(
                table_name=self.asset_type_manager.generate_asset_table_name(asset_type),
                headers=headers, limit=limit, offset=offset
            )

        return self._convert_results_to_assets(results, result_columns, depth)

    def count(self, asset_type: AssetType):
        """Count the number of assets of the given type."""

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            raise AssetTypeDoesNotExistException()

        count: int = self.db_connection.count(asset_type.asset_table_name)
        return count

    #
    # PRIVATE METHODS
    # ~~~~~~~~~~~~~~~
    #

    def _convert_result_to_asset(self, result, result_columns, depth):
        """Convert a single result to an asset."""
        return Asset(
            asset_id=result.pop(self.PRIMARY_KEY),
            data=self.convert_row_to_data(result, result_columns, depth),
            created=datetime.fromtimestamp(result[self.CREATED]),
            updated=datetime.fromtimestamp(result[self.UPDATED]),
            extended_by_id=result[self.JOIN_ON]
        )

    def _convert_results_to_assets(self, results, result_columns, depth):
        """Convert the db results to a list of Assets."""

        assets = []

        for result in results:
            assets.append(self._convert_result_to_asset(result, result_columns, depth))
        return assets

    def _extract_joined_parameters(self, asset_type: AssetType):
        """Extract the parameters required for a joined read from an asset type."""

        table_headers: OrderedDict[str, Tuple[str, Sequence[str]]] = OrderedDict()
        result_columns: List[Column] = []

        table_name: str = self.asset_type_manager.generate_asset_table_name(asset_type)
        table_headers[table_name] = \
            (self.JOIN_ON, self.ASSET_HEADERS + [c.db_name for c in asset_type.columns])
        result_columns.extend(asset_type.columns)

        inspected_type: AssetType = asset_type

        while (super_id := inspected_type.get_super_type_id()) > 0:
            inspected_type = self.asset_type_manager.get_one(super_id)
            result_columns.extend(inspected_type.columns)
            table_headers[inspected_type.asset_table_name] = \
                (self.JOIN_ON, [column.db_name for column in inspected_type.columns])

        return table_headers, result_columns
