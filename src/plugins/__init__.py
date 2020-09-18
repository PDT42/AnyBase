"""
:Author: PDT
:Since: 2020/08/26

This is the plugins package. In this module we define the plugin register.
"""

from dataclasses import dataclass
from enum import Enum
from enum import unique
from typing import Any
from typing import Dict
from typing import Optional
from typing import Type
from uuid import uuid4

from plugins.abstract_plugin import APluginServer


class PluginType(Enum):
    """These are the PluginTypes available."""

    HYBRID = 'hybrid'
    ASSET_TYPE = 'asset_type'
    ASSET = 'asset'


@dataclass
class Plugin:
    """This is a plugin. It is crucial - trust me."""

    id: str  # The id doubles as name
    view: str  # Path to jinja view template -> later _source_?
    server: Optional[Type[APluginServer]]
    type: PluginType

    def __hash__(self):
        return int(uuid4())

    def __eq__(self, other):
        if not isinstance(other, Plugin):
            return False
        if not self.view == other.view and not self.id == other.id:
            return False
        return True

    def as_dict(self) -> Dict[str, Any]:
        """Get a dict representation of a Plugin."""

        return {
            'id': self.id,
            'view': self.view,
        }


@unique
class PluginRegister(Enum):
    """This is the ``PluginRegister``. It represents the connection
    between the ``id`` stored in the ``ColumnInfo``"""

    from plugins.notes_plugin import NotesPluginServer

    BASIC_NOTES = Plugin(
        id='basic-notes',
        view='plugins/basic-notes-plugin.html',
        server=NotesPluginServer,
        type=PluginType.HYBRID
    )

    ASSET_DETAILS = Plugin(
        id='asset-details',
        view='plugins/asset-details-plugin.html',
        server=None,
        type=PluginType.ASSET
    )

    LIST_ASSETS = Plugin(
        id='list-assets',
        view='plugins/list-assets-plugin.html',
        server=None,
        type=PluginType.ASSET_TYPE
    )

    # --

    @classmethod
    def get_all_plugins(cls):
        """Get all distinct field values from enum."""
        return list(set(
            [mapping.value for
             mapping in cls.__members__.values()
             if isinstance(mapping.value, Plugin)
             ]))

    @classmethod
    def get_all_plugin_ids(cls):
        """Get the names of all available data types."""
        return list(cls.__members__.keys())
