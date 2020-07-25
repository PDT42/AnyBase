"""
:Author: PDT
:Since: 2020/07/21

This is the module for the plugin manager. It stores and loads available plugins
in and from the database.
"""

from typing import Any, List, Mapping, Optional, Sequence

from database import Column, DataTypes
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from exceptions.plugins import KeyConstraintException
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

        # Ensuring the table to the plugins in exists
        self._init_plugin_table()

        # Creating a query dict as required by write_dict
        query_dict = {
            'primary_key': plugin.plugin_id,
            'plugin_name': plugin.plugin_name,
            'plugin_macro_path': plugin.plugin_macro_path
        }

        # Storing the plugin in the database
        self.db_connection.write_dict(self._plugins_table_name, query_dict)
        self.db_connection.commit()

    def delete_plugin(self, plugin: Plugin):
        """Delete a plugin from the database. It will no longer be available to the user."""

        # Ensuring the table to the plugins in exists
        self._init_plugin_table()

        self.db_connection.delete(self._plugins_table_name, [f"primary_key = {plugin.plugin_id}"])
        self.db_connection.commit()

    def get_one(self, plugin_id: int) -> Optional[Plugin]:
        """Get one ``Plugin`` from the database."""

        # Ensuring the table to the plugins in exists
        self._init_plugin_table()

        result: Sequence[Mapping[str, Any]] = self.db_connection.read(
            table_name=self._plugins_table_name,
            headers=self._plugins_headers,
            and_filters=[f'primary_key = {plugin_id}']
        )

        if len(result) < 1:
            return None

        if len(result) > 1:
            raise KeyConstraintException(
                "There is a real big problem here! Real biggy - trust me." +
                "The primary key constraint is broken!"
            )

        plugin: Plugin = Plugin(
            plugin_name=result[0].get('plugin_name'),
            plugin_macro_path=result[0].get('plugin_macro_path'),
            plugin_id=result[0].get('primary_key')
        )
        return plugin

    def get_all(self) -> List[Plugin]:
        """Get all Plugins from the database."""

        # Ensuring the table to the plugins in exists
        self._init_plugin_table()

        result: Sequence[Mapping[str, Any]] = self.db_connection.read(
            table_name=self._plugins_table_name,
            headers=self._plugins_headers)

        plugins: List[Plugin] = []
        for row in result:
            plugins.append(Plugin(
                plugin_name=row.get('plugin_name'),
                plugin_macro_path=row.get('plugin_macro_path'),
                plugin_id=row.get('primary_key')
            ))
        return plugins

    def _init_plugin_table(self):
        """Initialize the plugins table."""

        plugin_columns: Sequence[Column] = [
            # The column primary_key, will be added automatically
            Column('plugin_name', 'plugin_name', DataTypes.VARCHAR.value, required=True),
            Column('plugin_macro_path', 'plugin_macro_path', DataTypes.VARCHAR.value, required=True)
        ]

        self.db_connection.create_table(self._plugins_table_name, plugin_columns)
        self.db_connection.commit()
