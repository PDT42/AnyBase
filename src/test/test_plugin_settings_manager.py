"""
:Author: PDT
:Since: 2020/07/25

These are tests for the PluginSettingsManager.
"""
from shutil import rmtree
from unittest import TestCase

from plugins import Plugin, PluginSettings
from plugins.plugin_manager import PluginManager
from plugins.plugin_settings_manager import PluginSettingsManager
from test.test_util import init_test_db


class TestPluginSettingsManager(TestCase):

    def setUp(self) -> None:
        self.tempdir, self.db_connection = init_test_db()
        # print(f"Tempdir used in this tests: {self.tempdir}")

        self.plugin_settings_manager: PluginSettingsManager = PluginSettingsManager()
        self.plugin_manager: PluginManager = PluginManager()

        self.plugin: Plugin = Plugin(
            plugin_name='TestPlugin',
            plugin_macro_path='test/path',
        )

        self.plugin_manager.store_plugin(plugin=self.plugin)
        self.plugin = self.plugin_manager.get_one(1)

        self.plugin_settings: PluginSettings = PluginSettings(
            plugin=self.plugin,
            employed_columns=['column1', 'column2']
        )

    def tearDown(self) -> None:
        self.db_connection.kill()
        rmtree(self.tempdir)

    def test_store_plugin_settings(self):
        self.plugin_settings_manager.store_plugin_settings(self.plugin_settings)
        self.plugin_settings.plugin_settings_id = 1
        self.assertEqual(self.plugin_settings, self.plugin_settings_manager.get_plugin_settings(1))

    def test_get_plugin_settings(self):
        self.plugin_settings_manager.store_plugin_settings(self.plugin_settings)
        self.plugin_settings.plugin_settings_id = 1
        self.assertEqual(self.plugin_settings, self.plugin_settings_manager.get_plugin_settings(1))


