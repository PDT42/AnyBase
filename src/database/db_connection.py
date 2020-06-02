"""
:Auth: PDT
:Since: 2020/05/24

This is the database connection module. It contains the DbConnection class, which is an interface for any database
connection used in the scope of the project. The DbConnection class must contain all methods used to interact with the
database.
"""

from abc import abstractmethod
from typing import Any, Mapping, Sequence

from database import Column


class DbConnection:
    """This is the DbConnection."""

    @staticmethod
    @abstractmethod
    def get():
        """Get the instance of the Connection singleton."""
        pass

    @abstractmethod
    def commit(self):
        """Commit changes."""
        pass

    @abstractmethod
    def close(self):
        """Commit changes and close the connection."""
        pass

    @abstractmethod
    def read(
            self, table_name: str,
            headers: Sequence[str],
            and_filters: Sequence[str] = None,
            or_filters: Sequence[str] = None,
            offset: int = None,
            limit: int = None
    ):
        """Read from the database."""
        pass

    @abstractmethod
    def write_dict(
            self, table_name: str,
            values: Mapping[str, Any]
    ):
        """Write to the database."""
        pass

    @abstractmethod
    def create_table(
            self, table_name: str,
            columns: Sequence[Column]
    ):
        """Create a table in the database."""
        pass

    @abstractmethod
    def get_table_info(self, table_name: str):
        """TODO"""
        pass

    @abstractmethod
    def check_table_exists(self, resource_name) -> bool:
        """TODO"""
        pass
