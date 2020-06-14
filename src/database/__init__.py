"""
:Author: PDT
:Since: 2020/05/27

This is the database package.
"""
from enum import Enum
from typing import NamedTuple


class DataTypes(Enum):
    """The available data types."""
    TEXT = 'VARCHAR'
    NUMBER = 'REAL'
    DATE = 'DATE'
    DATETIME = 'DATETIME'
    # TODO: Update sqlite connection using this


class Column(NamedTuple):
    """This is a column, as required to create database column."""
    name: str
    datatype: str
    required: bool
