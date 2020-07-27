"""
:Author: PDT
:Since: 2020/05/28

The package contains the AssetManager and the AssetTypeManager.
"""
from dataclasses import dataclass
from typing import Any, List, MutableMapping, Optional

from database import Column


@dataclass
class AssetType:
    """This is a ``AssetType``, it defines an asset."""

    asset_name: str
    columns: List[Column]
    asset_table_name: str = None
    asset_type_id: int = None
    is_subtype: bool = False


@dataclass
class Asset:
    """This is an ``Asset``."""

    data: MutableMapping[Any, Any]
    asset_id: Optional[int] = None
