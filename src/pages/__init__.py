"""
:Author: PDT
:Since: 2020/06/12

This is the package for all frontend creating stuff.
# TODO
"""

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import List
from typing import Mapping
from typing import MutableMapping
from typing import Optional
from uuid import uuid4

from plugins import Plugin


@dataclass
class ColumnInfo:
    """This is one column if a layout."""

    plugin: Plugin
    column_width: int
    field_mappings: Mapping[str, str]
    sources: MutableMapping[str, str] = None
    column_id: int = None

    def as_dict(self):
        return {
            'plugin': self.plugin.as_dict(),
            'column_width': self.column_width,
            'field_mappings': self.field_mappings,
            'sources': list(self.sources) if self.sources else [],
            'column_id': self.column_id
        }


@dataclass
class PageLayout:
    """This is a ``PageLayout``."""

    asset_type_id: int
    asset_page_layout: bool
    layout: List[List[ColumnInfo]]
    field_mappings: MutableMapping[str, str]
    created: datetime = None
    updated: datetime = None
    sources: MutableMapping[str, str] = None
    layout_id: Optional[int] = None

    def __hash__(self):
        return hash(uuid4())

    def __eq__(self, other):
        if not isinstance(other, PageLayout):
            return False

        this_dict = deepcopy(self.as_dict())
        other_dict = deepcopy(other.as_dict())

        # Let's ignore timestamps here
        for key in ['created', 'updated']:
            this_dict.pop(key)
            other_dict.pop(key)

        if this_dict == other_dict:
            return True
        return False

    def as_dict(self):
        return {
            'asset_type_id': self.asset_type_id,
            'asset_page_layout': self.asset_page_layout,
            'layout': [[column.as_dict() for column in row] for row in self.layout],
            'field_mappings': self.field_mappings if self.field_mappings else {},
            'created': int(self.created.replace(microsecond=0).timestamp()) if self.created else None,
            'updated': int(self.updated.replace(microsecond=0).timestamp()) if self.updated else None,
            'sources': self.sources if self.sources else {},
            'layout_id': self.layout_id
        }
