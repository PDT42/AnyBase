"""
:Author: PDT
:Since: 2020/07/19

This is the plugin manager. As the name suggests it is the connection between the backend
and the database and provides all required functionalities for interacting plugin settings
stored in the database.
"""
from typing import Sequence

from database import Column
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from plugins import PluginSettings


class PluginManager:
    """This is the ``PluginManager``."""

    def __init__(self):
        """Create a new ``PluginManager``."""

        self._plugin_headers = []
        self._plugin_table_name = 'abintern_plugin_settings'

        self.db_connection: DbConnection = SqliteConnection.get()

    def store_plugin_settings(self, plugin_settings: PluginSettings):
        """Store plugin settings in the database."""

        # Ensuring the table to store the plugin settings in exists
        self._init_plugin_settings_table()

    def _init_plugin_settings_table(self):
        """Initialize the plugins settings table."""

        plugin_settings_columns: Sequence[Column] = [
            Column(),
        ]

        self.db_connection.create_table(self._plugin_table_name)