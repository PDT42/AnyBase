"""
:Author: PDT
:Since: 2020/07/01

These are exceptions used in the database package.
"""


class TableDoesNotExistException(Exception):
    pass


class TableAlreadyExistsException(Exception):
    pass


class ColumnAlreadyExistsException(Exception):
    pass


class ColumnDoesNotExistException(Exception):
    pass


class DataTypeDoesNotExistException(Exception):
    pass


class DataTypeChangedException(Exception):
    pass


class MissingValueException(Exception):
    pass


class UniqueConstraintError(Exception):
    pass
