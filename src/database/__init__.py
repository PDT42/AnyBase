"""
:Author: PDT
:Since: 2020/05/27

This is the database package.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import NamedTuple

from database.util import convert_asset_to_dbtype, convert_assetlist_to_dbtype


class DataType(NamedTuple):
    """This is a possible datatype."""
    typename: str
    fe_name: str
    fe_type: str
    db_type: str
    convert_to_dbtype: callable
    convert_from_db_type: callable


class DataTypes(Enum):
    """The available data types."""

    TEXT = DataType(typename='TEXT', fe_name='Text', fe_type='text', db_type='VARCHAR',
                    convert_to_dbtype=str, convert_from_db_type=str)
    VARCHAR = TEXT

    NUMBER = DataType(typename='NUMBER', fe_name='Number', fe_type='number', db_type='REAL',
                      convert_to_dbtype=float, convert_from_db_type=float)
    REAL = NUMBER

    INTEGER = DataType(typename='INTEGER', fe_name='Integer', fe_type='number', db_type='INTEGER',
                       convert_to_dbtype=int, convert_from_db_type=int)

    BOOLEAN = DataType(typename='BOOLEAN', fe_name='Boolean', fe_type='boolean', db_type='INTEGER',
                       convert_to_dbtype=int, convert_from_db_type=bool)

    DATETIME = DataType(
        typename='DATETIME', fe_name='Datetime', fe_type='datetime-local', db_type='INTEGER',
        convert_to_dbtype=lambda dt: int(dt.timestamp()),
        convert_from_db_type=lambda timestamp: datetime.fromtimestamp(timestamp)
    )

    DATE = DataType(
        typename='DATE', fe_name='Date', fe_type='date', db_type='INTEGER',
        convert_to_dbtype=lambda d: int(datetime.combine(d, datetime.min.time()).timestamp()),
        convert_from_db_type=lambda timestamp: datetime.fromtimestamp(timestamp).date()
    )

    ASSET = DataType(
        typename='ASSET', fe_name="Asset", fe_type="number", db_type='INTEGER',
        convert_to_dbtype=convert_asset_to_dbtype, convert_from_db_type=int
    )

    ASSETLIST = DataType(
        typename='ASSETLIST', fe_name="Asset List", fe_type="text", db_type='VARCHAR',
        convert_to_dbtype=convert_assetlist_to_dbtype,
        convert_from_db_type=lambda al: [int(a) for a in al.split(';')]
    )

    # --

    @classmethod
    def get_all_data_types(cls):
        """Get all distinct field values from enum."""
        return set([data_type.value for data_type in cls.__members__.values()])

    @classmethod
    def get_all_type_names(cls):
        """Get the names of all available data types."""
        return cls.__members__.keys()


@dataclass
class Column:
    """This is a column, as required to create database column."""
    name: str
    db_name: str
    datatype: DataType
    asset_type: int = 0
    required: bool = False
