"""
:Author: PDT
:Since: 2020/05/27

This is the implementation of DbConnection for Connections to sqlite databases.
"""

import sqlite3
from datetime import datetime
from typing import Any
from typing import List
from typing import Mapping
from typing import MutableMapping
from typing import OrderedDict
from typing import Sequence
from typing import Tuple

from database import DataType
from database import DataTypes
from database.util import convert_asset_to_dbtype
from database.util import convert_assetlist_to_dbtype
from exceptions.common import IllegalStateException
from exceptions.common import MissingArgumentException
from exceptions.database import ColumnAlreadyExistsException
from exceptions.database import ColumnDoesNotExistException
from exceptions.database import DataTypeChangedException
from exceptions.database import MissingValueException
from exceptions.database import TableAlreadyExistsException
from exceptions.database import TableDoesNotExistException
from exceptions.database import UniqueConstraintError
from src.database.db_connection import Column
from src.database.db_connection import DbConnection


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

        # Making sure we use unique headers
        headers = set(headers)
        headers.add('primary_key')

        if not self.check_table_exists(table_name):
            raise TableDoesNotExistException("The table you supplied does not exist!")

        # Creating Query
        # --------------
        # TODO: This should be made injection proof
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
            self, table_headers: OrderedDict[str, Tuple[str, Sequence[str]]],
            and_filters: Sequence[str] = None,
            or_filters: Sequence[str] = None,
            offset: int = None,
            limit: int = None
    ):
        """Read from the database joining the table names in ``table_names``."""

        # Initialize connection
        self._connect()

        # Making sure the table we want to read from exists in the database
        if not all(self.check_table_exists(name) for name in table_headers.keys()):
            raise TableDoesNotExistException(
                "One of the table names you supplied was invalid!")

        # Making sure people don't get lazy
        if not len(table_headers) > 1:
            raise IllegalStateException(
                "You are trying to use a joined read, to read from only one table. " +
                "That is unnecessary however. Please use db_connection.read instead!")

        # Creating Query
        # --------------
        # TODO: This should be made injection proof
        query_headers: List[str] = []
        for table_name, (_, headers) in table_headers.items():
            query_headers += [f"{table_name}.{header}" for header in headers]

        query = f"SELECT {', '.join(query_headers)} FROM {' JOIN '.join(table_headers.keys())} WHERE "

        # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
        def generate_join_chain(theaders):

            for (tn, jo), tt in zip(
                    [(th, jo) for th, (jo, _) in theaders.items()],
                    list(theaders.keys())[1:]
            ):
                yield f"{tn}.{jo} = {tt}.primary_key"

        # ................................

        query = f"{query}{' AND '.join(list(generate_join_chain(table_headers)))}"

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

        # TODO: This should be made injection proof
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
        # TODO: This should be made injection proof
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
        try:
            self.cursor.execute(query)
        except sqlite3.IntegrityError:
            raise UniqueConstraintError()

        result: int = self.cursor.lastrowid

        return result

    def update(self, table_name: str, values: Mapping[str, Any]) -> int:
        """Update an entry in the database."""

        # Initialize connection
        self._connect()

        table_name = table_name.replace(' ', '_').lower()

        if not self.check_table_exists(table_name):
            raise TableDoesNotExistException(f"Table {table_name} does not exist!")

        # Get info on ``table_name`` from database
        table_info = self.get_table_info(table_name)

        # Creating Query
        # --------------
        # TODO: This should be made injection proof
        query = f"UPDATE {table_name} SET "

        for column_info in table_info:

            column_name = column_info['name']
            column_required = column_info['notnull']

            # We gotta cover some different cases
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            # 'column_name' is not provided on values. Do we need it?
            # Values for required columns must be present in 'values'
            if (column_name not in values.keys() or values[column_name] is None) and bool(column_required):
                raise MissingValueException(f"The required value {column_name} is missing. Please provide it!")

            # It's not there, but we don't need it - so we don't care
            elif (column_name not in values.keys() or values[column_name] is None) and not bool(column_required):
                query = f'''{query}{column_name} = null, '''

            # The most obvious other case: There are values for the column.
            elif column_name in values.keys():
                column_value = values[column_name]

                # Checking if the value we want to enter is a string
                # Strings are special -> They need an extra sausage
                if isinstance(column_value, str):
                    if column_required and not column_value:
                        MissingValueException("Required fields of type VARCHAR cannot contain an empty string!")
                    query = f'''{query}{column_name} = "{column_value}", '''
                else:
                    query = f'''{query}{column_name} = {column_value}, '''

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        query = f"{''.join(query[:-2])} "

        query += f"WHERE primary_key = {values['primary_key']}"
        # --------------
        self.cursor.execute(query)

        result: int = self.cursor.lastrowid

        return result

    def update_table_name(self, table_name: str, new_table_name: str):
        """Update the name of a table in the database."""

        # Initialize connection
        self._connect()

        table_name = table_name.replace(' ', '_').lower()
        new_table_name = new_table_name.replace(' ', '_').lower()

        if not self.check_table_exists(table_name):
            raise TableDoesNotExistException(f"Table {table_name} does not exist!")

        if self.check_table_exists(new_table_name):
            raise TableAlreadyExistsException(f"Table {new_table_name} does already exist!")

        # TODO: This should be made injection proof
        query = f"ALTER TABLE {table_name} RENAME TO {new_table_name}"
        self.cursor.execute(query)

    def update_columns(self, table_name: str, update_columns: Mapping[str, Column]):
        """Update columns of the database table ``table_name``. The columns
        with the ``db_names`` used as keys in ``update_columns`` will be updated
        to the respective value in ``update_columns``. """

        # Initialize connection
        self._connect()

        table_name = table_name.replace(' ', '_').lower()

        # Making sure table exists
        if not self.check_table_exists(table_name):
            raise TableDoesNotExistException(f"Table {table_name} does not exist!")

        # Get info on ``table_name`` from database
        table_info = self.get_table_info(table_name)

        # TODO: This whole method feels clumsy
        # TODO: Musta done it while high

        # Creating a mapping for column renames

        db_columns: MutableMapping[str, Column] = {
            column['name']: Column(
                column['name'], column['name'],
                DataTypes[column['type']].value,
                required=bool(column['notnull'])
            ) for column in table_info
            if column['name'] != 'primary_key'
        }

        for old_name, update_column in update_columns.items():

            if old_name not in db_columns.keys():
                raise ColumnDoesNotExistException(
                    f"The column {old_name}, you just tried " +
                    f"to update does not exist in {table_name}!")

            if update_column.datatype is not db_columns[old_name].datatype:
                if self.count(table_name) > 0:
                    raise DataTypeChangedException(
                        "Can't update the column datatype of a none empty table!"
                    )
            db_columns[old_name] = update_column

        # Creating a temp table for the transition
        temp_table_name: str = f"temp_{table_name}"
        temp_table_columns: List[Column] = []

        # TODO: This could be done way cleaner
        old_column_names: List[str] = []
        new_column_names: List[str] = []

        for old_name, column in db_columns.items():
            old_column_names.append(old_name)
            new_column_names.append(column.db_name)
            temp_table_columns.append(column)
        self.create_table(temp_table_name, temp_table_columns)

        old_column_names.append('primary_key')
        new_column_names.append('primary_key')

        # TODO: This should be made injection proof
        query = f"INSERT INTO {temp_table_name}({', '.join(new_column_names)}) " + \
                f"SELECT {', '.join(old_column_names)} FROM {table_name}"
        self.cursor.execute(query)

        # Finally deleting the old table and
        # renaming the temp table to it's now
        # free table id.
        self.delete_table(table_name)
        self.update_table_name(temp_table_name, table_name)

    def update_append_column(self, table_name: str, append_column: Column):
        """Append ``append_column`` to db table named ``table_name``."""

        # Initialize connection
        self._connect()

        table_name = table_name.replace(' ', '_').lower()

        # Making sure table exists
        if not self.check_table_exists(table_name):
            raise TableDoesNotExistException(f"Table {table_name} does not exist!")

        # Get info on ``table_name`` from database
        table_info = self.get_table_info(table_name)
        db_column_names = [column['name'] for column in table_info]

        # Making sure a column with the same name does
        # not already exist for this database table
        if append_column.db_name in db_column_names:
            raise ColumnAlreadyExistsException(
                f"A column named {append_column.db_name} does already exist in {table_name}!")

        # Columns we append to a table must not
        # be required. We got no value for em!
        append_column.required = False

        # Creating a temp table for the transition
        temp_table_name: str = f"temp_{table_name}"
        temp_table_columns: List[Column] = [append_column] + [
            Column(col['name'], col['name'], DataTypes[col['type']].value, required=bool(col['notnull']))
            for col in table_info if col['name'] != 'primary_key']
        self.create_table(temp_table_name, temp_table_columns)

        query = f"INSERT INTO {temp_table_name}({', '.join(db_column_names)}) " + \
                f"SELECT {', '.join(db_column_names)} FROM {table_name}"
        self.cursor.execute(query)

        self.delete_table(table_name)
        self.update_table_name(temp_table_name, table_name)

    def update_remove_column(self, table_name: str, remove_column: Column):
        """Remove column ``remove_column`` from db table named ``table_name``."""

        # Initialize connection
        self._connect()

        table_name = table_name.replace(' ', '_').lower()
        # Making sure table exists
        if not self.check_table_exists(table_name):
            raise TableDoesNotExistException(f"Table {table_name} does not exist!")

        # Get info on ``table_name`` from database
        table_info = self.get_table_info(table_name)
        db_column_names = [column['name'] for column in table_info]

        # Making sure a column with the name does
        # exist in  this database table
        if remove_column.db_name not in db_column_names:
            raise ColumnDoesNotExistException(
                f"A column named {remove_column.db_name} does not exist in {table_name}!")

        # Creating a temp table for the transition
        temp_table_name: str = f"temp_{table_name}"
        temp_table_columns: List[Column] = []
        temp_table_column_names: List[str] = []

        for col in table_info:

            if col['name'] == remove_column.db_name:
                continue

            if col['name'] == 'primary_key':
                temp_table_column_names.append(col['name'])
                continue

            temp_table_column_names.append(col['name'])
            temp_table_columns.append(Column(
                col['name'], col['name'],
                DataTypes[col['type']].value,
                required=bool(col['notnull'])
            ))

        self.create_table(temp_table_name, temp_table_columns)

        query = f"INSERT INTO {temp_table_name}({', '.join(temp_table_column_names)}) " + \
                f"SELECT {', '.join(temp_table_column_names)} FROM {table_name}"
        self.cursor.execute(query)

        self.delete_table(table_name)
        self.update_table_name(temp_table_name, table_name)

    def create_table(
            self, table_name: str,
            columns: Sequence[Column]
    ):
        """Create a table called ``table_name`` with ``field_mappings`` in the database."""

        primary_key = False

        # TODO: Make sure to ignore spaces in column names
        table_name = table_name.replace(' ', '_').lower()

        # Initialize connection
        self._connect()

        # Creating Query
        # --------------
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ("

        for column in columns:

            # Adding field_mappings
            query = f"{query}{column.db_name} {column.datatype.db_type}"

            if column.unique:
                query = f"{query} UNIQUE"

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

        table_name = table_name.replace(' ', '_').lower()

        query = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(query)

    def get_table_info(self, table_name: str):
        """Get information on ``table_name``."""

        # Initialize connection
        self._connect()

        table_name = table_name.replace(' ', '_').lower()

        query = f"PRAGMA table_info('{table_name}')"
        self.cursor.execute(query)

        result = sorted(self.cursor.fetchall(), key=lambda column: column['cid'])
        return result

    def check_table_exists(self, table_name) -> bool:
        """Check if a table ``table_name`` already exists in the database"""

        # Initialize connection
        self._connect()

        table_name = table_name.replace(' ', '_').lower()

        query = f"SELECT COUNT(*) as 'exists' FROM sqlite_master " + \
                f"WHERE type='table' AND name='{table_name}'"
        self.cursor.execute(query)

        result = bool(self.cursor.fetchall()[0]['exists'])
        return result

    def count(self, table_name: str, query_filters: List[str] = None) -> int:
        """Count the number of items in ``table_name``."""

        # Initialize connection
        self._connect()

        table_name = table_name.replace(' ', '_').lower()

        query = f"SELECT COUNT(*) FROM {table_name}"

        if query_filters:
            query = f"{query} WHERE {' AND '.join(query_filters)}"

        self.cursor.execute(query)
        result = self.cursor.fetchall()[0]['COUNT(*)']
        return result
