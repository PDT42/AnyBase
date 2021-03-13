"""
:Author: PDT
:Since: 2020/07/01

These are utility functions for testing.
"""
from tempfile import mkdtemp
from typing import Tuple

from config import Config
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection


def init_test_db() -> Tuple[str, DbConnection]:
    """Create a new DbConnection singleton connected to a special
    test database."""

    Config.get().change_path('U:/projects/anybase_modular_management/res/config.ini')
    tempdir = mkdtemp()
    return tempdir, SqliteConnection.get(f"{tempdir}\\database.db")
