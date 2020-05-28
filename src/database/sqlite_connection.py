"""
:Author: PDT
:Since: 2020/05/27

This is the implementation of DbConnection for Connections to sqlite databases.
"""
import sqlite3
from typing import Any, Mapping, Sequence

from src.config import Config
from src.database.db_connection import Column, DbConnection


class SqliteConnection(DbConnection):
    """This is a connection to an sqlite database."""

    _instance = None

    @staticmethod
    def get():
        """Get the instance of this singleton."""

        if not SqliteConnection._instance:
            SqliteConnection._instance = SqliteConnection()
        return SqliteConnection._instance

    def __init__(self):
        """Create a new SqliteConnection."""

        self.connection = None
        self.cursor = None

        self.db_path = Config.get().read('local database', 'path', 'res/database.db')

    @staticmethod
    def _dict_factory(cursor, row):
        result = {}
        for index, column in enumerate(cursor.description):
            result[column[0]] = row[index]
        return result

    def connect(self):
        """Connect to the database."""

        if self.connection:
            return

        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = SqliteConnection._dict_factory
        self.cursor = self.connection.cursor()

    def commit(self):
        """Commit Changes and close database connection."""

        if not self.connection:
            return
        self.connection.commit()
        self.connection.close()

    def read(
            self, table_name: str,
            headers: Sequence[str],
            and_filters: Sequence[str] = None,
            or_filters: Sequence[str] = None,
            offset: int = None,
            limit: int = None
    ) -> Sequence[Mapping[str, str]]:
        """Read from ``table``."""

        # Initialize connection
        self.connect()

        # Creating Query
        # --------------
        query = f"SELECT {', '.join(headers)} FROM {table_name}"

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

        if limit:
            query = f"{query} LIMIT {limit}"

        if offset:
            query = f"{query} OFFSET {offset}"
        # --------------
        self.cursor.execute(query)

        return self.cursor.fetchall()

    def write_dict(
            self, table_name: str,
            values: Mapping[str, Any]
    ):
        """Write ``values`` to ``table_name``."""

        # Initialize connection
        self.connect()

        # Get info on ``table_name`` from database
        table_info = self.get_table_info(table_name)

        # Creating Query
        # --------------
        query = f"INSERT INTO {table_name} VALUES ("

        for column in table_info:

            if column['name'] == 'primary_key':
                continue

            query = f'''{query} "{values[column['name']]}",'''
        query = f"{''.join(query[:-1])})"
        # --------------
        self.cursor.execute(query)

    def create_table(
            self, table_name: str,
            columns: Sequence[Column]
    ):
        """Create a table called ``table_name`` with ``columns`` in the database."""

        primary_key = False

        # Initialize connection
        self.connect()

        # Creating Query
        # --------------
        query = f"CREATE TABLE {table_name} ("

        for column in columns:

            # Adding columns
            query = f"{query}{column.name} {column.type}"

            if column.required:
                query = f"{query} NOT NULL"

            if column.primary_key and primary_key:
                raise Exception("There can't be more than one primary key.")

            if column.primary_key:
                primary_key = True
                query = f"{query} PRIMARY KEY"

            query = f"{query},"

        if not primary_key:
            query = f"{query} primary_key INTEGER PRIMARY KEY AUTOINCREMENT,"

        query = f"{''.join(query[:-1])})"
        # --------------
        self.cursor.execute(query)

    def get_table_info(self, table_name: str):
        """Get information on ``table_name``."""

        # Initialize connection
        self.connect()

        query = f"PRAGMA table_info('{table_name}')"

        self.cursor.execute(query)

        return sorted(self.cursor.fetchall(), key=lambda column: column['cid'])
