"""
:Author: PDT
:Since: 2020/08/26

This is a command line interface for the sqlite connection.
"""

from argparse import ArgumentParser
from typing import Any
from typing import Iterable

from config import Config
from database.sqlite_connection import SqliteConnection
from exceptions.common import MissingArgumentException


class SqliteExecutor(SqliteConnection):
    """This is a special implementation of an sqlite connection.
    It implements a function that can execute queries on the
    database directly. A functionality, I don't want the regular
    connection to supply."""

    @staticmethod
    def get(db_path: str = None):
        """Get the instance of this singleton."""

        if not SqliteExecutor._instance:
            if not db_path:
                raise MissingArgumentException("Db Path is required on initialization!")
            SqliteExecutor._instance = SqliteExecutor(db_path)
        return SqliteExecutor._instance

    def execute_query(self, sqlite_query: str):
        """Directly execute ``sqlite_query`` on the database."""

        # Initialize connection
        self._connect()

        self.cursor.execute(sqlite_query)
        res = self.cursor.fetchall()
        return res


# DEFINING AN ARGUMENT PARSER
# °°°°°°°°°°°°°°°°°°°°°°°°°°°
arg_parser: ArgumentParser = ArgumentParser(
    description="This is the argument parser for the AnyBase Sqlite CLI.")

arg_parser.add_argument('command', type=str, help="The command you want to execute ...")
arg_parser.add_argument('--query', type=str, help="Query parameter, if required ...")

if __name__ == '__main__':

    Config.get().change_path('U:/projects/anybase_modular_management/res/config.ini')

    database_path = Config.get().read('local database', 'path')
    sqlite_con: SqliteExecutor = SqliteExecutor.get(database_path)

    arguments: dict = vars(arg_parser.parse_args())


    def execute_query():

        if not (query := arguments.get('query', None)) or query in ['', ' ']:
            return 'Error: No Query supplied ...'

        print(f"Executing query: '{query}'\n")
        return sqlite_con.execute_query(query)


    def reset_layouts():
        sqlite_con.delete_table('abintern_layout')
        sqlite_con.delete_table('abintern_plugins')
        return 0


    def delete_basic_notes_notes():
        get_tables_query: str = \
            "SELECT name FROM sqlite_master " \
            "WHERE type='table' " \
            "AND name LIKE 'abasset_table_basic_notes_%'"
        plugin_table_names = sqlite_con.execute_query(get_tables_query)

        for name in [row['name'] for row in plugin_table_names]:
            sqlite_con.delete_table(name)
        return 0

    # This implements an action switch

    result: Any = {
        'exec': execute_query(),
        'reset_layouts': reset_layouts(),
        'reset_basic_notes': delete_basic_notes_notes()
    }.get(arguments.get('command'), 'Error: Invalid Command ...')

    join_on = '\n'

    if result != 'Error: Invalid Command ...':
        print("Result:")
        print("=======")
        if isinstance(result, Iterable):
            print(f"[{join_on.join([str(r) for r in result])}]")
        else:
            print(result)
    else:
        print(result)
