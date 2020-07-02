"""
:Author: PDT
:Since: 2020/05/27

This is the database package.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple

from exceptions.database import DataTypeDoesNotExistException


class DataType(NamedTuple):
    """This is a possible datatype."""
    typename: str
    db_type: str
    convert: callable


class DataTypes:
    """The available data types."""

    TEXT = DataType(typename='TEXT', db_type='VARCHAR', convert=str)
    VARCHAR = TEXT
    NUMBER = DataType(typename='NUMBER', db_type='REAL', convert=float)
    REAL = NUMBER
    INTEGER = DataType(typename='INTEGER', db_type='INTEGER', convert=int)
    DATETIME = DataType(typename='DATETIME', db_type='INTEGER', convert=datetime.utcfromtimestamp)

    # TODO: Add additional required types
    # TODO: Update sqlite connection using this

    @staticmethod
    def get(type_name: str):
        data_type = DataTypes.__dict__.get(type_name, None)
        if data_type:
            return data_type
        raise DataTypeDoesNotExistException(f"The datatype {type_name} does not exist!")


@dataclass
class Column:
    """This is a column, as required to create database column."""
    name: str
    datatype: DataType
    required: bool
