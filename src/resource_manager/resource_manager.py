"""
:Author: PDT
:Since: 2020/05/28

This is the the module for the resource manager.
"""

from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from resource_manager import Resource, ResourceType


class ResourceManager:
    """This is the ``ResourceManager``."""

    def __init__(self):
        """Create a new ``ResourceManager``."""

        self.db_connection: DbConnection = SqliteConnection.get()

    def create_resource(self, resource: Resource):
        """TODO"""

        self.db_connection.write_dict(resource.resource_type.resource_table_name, resource.data)

    def _check_resource_type_exists(self, resource_type: ResourceType) -> bool:
        """Check if ``resource_type`` exists."""
