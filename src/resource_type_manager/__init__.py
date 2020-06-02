"""
:Author: PDT
:Since: 2020/06/02

The package contains the ResourceTypeManager.
"""
from typing import NamedTuple, Sequence

from database import Column


class ResourceType(NamedTuple):
    """This is a ``ResourceType``, it defines a resource."""

    resource_type_id: str
    resource_name: str
    resource_table_name: str
    columns: Sequence[Column]
