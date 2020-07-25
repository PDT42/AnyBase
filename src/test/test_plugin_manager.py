"""
:Author: PDT
:Since: 2020/07/25

These are tests for the plugin manager.
"""

from shutil import rmtree
from unittest import TestCase

from plugins import Plugin
from plugins.plugin_manager import PluginManager
from test.test_util import init_test_db


class TestPluginManager(TestCase):

    def setUp(self) -> None:
        self.tempdir, self.db_connection = init_test_db()
        print(f"Tempdir used in this tests: {self.tempdir}")

        self.plugin_manager: PluginManager = PluginManager()

        self.plugin = Plugin(
            plugin_name='TestPlugin',
            plugin_macro_path='test/path',
        )

    def tearDown(self) -> None:
        self.db_connection.kill()
        rmtree(self.tempdir)

    def test_store_plugin(self):
        self.plugin_manager.store_plugin(self.plugin)
        self.plugin.plugin_id = 1
        plugin = self.plugin_manager.get_one(1)
        self.assertEqual(self.plugin, plugin)

    def test_delete_plugin(self):
        self.plugin_manager.store_plugin(self.plugin)
        self.plugin.plugin_id = 1
        self.assertEqual(self.plugin, self.plugin_manager.get_one(1))
        self.plugin_manager.delete_plugin(self.plugin)
        self.assertEqual([], self.plugin_manager.get_all())

    def test_get_all(self):
        self.plugin_manager.store_plugin(self.plugin)
        self.plugin.plugin_id = 1
        self.assertEqual([self.plugin], self.plugin_manager.get_all())
        self.plugin_manager.delete_plugin(self.plugin)
        self.assertEqual([], self.plugin_manager.get_all())
