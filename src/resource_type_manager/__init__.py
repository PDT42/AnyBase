"""
:Author: PDT
:Since: 2020/06/02

The package contains the ResourceTypeManager.
"""
from typing import NamedTuple, Sequence

from database import Column


class ResourceType(NamedTuple):
    """This is a ``ResourceType``, it defines a resource."""

    resource_name: str
    columns: Sequence[Column]
    resource_table_name: str = None
    resource_type_id: int = None
