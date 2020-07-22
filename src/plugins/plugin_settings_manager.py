"""
:Author: PDT
:Since: 2020/07/19

This is the plugin settings manager. As the name suggests it is the connection between the
backend and the database and provides all required functionalities for interacting plugin
settings stored in the database.
"""

from typing import Any, Mapping, Sequence

from database import Column, DataTypes
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from plugins import PluginSettings
from plugins.plugin_manager import PluginManager


class PluginSettingsManager:
    """This is the ``PluginSettingsManager``."""

    def __init__(self):
        """Create a new ``PluginSettingsManager``."""

        self._plugin_settings_headers = ['plugin', 'employed_columns']
        self._plugin_settings_table_name = 'abintern_plugin_settings'

        self.plugin_manager = PluginManager()

        self.db_connection: DbConnection = SqliteConnection.get()

    def store_plugin_settings(self, plugin_settings: PluginSettings):
        """Store plugin settings in the database."""

        # Ensuring the table to store the plugin settings in exists
        self._init_plugin_settings_table()

    def get_plugin_settings(self, plugin_settings_id: int):
        """Get ``PluginSettings`` from the database."""

        result: Sequence[Mapping[str, Any]] = self.db_connection.read(
            table_name=self._plugin_settings_table_name,
            headers=self._plugin_settings_headers,
            and_filters=[f'primary_key = {plugin_settings_id}']
        )

        if len(result) < 1:
            return None

        plugin_settings = PluginSettings(

        )

    def _generate_employed_columns_string(self, columns: Sequence[Column]):
        """Generate a string to use in 'employed_columns'."""
        pass

    def _init_plugin_settings_table(self):
        """Initialize the plugins settings table."""

        plugin_settings_columns: Sequence[Column] = [
            # The column 'primary_key' will be created automatically
            Column('plugin', 'plugin', DataTypes.INTEGER.value, required=True),
            Column('employed_columns', 'employed_columns', DataTypes.VARCHAR.value, required=True)
        ]

        self.db_connection.create_table(self._plugin_settings_table_name, plugin_settings_columns)
