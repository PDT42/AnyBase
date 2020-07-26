"""
:Author: PDT
:Since: 2020/07/19

This is the plugin settings manager. As the name suggests it is the connection between the
backend and the database and provides all required functionalities for interacting plugin
settings stored in the database.
"""

from typing import Any, Mapping, Optional, Sequence

from database import Column, DataTypes
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from exceptions.common import KeyConstraintException
from plugins import PluginSettings
from plugins.plugin_manager import PluginManager


class PluginSettingsManager:
    """This is the ``PluginSettingsManager``."""

    def __init__(self):
        """Create a new ``PluginSettingsManager``."""

        self._plugin_settings_headers = ['plugin_id', 'employed_columns']
        self._plugin_settings_table_name = 'abintern_plugin_settings'

        self.plugin_manager = PluginManager()

        self.db_connection: DbConnection = SqliteConnection.get()

    def store_plugin_settings(self, plugin_settings: PluginSettings):
        """Store plugin settings in the database."""

        # Ensuring the table to store the plugin settings in exists
        self._init_plugin_settings_table()

        # Creating a query dict as required by write_dict
        query_dict = {
            'primary_key': plugin_settings.plugin_settings_id,
            'plugin_id': plugin_settings.plugin.plugin_id,
            'employed_columns': ";".join(plugin_settings.employed_columns)
        }

        # Storing the plugin settings in the appropriate table
        self.db_connection.write_dict(self._plugin_settings_table_name, query_dict)
        self.db_connection.commit()

    def get_plugin_settings(self, plugin_settings_id: int) -> Optional[PluginSettings]:
        """Get ``PluginSettings`` from the database."""

        result: Sequence[Mapping[str, Any]] = self.db_connection.read(
            table_name=self._plugin_settings_table_name,
            headers=self._plugin_settings_headers,
            and_filters=[f'primary_key = {plugin_settings_id}']
        )

        if len(result) < 1:
            return None

        if len(result) > 1:
            raise KeyConstraintException(
                "There is a real big problem here! Real biggy - trust me." +
                "The primary key constraint is broken!"
            )

        plugin_settings: PluginSettings = PluginSettings(
            plugin=self.plugin_manager.get_one(result[0]['primary_key']),
            employed_columns=result[0].get('employed_columns').split(';'),
            plugin_settings_id=result[0].get('primary_key')
        )
        return plugin_settings

    def _init_plugin_settings_table(self):
        """Initialize the plugins settings table."""

        plugin_settings_columns: Sequence[Column] = [
            # The column 'primary_key' will be created automatically
            Column('plugin_id', 'plugin_id', DataTypes.INTEGER.value, required=True),
            Column('employed_columns', 'employed_columns', DataTypes.VARCHAR.value, required=True)
        ]

        self.db_connection.create_table(self._plugin_settings_table_name, plugin_settings_columns)
        self.db_connection.commit()
