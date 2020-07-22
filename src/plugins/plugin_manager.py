"""
:Author: PDT
:Since: 2020/07/21

This is the module for the plugin manager. It stores and loads available plugins
in and from the database.
"""
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from plugins import Plugin


class PluginManager:
    """This is the ``PluginManager``."""

    def __init__(self):
        """Create a new ``PluginManager``."""

        self._plugins_table_name = 'abintern_plugins'
        self._plugins_headers = ['plugin_name', 'plugin_macro_path']

        self.db_connection: DbConnection = SqliteConnection.get()

    def store_plugin(self, plugin: Plugin):
        """Store a plugin in the database to make it available to the user."""
        pass

    def delete_plugin(self, plugin: Plugin):
        """Delete a plugin from the database. It will no longer be available to the user."""
        pass

    def get_one(self, plugin_id: int):
        """Get one ``Plugin`` from the database."""
        pass

    def get_all(self):
        """Get all Plugins from the database."""
        pass
