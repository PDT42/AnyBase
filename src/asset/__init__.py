"""
:Author: PDT
:Since: 2020/05/28

The package contains the AssetManager and the AssetTypeManager.
"""
import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, List, MutableMapping, Optional

from database import Column, DataTypes


@dataclass
class AssetType:
    """This is a ``AssetType``, it defines an asset."""

    asset_name: str
    columns: List[Column]
    asset_table_name: str = None
    asset_type_id: int = None
    is_subtype: bool = False
    super_type_id: int = 0


@dataclass
class AssetTypePrefab:
    """This is an ``AssetTypePrefab``."""

    prefab_name: str
    columns: List[Column]


@dataclass
class AssetTypePrefabs(Enum):
    """These are the available ``AssetTypePrefabs``."""

    ADDRESS = AssetTypePrefab(
        prefab_name="Address",
        columns=[
            Column("Country", "country", DataTypes.TEXT.value, required=True),
            Column("City", "city", DataTypes.TEXT.value, required=True),
            Column("Street", "street", DataTypes.TEXT.value, required=True),
            Column("ZipCode", "zipcode", DataTypes.INTEGER.value, required=True),
            Column("House Number", "house_number", DataTypes.INTEGER.value, required=True),
        ],
    )

    # --

    @classmethod
    def get_all_asset_type_prefabs(cls):
        """Get all distinct field values from enum."""
        return list(set([prefab.value for prefab in cls.__members__.values()]))

    @classmethod
    def get_all_asset_type_prefab_names(cls):
        """Get the names of all available asset type prefabs."""
        return list(cls.__members__.keys())


@dataclass
class Asset:
    """This is an ``Asset``."""

    data: MutableMapping[Any, Any]
    asset_id: Optional[int] = None

    def to_json(self):
        return json.dumps({'data': self.data, 'asset_id': self.asset_id})
