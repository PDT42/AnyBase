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
from typing import Mapping
from typing import Optional
from typing import Set
from typing import Type
from uuid import uuid4


class PluginType(Enum):
    """These are the PluginTypes available."""

    HYBRID = 'hybrid'
    ASSET_TYPE = 'asset_type'
    ASSET = 'asset'


@dataclass
class PluginField:
    """This is a PluginField."""

    field_id: str
    field_label: str
    mapping: str

    def as_dict(self) -> Dict[str, Any]:
        """Get a dict representation of a PluginField."""

        return {
            'field_id': self.field_id,
            'field_label': self.field_label,
            'mapping': self.mapping
        }


@dataclass
class Plugin:
    """This is a plugin. It is crucial - trust me."""

    name: str
    id: str
    view: str  # Path to jinja view template -> later _source_?
    server: Optional[Type['APluginServer']]
    fields: Set[str]
    allow_custom_mappings: bool
    allow_custom_fields: bool
    default_field_mappings: Optional[Mapping[str, str]]
    plugin_type: PluginType

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
            'name': self.name,
            'id': self.id,
            'view': self.view,
            'fields': list(self.fields) if self.fields else [],
            'allow_custom_mappings': self.allow_custom_mappings,
            'allow_custom_fields': self.allow_custom_fields
        }


@unique
class PluginRegister(Enum):
    """This is the ``PluginRegister``. It represents the connection
    between the ``id`` stored in the ``ColumnInfo``"""

    from plugins.notes_plugin import NotesPluginServer
    from plugins.calendar_plugin import CalendarServer

    BASIC_NOTES = Plugin(
        name='Basic Notes',
        id='basic-notes',
        view='plugins/basic-notes-plugin.html',
        fields={'title', 'note', 'author'},
        allow_custom_mappings=False,
        allow_custom_fields=False,
        default_field_mappings={
            'title': 'title',  # The right must be column.db_names.
            'note': 'note',
            'author': 'author'
        },
        server=NotesPluginServer,
        plugin_type=PluginType.HYBRID
    )

    CALENDAR = Plugin(
        name='Calendar',
        id='calendar',
        view='plugins/calendar-plugin.html',
        fields=set(),
        allow_custom_mappings=False,
        allow_custom_fields=False,
        default_field_mappings={
            'title': 'title'
        }, server=CalendarServer,
        plugin_type=PluginType.HYBRID
    )

    ASSET_DETAILS = Plugin(
        name='Asset Details',
        id='asset-details',
        view='plugins/asset-details-plugin.html',
        fields=set(),
        allow_custom_mappings=True,
        allow_custom_fields=True,
        default_field_mappings=None,
        server=None,
        plugin_type=PluginType.ASSET
    )

    LIST_ASSETS = Plugin(
        name='List Assets',
        id='list-assets',
        view='plugins/list-assets-plugin.html',
        fields={'field-title'},
        allow_custom_mappings=True,
        allow_custom_fields=True,
        default_field_mappings=None,
        server=None,
        plugin_type=PluginType.ASSET_TYPE
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
