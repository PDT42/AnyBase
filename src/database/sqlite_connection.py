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

        self.connect()

        query = f"SELECT {', '.join('headers')} FROM {table_name}"

        self.cursor.execute(query)

        return self.cursor.fetchall()

    def write_dict(
            self, table_name: str,
            values: Mapping[str, Any]
    ):
        """TODO"""

        # TODO: implement update

        self.connect()

        table_info = self.get_table_info(table_name)

        query = f"INSERT INTO {table_name} VALUES ("

        for column in table_info:

            if column['name'] == 'primary_key':
                continue

            query = f'''{query} "{values[column['name']]}",'''
        query = f"{''.join(query[:-1])})"

        self.cursor.execute(query)

    def create_table(
            self, table_name: str,
            columns: Sequence[Column]
    ):
        """Create a table called ``table_name`` with ``columns`` in the database"""

        self.connect()

        primary_key = False

        query = f"CREATE TABLE {table_name} ("

        for column in columns:

            query = f"{query}{column.name} {column.type}"

            if column.required:
                query = f"{query} NOT NULL"

            if column.primary_key:
                primary_key = True
                query = f"{query} PRIMARY KEY"

            query = f"{query},"

        if not primary_key:
            query = f"{query} primary_key INTEGER PRIMARY KEY AUTOINCREMENT,"

        query = f"{''.join(query[:-1])})"

        self.cursor.execute(query)

    def get_table_info(self, table_name: str):
        """Get information on ``table_name``."""

        self.connect()

        query = f"PRAGMA table_info('{table_name}')"

        self.cursor.execute(query)

        return sorted(self.cursor.fetchall(), key=lambda column: column['cid'])
