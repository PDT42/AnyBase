"""
:Author: PDT
:Since: 2020/08/26

This is the plugins package. In this module we define the plugin register.
"""

from dataclasses import dataclass
from enum import Enum, unique
from typing import Any, Dict, Optional, Type

from plugins.abstract_plugin import APluginServer
from plugins.notes_plugin import NotesPluginServer


class PluginType(Enum):
    """These are the PluginTypes available."""

    HYBRID = 'hybrid'
    ASSET_TYPE = 'asset_type'
    ASSET = 'asset'


@dataclass
class Plugin:
    """This is a plugin. It is crucial - trust me."""

    name: str
    path: str
    server: Optional[Type[APluginServer]]
    type: PluginType

    def as_dict(self) -> Dict[str, Any]:
        """Get a dict representation of a Plugin."""

        return {
            'name': self.name,
            'path': self.path,
            # TODO: Add missing fields
        }

    def __eq__(self, other):
        if not isinstance(other, Plugin):
            return False
        if not self.path == other.path and not self.name == other.name:
            return False
        return True


@unique
class PluginRegister(Enum):
    """This is the ``PluginRegister``. It represents the connection
    between the ``name`` stored in the ``ColumnInfo``"""

    BASIC_NOTES = Plugin(
        name='basic-notes',
        path='plugins/basic-notes-plugin.html',
        server=NotesPluginServer,
        type=PluginType.HYBRID
    )

    ASSET_DETAILS = Plugin(
        name='asset-details',
        path='plugins/asset-details-plugin.html',
        server=None,
        type=PluginType.ASSET
    )

    LIST_ASSETS = Plugin(
        name='list-assets',
        path='plugins/list-assets-plugin.html',
        server=None,
        type=PluginType.ASSET_TYPE
    )

    # --

    @classmethod
    def get_all_data_types(cls):
        """Get all distinct field values from enum."""
        return list(set([data_type.value for data_type in cls.__members__.values()]))

    @classmethod
    def get_all_type_names(cls):
        """Get the names of all available data types."""
        return list(cls.__members__.keys())
