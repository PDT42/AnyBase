"""
:Author: PDT
:Since: 2020/05/28

The package contains the AssetManager and the AssetTypeManager.
"""
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Any, List, MutableMapping, Optional, Union
from uuid import uuid4

from database import Column


@dataclass
class AssetType:
    """This is a ``AssetType``, it defines an asset."""

    asset_name: str
    columns: List[Column]
    created: datetime = None
    updated: datetime = None
    asset_table_name: str = None
    asset_type_id: int = None
    super_type: Union['AssetType', int] = 0
    owner_id: int = 0

    def as_dict(self):
        return {
            'asset_name': self.asset_name,
            'columns': [col.as_dict() for col in self.columns],
            'created': int(self.created.timestamp()),
            'updated': int(self.created.timestamp()),
            'asset_table_name': self.asset_table_name,
            'asset_type_id': self.asset_type_id,
            'super_type': self.super_type,
            'owner_id': self.owner_id
        }

    def get_super_type_id(self) -> int:
        if isinstance(self.super_type, int):
            return self.super_type
        elif isinstance(self.super_type, AssetType):
            return self.super_type.asset_type_id


@dataclass
class Asset:
    """This is an ``Asset``."""

    data: MutableMapping[Any, Any]
    created: datetime = None
    updated: datetime = None
    asset_id: Optional[int] = None
    extended_by_id: Optional[int] = 0

    def __hash__(self):
        return hash(uuid4())

    def __eq__(self, other):
        if not isinstance(other, Asset):
            return False
        if self.as_dict() == other.as_dict():
            return True
        return False

    def as_dict(self):
        """Get a dict from an Asset."""

        data = {}
        for key, value in self.data.items():
            if isinstance(value, datetime):
                data[key] = int(value.timestamp())
                continue
            if isinstance(value, date):
                data[key] = int(datetime.combine(value, time(0)).timestamp())
                continue
            if isinstance(value, type(None)):
                data[key] = 'null'
                continue
            data[key] = value

        return {
            'data': data,
            'asset_id': self.asset_id,
            'created': int(self.created.timestamp()),
            'updated': int(self.updated.timestamp()),
            'extended_by_id': self.extended_by_id
        }
