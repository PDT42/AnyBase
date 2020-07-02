"""
:Author: PDT
:Since: 2020/07/01

These are exceptions used in the database package.
"""


class TableDoesNotExistException(Exception):
    pass


class TableAlreadyExistsException(Exception):
    pass


class DataTypeDoesNotExistException(Exception):
    pass
