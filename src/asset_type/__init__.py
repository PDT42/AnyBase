"""
:Author: PDT
:Since: 2020/09/15

This package contains everything ``AssetType`` related.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List
from typing import Union
from uuid import uuid4

from database import Column


@dataclass
class AssetType:
    """This is a ``AssetType``, it defines an asset."""

    asset_name: str  # Name of the asset this type defines
    columns: List[Column]  # Fields of the defined asset
    created: datetime = None  # When the type was created
    updated: datetime = None  # When the type was last updated
    asset_table_name: str = None  # Name of the table the assets of this type are stored in
    asset_type_id: int = None  # Database unique id of this type
    super_type: Union['AssetType', int] = 0  # this is either the actual item or its id
    owner_id: int = 0  # Id of the owner of assets of this type

    def __hash__(self):
        return hash(uuid4())

    def __eq__(self, other):
        if not isinstance(other, AssetType):
            return False
        if self.as_dict() == other.as_dict():
            return True
        return False

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
