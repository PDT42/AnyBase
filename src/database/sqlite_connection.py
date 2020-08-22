"""
:Author: PDT
:Since: 2020/05/27

This is the implementation of DbConnection for Connections to sqlite databases.
"""
import sqlite3
from datetime import datetime
from typing import Any, List, Mapping, Sequence

from database import DataType, DataTypes
from database.util import convert_asset_to_dbtype, convert_assetlist_to_dbtype
from exceptions.common import IllegalStateException, InvalidArgumentError, MissingArgumentException
from exceptions.database import MissingValueException, TableAlreadyExistsException
from exceptions.database import TableDoesNotExistException
from src.database.db_connection import Column, DbConnection


class SqliteConnection(DbConnection):
    """This is a connection to an sqlite database."""

    _instance = None

    _conversions: Mapping[DataType, callable] = {
        DataTypes.TEXT.value: str,
        DataTypes.NUMBER.value: float,
        DataTypes.INTEGER.value: int,
        DataTypes.BOOLEAN.value: int,
        DataTypes.DATETIME.value: lambda dt: int(dt.timestamp()),
        DataTypes.DATE.value: lambda d: int(datetime.combine(d, datetime.min.time()).timestamp()),
        DataTypes.ASSET.value: convert_asset_to_dbtype,
        DataTypes.ASSETLIST.value: convert_assetlist_to_dbtype
    }

    @staticmethod
    def get(db_path: str = None):
        """Get the instance of this singleton."""

        if not SqliteConnection._instance:
            if not db_path:
                raise MissingArgumentException("Db Path is required on initialization!")
            SqliteConnection._instance = SqliteConnection(db_path)
        return SqliteConnection._instance

    def __init__(self, db_path):
        """Create a new SqliteConnection."""

        if SqliteConnection._instance:
            raise IllegalStateException(
                "This singleton already exists. Use SqliteConnection.get() to get the instance!")

        self.db_path = db_path

        self.connection = None
        self.cursor = None

        self._connect()

    @staticmethod
    def _dict_factory(cursor, row):
        result = {}
        for index, column in enumerate(cursor.description):
            result[column[0]] = row[index]
        return result

    @staticmethod
    def initialize(db_path: str):
        """Initialize a sqlite connection using a custom path. This is mainly
        for testing purposes. For deployment its advised to set the database
        path in the config."""

        if not SqliteConnection._instance:
            SqliteConnection._instance = SqliteConnection(db_path=db_path)
        else:
            raise IllegalStateException("This singleton already exists, can't change the db path during runtime.")
        return SqliteConnection._instance

    def _connect(self):
        """Connect to the database."""

        if self.connection:
            return

        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = SqliteConnection._dict_factory
        self.cursor = self.connection.cursor()

    ##########################
    # Connection Interaction #
    ##########################

    def commit(self):
        """Commit Changes."""

        if not self.connection:
            return
        self.connection.commit()

    def reset(self):
        """Reset connection."""

        if not self.connection:
            return
        self.connection.close()
        self.connection = None
        self._connect()

    def close(self):
        """Commit changes and close the database connection."""

        if not self.connection:
            return
        self.connection.commit()
        self.connection.close()

    def kill(self):
        """Close the connection and kill the singleton."""
        if self.connection:
            self.connection.close()
        SqliteConnection._instance = None

    ########################
    # Database Interaction #
    ########################

    def read(
            self, table_name: str,
            headers: Sequence[str],
            and_filters: Sequence[str] = None,
            or_filters: Sequence[str] = None,
            offset: int = None,
            limit: int = None
    ) -> Sequence[Mapping[str, Any]]:
        """Read headers_sequence from database ``table`` called ``table_name``.

        This will read all ``headers_sequence`` from ``table_name`` adding the
        ``and_filters`` and the ``or_filters`` to the query it runs on the
        database and using ``offset`` and ``limit`` in the way the names
        suggest."""

        # Initialize connection
        self._connect()

        headers = set(headers)
        headers.add('primary_key')

        if not self.check_table_exists(table_name):
            raise TableDoesNotExistException("The table you supplied does not exist!")

        # Creating Query
        # --------------
        query = f"SELECT {', '.join(headers)} FROM {table_name.replace(' ', '_')}"

        # Adding Filters
        if and_filters or or_filters:
            query = f"{query} WHERE "

        if and_filters:
            query = f"{query}{' AND '.join(and_filters)}"

        if or_filters:

            if and_filters:
                query = f"{query} AND ("

            query = f"{query}{' OR '.join(or_filters)}"

            if and_filters:
                query = f"{query})"

        # Adding Limit
        if limit:
            query = f"{query} LIMIT {limit}"

        # Adding Offset
        if offset:
            query = f"{query} OFFSET {offset}"
        # --------------
        self.cursor.execute(query)

        result = self.cursor.fetchall()

        return result

    def read_joined(
            self, table_names: List[str],
            join_on_chain: List[str],
            headers_sequence: Sequence[Sequence[str]],
            and_filters: Sequence[str] = None,
            or_filters: Sequence[str] = None,
            offset: int = None,
            limit: int = None
    ):
        """Read from the database joining the table names in ``table_names``."""

        # Initialize connection
        self._connect()

        headers_sequence = [set(hs) for hs in list(headers_sequence)]

        if not len(headers_sequence) == len(table_names):
            raise InvalidArgumentError("Number of headers_sequence and tables does not match!")

        # Making sure the table we want to read from exists in the database
        if not all(self.check_table_exists(name) for name in table_names):
            raise TableDoesNotExistException(
                "One of the table names you supplied was invalid!")

        # Making sure people don't get lazy
        if not len(table_names) > 1:
            raise IllegalStateException(
                "You are trying to use a joined read, to read from only one table. " +
                "That is unnecessary however. Please use db_connection.read instead!")

        # Creating Query
        # --------------
        query_headers: List[str] = []
        for index, headers in enumerate(headers_sequence):
            query_headers += [f"{table_names[index]}.{header}" for header in headers]

        query = f"SELECT {', '.join(query_headers)} FROM {' JOIN '.join(table_names)} WHERE "

        for iteration, (table_name, join_on) in enumerate(zip(table_names, join_on_chain)):
            if (iteration + 1) is len(table_names):
                break
            query += f"{table_name}.{join_on} = {table_names[iteration + 1]}.primary_key"
            query += " AND " if (iteration + 2) < len(table_names) else ""

        if and_filters:
            query = f"{query} AND {' AND '.join(and_filters)}"

        if or_filters:
            query = f"{query} AND ({' OR '.join(or_filters)})"

        # Adding Limit
        if limit:
            query = f"{query} LIMIT {limit}"

        # Adding Offset
        if offset:
            query = f"{query} OFFSET {offset}"
        # --------------
        self.cursor.execute(query)

        result = self.cursor.fetchall()

        return result

    def delete(self, table_name: str, and_filters: Sequence[str]):
        """Delete from ``table_name`` where filters apply."""

        # Initialize connection
        self._connect()

        query = f"DELETE FROM {table_name} WHERE {' AND '.join(and_filters)}"

        self.cursor.execute(query)

    def write_dict(
            self, table_name: str,
            values: Mapping[str, Any]
    ) -> int:
        """Write ``values`` to ``table_name``."""

        # Initialize connection
        self._connect()

        if not self.check_table_exists(table_name):
            raise TableDoesNotExistException(f"Table {table_name} does not exist!")

        # Get info on ``table_name`` from database
        table_name = table_name.replace(' ', '_')
        table_info = self.get_table_info(table_name)

        # Creating Query
        # --------------
        query = f"INSERT INTO {table_name} VALUES ("

        for column_info in table_info:

            column_name = column_info['name']
            column_required = column_info['notnull']

            # We gotta cover some different cases
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            # We don't WRITE pks - pks are assigned by the db
            if column_name == 'primary_key':
                query = f'''{query}null, '''
                continue

            # 'column_name' is not provided on values. Do we need it?
            # Values for required columns must be present in 'values'
            if (column_name not in values.keys() or values[column_name] is None) and bool(column_required):
                raise MissingValueException(f"The required value {column_name} is missing. Please provide it!")

            # It's not there, but we don't need it - so we don't care
            elif (column_name not in values.keys() or values[column_name] is None) and not bool(column_required):
                query = f'''{query}null, '''

            # The most obvious other case: There are values for the column.
            elif column_name in values.keys():
                column_value = values[column_name]

                # Checking if the value we want to enter is a string
                # Strings are special -> They need an extra sausage
                if isinstance(column_value, str):
                    if column_required and not column_value:
                        MissingValueException("Required fields of type VARCHAR cannot contain an empty string!")
                    query = f'''{query}"{column_value}", '''
                else:
                    query = f'''{query}{column_value}, '''

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Removing the ', '.join artifacts
        query = f"{''.join(query[:-2])})"
        # --------------
        self.cursor.execute(query)

        result: int = self.cursor.lastrowid

        return result

    def update(self, table_name: str, values: Mapping[str, Any]) -> int:
        """Update an entry in the database."""

        # Initialize connection
        self._connect()

        table_name = table_name.replace(' ', '_')

        if not self.check_table_exists(table_name):
            raise TableDoesNotExistException(f"Table {table_name} does not exist!")

        # Get info on ``table_name`` from database
        table_info = self.get_table_info(table_name)

        # Creating Query
        # --------------
        query = f"UPDATE {table_name} SET "

        for column_info in table_info:

            column_name = column_info['name']

            if column_name == 'primary_key':
                continue

            # If its not supplied, we don't
            # want to update it
            if column_name not in values.keys():
                continue

            if isinstance(values[column_name], str):
                query += f'{column_name} = "{values[column_name]}", '
            elif isinstance(values[column_name], datetime):
                timestamp = int(values[column_name].timestamp())
                query += f'''{query}"{timestamp}", '''
            else:
                query += f'{column_name} = {values[column_name]}, '

        query = f"{''.join(query[:-2])} "

        query += f"WHERE primary_key = {values['primary_key']}"
        # --------------
        result = self.cursor.execute(query)

        return result

    def update_table_name(self, table_name: str, new_table_name: str):
        """Update the name of a table in the database."""

        # Initialize connection
        self._connect()

        table_name = table_name.replace(' ', '_')

        if not self.check_table_exists(table_name):
            raise TableDoesNotExistException(f"Table {table_name} does not exist!")

        if self.check_table_exists(new_table_name):
            raise TableAlreadyExistsException(f"Table {new_table_name} does already exist!")

        query = f"ALTER TABLE {table_name} RENAME TO {new_table_name}"
        self.cursor.execute(query)

    def update_table_columns(self, table_name: str, columns: Sequence[Column]):
        """Update the columns of a table in the database."""

        # Initialize connection
        self._connect()

        table_name = table_name.replace(' ', '_')

        # Making sure table exists
        if not self.check_table_exists(table_name):
            raise TableDoesNotExistException(f"Table {table_name} does not exist!")

        # Get info on ``table_name`` from database
        table_info = self.get_table_info(table_name)

        # Making sure any columns we create have required = False
        remote_columns = [column['name'] for column in table_info]
        for column in columns:
            if column.db_name not in remote_columns:
                column.required = False

        temp_table_name = f"temp_{table_name}"

        self.create_table(temp_table_name, columns)

        column_str = ', '.join([column.db_name for column in columns[:len(remote_columns) - 1]]) + ', primary_key'
        query = f"INSERT INTO {temp_table_name}({column_str}) SELECT {', '.join(remote_columns)} FROM {table_name}"
        self.cursor.execute(query)

        self.delete_table(table_name)
        self.update_table_name(temp_table_name, table_name)

    def create_table(
            self, table_name: str,
            columns: Sequence[Column]
    ):
        """Create a table called ``table_name`` with ``employed_columns`` in the database."""

        primary_key = False

        # TODO: Make sure to ignore spaces in column names

        # Initialize connection
        self._connect()

        # Creating Query
        # --------------
        query = f"CREATE TABLE IF NOT EXISTS {table_name.replace(' ', '_')} ("

        for column in columns:

            # Adding employed_columns
            query = f"{query}{column.db_name} {column.datatype.db_type}"

            if column.required:
                query = f"{query} NOT NULL"

            query = f"{query},"

        if not primary_key:
            query = f"{query} primary_key INTEGER PRIMARY KEY AUTOINCREMENT,"

        query = f"{''.join(query[:-1])})"
        # --------------

        self.cursor.execute(query)

    def delete_table(self, table_name: str):
        """Delete a table from the database."""

        # Initialize connection
        self._connect()

        query = f"DROP TABLE {table_name.replace(' ', '_')}"

        # If a table doesn't exist, we can't delete it
        try:
            self.cursor.execute(query)
        except sqlite3.OperationalError:
            pass

    def get_table_info(self, table_name: str):
        """Get information on ``table_name``."""

        # Initialize connection
        self._connect()

        query = f"PRAGMA table_info('{table_name.replace(' ', '_')}')"
        self.cursor.execute(query)

        result = sorted(self.cursor.fetchall(), key=lambda column: column['cid'])
        return result

    def check_table_exists(self, table_name) -> bool:
        """Check if a table ``table_name`` already exists in the database"""

        # Initialize connection
        self._connect()

        query = f"SELECT COUNT(*) as 'exists' FROM sqlite_master WHERE type='table' AND name='{table_name.replace(' ', '_')}'"
        self.cursor.execute(query)

        result = bool(self.cursor.fetchall()[0]['exists'])
        return result

    def count(self, table_name: str) -> int:
        """Count the number of items in ``table_name``."""

        # Initialize connection
        self._connect()

        query = f"SELECT COUNT(*) FROM {table_name.replace(' ', '_')}"
        self.cursor.execute(query)

        result = self.cursor.fetchall()[0]['COUNT(*)']
        return result
