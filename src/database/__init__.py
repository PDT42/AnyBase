"""
:Author: PDT
:Since: 2020/05/27

This is the database package.
"""
from typing import NamedTuple


class Column(NamedTuple):
    """This is a column, as required to create database column."""
    name: str
    datatype: str
    required: bool
    primary_key: bool
