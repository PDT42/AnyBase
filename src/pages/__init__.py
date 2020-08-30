"""
:Author: PDT
:Since: 2020/06/12

This is the package for all frontend creating stuff.
# TODO
"""
from dataclasses import dataclass
from typing import List, Mapping, Optional, Sequence

from asset import Asset, AssetType
from exceptions.asset import MissingAssetError
from plugins import Plugin


@dataclass
class ColumnInfo:
    """This is one column if a layout."""

    plugin: Plugin
    column_width: int
    field_mappings: Mapping[str, str]
    column_id: int = None

    def as_dict(self):
        return {
            'plugin': self.plugin.as_dict(),
            'column_width': self.column_width,
            'field_mappings': self.field_mappings,
            'column_id': self.column_id
        }


@dataclass
class PageLayout:
    """This is a ``PageLayout``."""

    asset_type_id: int
    asset_page_layout: bool
    layout: List[List[ColumnInfo]]
    field_mappings: Mapping[str, str] = None
    layout_id: Optional[int] = None

    def as_dict(self):
        return {
            'asset_type_id': self.asset_type_id,
            'asset_page_layout': self.asset_page_layout,
            'layout': [[column.as_dict() for column in row] for row in self.layout],
            'field_mappings': self.field_mappings,
            'layout_id': self.layout_id
        }

