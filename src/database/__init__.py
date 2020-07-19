"""
:Author: PDT
:Since: 2020/05/27

This is the database package.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import NamedTuple


class DataType(NamedTuple):
    """This is a possible datatype."""
    typename: str
    fe_name: str
    db_type: str
    convert: callable


class DataTypes(Enum):
    """The available data types."""

    TEXT = DataType(typename='TEXT', fe_name='Text', db_type='VARCHAR', convert=str)
    VARCHAR = TEXT
    NUMBER = DataType(typename='NUMBER', fe_name='Number', db_type='REAL', convert=float)
    REAL = NUMBER
    INTEGER = DataType(typename='INTEGER', fe_name='Integer', db_type='INTEGER', convert=int)
    DATETIME = DataType(typename='DATETIME', fe_name='Date', db_type='INTEGER', convert=datetime.utcfromtimestamp)

    @classmethod
    def get_all(cls):
        """Get all distinct field values from enum."""
        return set([data_type.value for data_type in cls.__members__.values()])


@dataclass
class Column:
    """This is a column, as required to create database column."""
    name: str
    db_name: str
    datatype: DataType
    asset_type: int = 0
    required: bool = False
