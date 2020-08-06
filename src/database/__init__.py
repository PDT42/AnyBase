"""
:Author: PDT
:Since: 2020/05/27

This is the database package.
"""

from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple


class DataType(NamedTuple):
    """This is a possible datatype."""
    typename: str
    fe_name: str
    fe_type: str
    db_type: str


class DataTypes(Enum):
    """The available data types."""

    TEXT = DataType(typename='TEXT', fe_name='Text', fe_type='text', db_type='VARCHAR')
    VARCHAR = TEXT

    NUMBER = DataType(typename='NUMBER', fe_name='Number', fe_type='number', db_type='REAL')
    REAL = NUMBER

    INTEGER = DataType(typename='INTEGER', fe_name='Integer', fe_type='number', db_type='INTEGER')

    BOOLEAN = DataType(typename='BOOLEAN', fe_name='Boolean', fe_type='boolean', db_type='INTEGER')

    DATETIME = DataType(typename='DATETIME', fe_name='Datetime', fe_type='datetime-local', db_type='INTEGER')

    DATE = DataType(typename='DATE', fe_name='Date', fe_type='date', db_type='INTEGER')

    ASSET = DataType(typename='ASSET', fe_name="Asset", fe_type="number", db_type='INTEGER')

    ASSETLIST = DataType(typename='ASSETLIST', fe_name="Asset List", fe_type="text", db_type='VARCHAR')

    # --

    @classmethod
    def get_all_data_types(cls):
        """Get all distinct field values from enum."""
        return list(set([data_type.value for data_type in cls.__members__.values()]))

    @classmethod
    def get_all_type_names(cls):
        """Get the names of all available data types."""
        return list(cls.__members__.keys())


@dataclass
class Column:
    """This is a column, as required to create database column."""
    name: str
    db_name: str
    datatype: DataType
    asset_type: int = 0
    required: bool = False
