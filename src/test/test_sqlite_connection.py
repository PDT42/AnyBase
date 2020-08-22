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
        # print(f"Tempdir used in this tests: {self.tempdir}")

        self.table_name = "test_table"
        self.db_columns = [
            Column("TextColumn", "textcolumn", DataTypes.VARCHAR.value),
            Column("NumberColumn", "numbercolumn", DataTypes.NUMBER.value)
        ]
        self.row_values = {"textcolumn": "testtext", "numbercolumn": 42}

    def tearDown(self) -> None:
        self.db_connection.kill()
        rmtree(self.tempdir)

    def test_read(self):
        # TODO: Add tests for filters, limit and offset
        self.db_connection.create_table(self.table_name, self.db_columns)
        self.assertTrue(self.db_connection.check_table_exists(self.table_name))
        self.db_connection.write_dict(self.table_name, self.row_values)
        self.assertEqual(1, self.db_connection.count(self.table_name))
        self.row_values["primary_key"] = 1
        self.assertEqual([self.row_values], self.db_connection.read(self.table_name, list(self.row_values.keys())))

    def test_read_joined(self):
        # Create an average Person
        person_table_name: str = 'abasset_table_person'
        self.db_connection.create_table(
            table_name=person_table_name,
            columns=[
                # Varchar and Text can be used interchangeably
                Column('name', 'name', DataTypes.TEXT.value, required=True),
                Column('age', 'age', DataTypes.INTEGER.value, required=True),
                Column('city_of_birth', 'city_of_birth', DataTypes.VARCHAR.value, required=True),
                Column('extended_by_id', 'extended_by_id', DataTypes.INTEGER.value, required=True)
            ]
        )

        # Each student is a person, but unlike other
        # people a student has a subject of study.
        student_table_name: str = 'abasset_table_student'
        self.db_connection.create_table(
            table_name=student_table_name,
            columns=[
                Column('subject', 'subject_of_study', DataTypes.VARCHAR.value, required=True),
                Column('extended_by_id', 'extended_by_id', DataTypes.INTEGER.value, required=True)
            ]
        )

        olaf_person_id: int = self.db_connection.write_dict(
            person_table_name, values={
                'name': 'Olaf',
                'age': 64,
                'city_of_birth': 'Bielefeld',
                'extended_by_id': 0
            })

        olaf_student_id: int = self.db_connection.write_dict(
            student_table_name, values={
                'subject_of_study': 'Modern Arts',
                'extended_by_id': olaf_person_id
            }
        )
        self.db_connection.commit()

        test_result = self.db_connection.read_joined(
            table_names=[student_table_name, person_table_name],
            join_on_chain=['extended_by_id', 'extended_by_id'],
            headers_sequence=[['subject_of_study', 'extended_by_id', 'primary_key'], ['name', 'age', 'city_of_birth']]
        )

        self.assertTrue(isinstance(test_result, list))
        self.assertEqual(test_result[0], {
            'name': 'Olaf',
            'age': 64,
            'city_of_birth': 'Bielefeld',
            'subject_of_study': 'Modern Arts',
            'extended_by_id': olaf_person_id,
            'primary_key': olaf_student_id
        })


    def test_delete(self):
        self.db_connection.create_table(self.table_name, self.db_columns)
        self.assertTrue(self.db_connection.check_table_exists(self.table_name))

        for iterator in range(0, 10):
            self.row_values['numbercolumn'] = iterator
            self.db_connection.write_dict(self.table_name, self.row_values)
        self.assertEqual(10, self.db_connection.count(self.table_name))
        self.db_connection.delete(self.table_name, [f'numbercolumn = 0'])
        self.assertEqual(9, self.db_connection.count(self.table_name))

    def test_write_dict(self):
        self.db_connection.create_table(self.table_name, self.db_columns)
        self.assertTrue(self.db_connection.check_table_exists(self.table_name))

        for iterator in range(0, 10):
            self.row_values['numbercolumn'] = iterator
            self.db_connection.write_dict(self.table_name, self.row_values)
        self.assertEqual(10, self.db_connection.count(self.table_name))

    def test_update(self):
        self.db_connection.create_table(self.table_name, self.db_columns)
        self.assertTrue(self.db_connection.check_table_exists(self.table_name))
        self.db_connection.write_dict(self.table_name, self.row_values)
        self.assertEqual(1, self.db_connection.count(self.table_name))
        self.row_values["primary_key"] = 1
        self.row_values["textcolumn"] = "Updated Text"
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
            [{'cid': 0, 'name': 'textcolumn', 'type': 'VARCHAR', 'notnull': 0, 'dflt_value': None, 'pk': 0},
             {'cid': 1, 'name': 'numbercolumn', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0},
             {'cid': 2, 'name': 'primary_key', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 1}],
            self.db_connection.get_table_info(self.table_name))

    def test_check_table_exists(self):
        self.db_connection.create_table(self.table_name, self.db_columns)
        self.assertTrue(self.db_connection.check_table_exists(self.table_name))

    def test_count(self):
        self.db_connection.create_table(self.table_name, self.db_columns)
        self.assertTrue(self.db_connection.check_table_exists(self.table_name))

        for iterator in range(0, 10):
            self.row_values["numbercolumn"] = iterator
            self.db_connection.write_dict(self.table_name, self.row_values)
        self.assertEqual(10, self.db_connection.count(self.table_name))
        self.db_connection.delete(self.table_name, [f"numbercolumn = 0"])
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
        self.db_columns.append(Column("appended_column", "appended_column", DataTypes.VARCHAR.value))
        self.db_connection.update_table_columns(self.table_name, self.db_columns)
        self.assertEqual(
            [{'cid': 0, 'name': 'textcolumn', 'type': 'VARCHAR', 'notnull': 0, 'dflt_value': None, 'pk': 0},
             {'cid': 1, 'name': 'numbercolumn', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0},
             {'cid': 2, 'name': 'appended_column', 'type': 'VARCHAR', 'notnull': 0, 'dflt_value': None, 'pk': 0},
             {'cid': 3, 'name': 'primary_key', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 1}],
            (self.db_connection.get_table_info(self.table_name)))
