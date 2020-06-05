"""
:Author: PDT
:Since: 2020/06/02

This is the module for the ResourceTypeManager.
"""

from database import Column
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from resource_manager import ResourceType


class ResourceTypeManager:
    """This is the ``ResourceTypeManager``."""

    def __init__(self):
        """Create a new ``ResourceTypeManager``."""

        self.db_connection: DbConnection = SqliteConnection.get()

    def create_resource_type(self, resource_type: ResourceType):
        """Create a new ``resource type`` in the resource type registry."""

        # Ensuring the table to store the resource types in exists
        self._init_resource_types_table()

        # Raise an exception if a type with that name already exists
        if self.check_resource_type_exists(resource_type):
            raise Exception(f"A ResourceType with the resource_name '{resource_type.resource_name}' already exists!")

        # Creating a query dict as required by write_dict
        query_dict = {
            'resource_name': resource_type.resource_name,
            'resource_table_name': resource_type.resource_table_name,
            'resource_columns': ' '.join([
                f"{column.name} {column.datatype} {int(column.required)}"
                for column in resource_type.columns
            ])
        }

        # Storing the type information in the appropriate table
        self.db_connection.write_dict('abintern_resource_types', query_dict)

        # Creating a table appropriate for the resource_type
        self.db_connection.create_table(
            resource_type.resource_table_name,
            resource_type.columns
        )

        self.db_connection.commit()

    def check_resource_type_exists(self, resource_type: ResourceType) -> bool:
        """Check if ``resource_type`` exists."""

        db_response = self.db_connection.read(
            table_name='abintern_resource_types',
            headers=['resource_type_id', 'resource_name'],
            and_filters=[
                f"resource_type_id = '{resource_type.resource_type_id}'",
                f"resource_name = '{resource_type.resource_name}'"
            ]
        )
        return db_response

    ######################
    #   STATIC METHODS   #
    ######################

    @staticmethod
    def get_resource_type_from_str(
            resource_type_id: str,
            resource_name: str,
            resource_table_name: str,
            resource_columns: str
    ):
        """Create a ``ResourceType`` object from parameters."""

        resource_columns = resource_columns.split(' ')

        return ResourceType(
            resource_type_id=resource_type_id,
            resource_name=resource_name,
            resource_table_name=resource_table_name,
            columns=[
                Column(name, datatype, bool(int(required)))
                for name, datatype, required in [
                    resource_columns[i:i + 3] for i in range(0, len(resource_columns), 3)
                ]
            ]
        )

    #####################
    #  PRIVATE METHODS  #
    #####################

    def _init_resource_types_table(self):
        """Initialize the required table ``abintern_resource_types``."""

        if not self.db_connection.check_table_exists('abintern_resource_types'):
            columns = [
                Column('resource_type_id', 'VARCHAR', True),
                Column('resource_name', 'VARCHAR', True),
                Column('resource_table_name', 'VARCHAR', True),
                Column('resource_columns', 'VARCHAR', True)
            ]
            self.db_connection.create_table('abintern_resource_types', columns)
