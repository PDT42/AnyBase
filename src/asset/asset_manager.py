"""
:Author: PDT
:Since: 2020/05/28

This is the the module for the AssetManager.
"""

from datetime import datetime
from typing import Any, List, Mapping, MutableMapping, Optional, Sequence, Set

from asset import Asset, AssetType
from asset.abstract_asset_manager import AAssetManager
from asset.asset_type_manager import AssetTypeManager
from database import Column, DataType, DataTypes
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from exceptions.asset import AssetTypeDoesNotExistException, SuperAssetDoesNotExistException, \
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
        self.asset_headers = ['primary_key', 'abintern_created', 'abintern_extended_by_id']

    def create_asset(self, asset_type: AssetType, asset: Asset) -> Optional[Asset]:
        """Create an asset in the database."""

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            return None

        # If the asset has a super type, we won't be able to store
        # all the data in asset.data in the asset database table.
        # We need to create a super type asset and let it handle
        # the additional data.

        if (super_id := asset_type.get_super_type_id()) > 0:

            super_type: AssetType = self.asset_type_manager.get_one(super_id)

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
            'primary_key': None,
            'abintern_created': int(created.timestamp()),
            'abintern_extended_by_id': asset.extended_by_id
        })

        asset_id = self.db_connection.write_dict(asset_type.asset_table_name, values)
        self.db_connection.commit()

        return Asset(
            data=asset.data,
            asset_id=asset_id,
            created=created,
            extended_by_id=asset.extended_by_id
        )

    def delete_asset(self, asset_type: AssetType, asset: Asset):
        """Delete an asset from the system."""

        if (super_id := asset_type.get_super_type_id()) > 0:
            super_type: AssetType = self.asset_type_manager.get_one(super_id)
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

            super_type: AssetType = self.asset_type_manager.get_one(super_id)

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

        data = self.db_connection.convert_data_to_row(asset.data, asset_type.columns)
        data.update({
            'primary_key': asset.asset_id,
            'abintern_created': int(asset.created.timestamp()),
            'abintern_extended_by_id': asset.extended_by_id
        })

        self.db_connection.update(asset_type.asset_table_name, data)

        return Asset(
            data=asset.data,
            created=asset.created,
            asset_id=asset.asset_id,
            extended_by_id=asset.extended_by_id
        )

    def get_one(self, asset_id: int, asset_type: AssetType, depth: int = 0) -> Optional[Asset]:
        """Get the ``Asset`` with ``asset_id`` from the database."""

        # Creating the list of headers_sequence required for this result_columns
        headers: List[str] = self.asset_headers + [column.db_name for column in asset_type.columns]

        # Check if we need to supplement the asset
        # with additional data from a super asset.

        if asset_type.get_super_type_id() > 0:

            table_names, headers_sequence, result_columns = \
                self._extract_joined_parameters(asset_type)

            result: Sequence[MutableMapping[str, Any]] = self.db_connection.read_joined(
                table_names=table_names,
                join_on_chain=['abintern_extended_by_id'] * (len(table_names) - 1),
                headers_sequence=headers_sequence,
                and_filters=[f'{table_names[0]}.primary_key = {asset_id}']
            )

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

        received_data: MutableMapping[str, Any] = \
            self.convert_row_to_data(result[0], result_columns, depth)

        asset = Asset(
            asset_id=result[0].pop('primary_key'),
            data=received_data,
            created=datetime.fromtimestamp(result[0]['abintern_created']),
            extended_by_id=int(result[0]['abintern_extended_by_id'])
        )
        return asset

    def get_all(self, asset_type: AssetType, depth: int = 0) -> List[Asset]:
        """Get all assets of ``AssetType`` from the database."""

        if not self.asset_type_manager.check_asset_type_exists(asset_type):
            raise AssetTypeDoesNotExistException()

        headers: List[str] = self.asset_headers + [column.db_name for column in asset_type.columns]

        # Check if the requested asset type defines a super type.
        # If that is the case, we need to supplement the assets
        # data, with data from the super asset it references.
        # We also need to consider cases, in which multiple assets
        # are chained in child-parent/extension hierarchies.

        if asset_type.get_super_type_id() > 0:

            table_names, headers_sequence, result_columns = \
                self._extract_joined_parameters(asset_type)

            results: Sequence[MutableMapping[str, Any]] = self.db_connection.read_joined(
                table_names=table_names,
                join_on_chain=['abintern_extended_by_id'] * (len(table_names) - 1),
                headers_sequence=headers_sequence
            )

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

        headers: List[str] = self.asset_headers + [column.db_name for column in asset_type.columns]

        if asset_type.get_super_type_id() > 0:

            table_names, headers_sequence, result_columns = \
                self._extract_joined_parameters(asset_type)

            results: Sequence[MutableMapping[str, Any]] = self.db_connection.read_joined(
                table_names=table_names,
                join_on_chain=['abintern_extended_by_id'] * (len(table_names) - 1),
                headers_sequence=headers_sequence,
                and_filters=and_filters,
                or_filters=or_filters
            )

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

        headers: List[str] = self.asset_headers + [column.db_name for column in asset_type.columns]

        if asset_type.get_super_type_id() > 0:

            table_names, headers_sequence, result_columns = \
                self._extract_joined_parameters(asset_type)

            results: Sequence[MutableMapping[str, Any]] = self.db_connection.read_joined(
                table_names=table_names,
                join_on_chain=['abintern_extended_by_id'] * (len(table_names) - 1),
                headers_sequence=headers_sequence, limit=limit, offset=offset
            )

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

    def _convert_results_to_assets(self, results, result_columns, depth):
        """Convert the db results to a list of Assets."""

        assets = []

        for asset_row in results:
            assets.append(Asset(
                asset_id=asset_row.pop('primary_key'),
                data=self.convert_row_to_data(asset_row, result_columns, depth),
                created=datetime.fromtimestamp(asset_row['abintern_created']),
                extended_by_id=asset_row['abintern_extended_by_id']
            ))

        return assets

    def _extract_joined_parameters(self, asset_type: AssetType):
        """Extract the parameters required for a joined read from an asset type."""

        table_names: List[str] = []
        headers_sequence: List[List[str]] = []
        result_columns: List[Column] = []

        table_names.append(self.asset_type_manager.generate_asset_table_name(asset_type))
        headers_sequence.append(self.asset_headers + [c.db_name for c in asset_type.columns])
        result_columns.extend(asset_type.columns)

        inspected_type: AssetType = asset_type

        while (super_id := inspected_type.get_super_type_id()) > 0:
            inspected_type = self.asset_type_manager.get_one(super_id)
            table_names.append(inspected_type.asset_table_name)
            result_columns.extend(inspected_type.columns)
            headers_sequence.append([column.db_name for column in inspected_type.columns])

        return table_names, headers_sequence, result_columns
