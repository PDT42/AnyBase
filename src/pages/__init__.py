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


@dataclass
class ColumnInfo:
    """This is one column if a layout."""
    plugin_name: str
    plugin_path: str
    column_width: int
    field_mappings: Mapping[str, str]
    column_id: int = None

    def as_dict(self):
        return {
            'column_width': self.column_width,
            'plugin_name': self.plugin_name,
            'plugin_path': self.plugin_path,
            'field_mappings': self.field_mappings,
            'column_id': self.column_id
        }


@dataclass
class PageLayout:
    """This is a ``PageLayout``."""

    layout: List[List[ColumnInfo]]
    asset_type: AssetType
    field_mappings: Mapping[str, str] = None
    items_url: Optional[str] = None
    layout_id: Optional[int] = None

    def as_dict(self):
        return {
            'layout': [[column.as_dict() for column in row] for row in self.layout],
            'asset_type': self.asset_type.as_dict(),
            'field_mappings': self.field_mappings,
            'items_url': self.items_url,
            'layout_id': self.layout_id
        }


@dataclass
class AssetPageLayout(PageLayout):
    """This is a ``PageLayout`` for an ``AssetPage``."""

    asset: Optional[Asset] = None

    def as_dict(self):

        if not self.asset:
            raise MissingAssetError("The of this Page is missing!")

        result_dict = super().as_dict()
        result_dict.update({
            'asset': self.asset.as_dict()
        })
        return result_dict

