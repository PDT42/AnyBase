"""
:Author: PDT
:Since: 2020/05/28

The package contains the ResourceManager.
"""
from typing import Any, Mapping, NamedTuple

from resource_type_manager import ResourceType


class Resource(NamedTuple):
    """This is a ``Resource``."""

    resource_id: str
    resource_type: ResourceType
    data: Mapping[Any, Any]
