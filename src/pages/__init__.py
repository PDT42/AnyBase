"""
:Author: PDT
:Since: 2020/06/12

This is the package for all frontend creating stuff.
# TODO
"""

from dataclasses import dataclass
from typing import List, Sequence

from asset import Asset, AssetType


@dataclass
class ColumnInfo:
    """This is one column if a layout."""
    column_width: int
    plugin_name: str
    plugin_path: str
    employed_columns: Sequence[str]
    column_id: int = None


@dataclass
class RowInfo:
    """This is one row of a layout."""
    columns: List[ColumnInfo]


@dataclass
class PageLayout:
    """This is a ``PageLayout``."""
    layout: List[RowInfo]
    layout_id: int


@dataclass
class AssetDetailPage(PageLayout):
    """This is an ``AssetDetailPage``."""
    asset: Asset


@dataclass
class AssetTypePage(PageLayout):
    """This is an ``AssetTypePage``."""
    asset_type: AssetType
    assets: List[Asset]
