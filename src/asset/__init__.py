"""
:Author: PDT
:Since: 2020/05/28

The package contains the AssetManager and the AssetTypeManager.
"""
from typing import Any, Mapping, MutableMapping, NamedTuple, Optional, Sequence

from database import Column


class AssetType(NamedTuple):
    """This is a ``AssetType``, it defines an asset."""

    asset_name: str
    columns: Sequence[Column]
    asset_table_name: str = None
    asset_type_id: int = None


class Asset(NamedTuple):
    """This is an ``Asset``."""

    asset_id: Optional[int]
    asset_type: AssetType
    data: MutableMapping[Any, Any]
