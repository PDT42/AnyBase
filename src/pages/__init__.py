"""
:Author: PDT
:Since: 2020/06/12

This is the package for all frontend creating stuff.
# TODO
"""
from dataclasses import dataclass
from typing import List, Optional, Sequence, Union

from asset import Asset, AssetType


@dataclass
class ColumnInfo:
    """This is one column if a layout."""
    plugin_name: str
    plugin_path: str
    column_width: int
    employed_columns: Sequence[str]
    column_id: int = None

    def as_dict(self):
        return {
            'column_width': self.column_width,
            'plugin_name': self.plugin_name,
            'plugin_path': self.plugin_path,
            'employed_columns': self.employed_columns,
            'column_id': self.column_id
        }


@dataclass
class PageLayout:
    """This is a ``PageLayout``."""
    layout: List[List[ColumnInfo]]
    asset_type: AssetType
    layout_id: int = None
    items_url: Optional[str] = None
    asset: Optional[Asset] = None
