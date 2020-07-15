"""
:Author: PDT
:Since: 2020/07/01

These are tests for the SqliteConnection class.
"""

from shutil import rmtree
from unittest import TestCase

from database import Column, DataTypes
from test.test_util import init_test_db


class TestSqliteConnection(TestCase):

    def setUp(self) -> None:
        self.tempdir, self.db_connection = init_test_db()

        self.table_name = "test_table"
        self.db_columns = [
            Column("TextColumn", "TextColumn", DataTypes.VARCHAR.value, False),
            Column("NumberColumn", "NumberColumn", DataTypes.NUMBER.value, False)
        ]
        self.row_values = {"TextColumn": "TestText", "NumberColumn": 42}

    def tearDown(self) -> None:
        self.db_connection.kill()
        rmtree(self.tempdir)

    def test_read(self):
        # TODO: Add tests fpr filters, limit and offset
        self.db_connection.create_table(self.table_name, self.db_columns)
        self.assertTrue(self.db_connection.check_table_exists(self.table_name))
        self.db_connection.write_dict(self.table_name, self.row_values)
        self.assertEqual(1, self.db_connection.count(self.table_name))
        self.row_values["primary_key"] = 1
        self.assertEqual([self.row_values], self.db_connection.read(self.table_name, list(self.row_values.keys())))

    def test_delete(self):
        self.db_connection.create_table(self.table_name, self.db_columns)
        self.assertTrue(self.db_connection.check_table_exists(self.table_name))

        for iterator in range(0, 10):
            self.row_values["NumberColumn"] = iterator
            self.db_connection.write_dict(self.table_name, self.row_values)
        self.assertEqual(10, self.db_connection.count(self.table_name))
        self.db_connection.delete(self.table_name, [f"NumberColumn = 0"])
        self.assertEqual(9, self.db_connection.count(self.table_name))

    def test_write_dict(self):
        self.db_connection.create_table(self.table_name, self.db_columns)
        self.assertTrue(self.db_connection.check_table_exists(self.table_name))

        for iterator in range(0, 10):
            self.row_values["NumberColumn"] = iterator
            self.db_connection.write_dict(self.table_name, self.row_values)
        self.assertEqual(10, self.db_connection.count(self.table_name))

    def test_update(self):
        self.db_connection.create_table(self.table_name, self.db_columns)
        self.assertTrue(self.db_connection.check_table_exists(self.table_name))
        self.db_connection.write_dict(self.table_name, self.row_values)
        self.assertEqual(1, self.db_connection.count(self.table_name))
        self.row_values["primary_key"] = 1
        self.row_values["TextColumn"] = "Updated Text"
        self.db_connection.update(self.table_name, self.row_values)
        self.assertEqual([self.row_values], self.db_connection.read(self.table_name, list(self.row_values.keys())))

    def test_create_table(self):
        self.db_connection.create_table(self.table_name, self.db_columns)
        self.assertTrue(self.db_connection.check_table_exists(self.table_name))

    def test_delete_table(self):
        self.db_connection.create_table(self.table_name, self.db_columns)
        self.assertTrue(self.db_connection.check_table_exists(self.table_name))
        self.db_connection.delete_table(self.table_name)
        self.assertFalse(self.db_connection.check_table_exists(self.table_name))

    def test_get_table_info(self):
        self.db_connection.create_table(self.table_name, self.db_columns)
        self.assertTrue(self.db_connection.check_table_exists(self.table_name))
        self.assertEqual(
            [{'cid': 0, 'name': 'TextColumn', 'type': 'VARCHAR', 'notnull': 0, 'dflt_value': None, 'pk': 0},
             {'cid': 1, 'name': 'NumberColumn', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0},
             {'cid': 2, 'name': 'primary_key', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 1}],
            self.db_connection.get_table_info(self.table_name))

    def test_check_table_exists(self):
        self.db_connection.create_table(self.table_name, self.db_columns)
        self.assertTrue(self.db_connection.check_table_exists(self.table_name))

    def test_count(self):
        self.db_connection.create_table(self.table_name, self.db_columns)
        self.assertTrue(self.db_connection.check_table_exists(self.table_name))

        for iterator in range(0, 10):
            self.row_values["NumberColumn"] = iterator
            self.db_connection.write_dict(self.table_name, self.row_values)
        self.assertEqual(10, self.db_connection.count(self.table_name))
        self.db_connection.delete(self.table_name, [f"NumberColumn = 0"])
        self.assertEqual(9, self.db_connection.count(self.table_name))

    def test_update_table_name(self):
        self.db_connection.create_table(self.table_name, self.db_columns)
        self.assertTrue(self.db_connection.check_table_exists(self.table_name))
        self.db_connection.update_table_name(self.table_name, "UpdatedTableName")
        self.assertTrue(self.db_connection.check_table_exists("UpdatedTableName"))
        self.assertFalse(self.db_connection.check_table_exists(self.table_name))

    def test_update_table_columns(self):
        self.db_connection.create_table(self.table_name, self.db_columns)
        self.assertTrue(self.db_connection.check_table_exists(self.table_name))
        self.db_columns.append(Column("appended_column", "appended_column", DataTypes.VARCHAR.value, False))
        self.db_connection.update_table_columns(self.table_name, self.db_columns)
        self.assertEqual(
            [{'cid': 0, 'name': 'TextColumn', 'type': 'VARCHAR', 'notnull': 0, 'dflt_value': None, 'pk': 0},
             {'cid': 1, 'name': 'NumberColumn', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0},
             {'cid': 2, 'name': 'appended_column', 'type': 'VARCHAR', 'notnull': 0, 'dflt_value': None, 'pk': 0},
             {'cid': 3, 'name': 'primary_key', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 1}],
            (self.db_connection.get_table_info(self.table_name)))
