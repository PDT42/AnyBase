"""
:Auth: PDT
:Since: 2020/05/24

This is the database connection module. It contains the DbConnection class, which is an interface for any database
connection used in the scope of the project. The DbConnection class must contain all methods used to interact with the
database.
"""

from abc import abstractmethod
from typing import Any
from typing import Mapping
from typing import MutableMapping
from typing import Optional
from typing import OrderedDict
from typing import Sequence
from typing import Tuple

from database import Column
from database import DataType
from exceptions.common import MissingKeyException


class DbConnection:
    """This is the DbConnection."""

    _instance = None
    _conversions: Mapping[DataType, callable] = None

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
    def kill(self):
        """Close and delete the database connection."""
        pass

    @abstractmethod
    def reset(self):
        """Reset the connection."""
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
    def read_joined(
            self, table_headers: OrderedDict[str, Tuple[str, Sequence[str]]],
            and_filters: Sequence[str] = None,
            or_filters: Sequence[str] = None,
            offset: int = None,
            limit: int = None
    ):
        """Read from joined tables."""
        pass

    @abstractmethod
    def delete(self, table_name: str, and_filters: Sequence[str]):
        """Delete From ``table_name`` where ``filters`` apply."""
        pass

    @abstractmethod
    def write_dict(
            self, table_name: str,
            values: Mapping[str, Any]
    ) -> int:
        """Write to the database."""
        pass

    @abstractmethod
    def update(self, table_name: str, values: Mapping[str, Any]) -> int:
        """Update database entry."""
        pass

    @abstractmethod
    def update_table_name(self, table_name: str, new_table_name: str):
        """Update the name of a table in the database."""
        pass

    @abstractmethod
    def update_columns(self, table_name: str, update_columns: Mapping[str, Column]):
        """Update columns of the database table ``table_name``. The columns
        with the ``db_names`` used as keys in ``update_columns`` will be updated
        to the respective value in ``update_columns``. """
        pass

    @abstractmethod
    def update_append_column(self, table_name: str, append_column: Column):
        """Append ``append_column`` to db table named ``table_name``."""
        pass

    @abstractmethod
    def update_remove_column(self, table_name: str, remove_column: Column):
        """Remove column ``remove_column`` from db table named ``table_name``."""
        pass

    @abstractmethod
    def create_table(
            self, table_name: str,
            columns: Sequence[Column]
    ):
        """Create a table in the database."""
        pass

    @abstractmethod
    def delete_table(self, table_name: str):
        """Delete a table from the database."""

    @abstractmethod
    def get_table_info(self, table_name: str):
        """TODO"""
        pass

    @abstractmethod
    def check_table_exists(self, table_name: str) -> bool:
        """TODO"""
        pass

    @abstractmethod
    def count(self, table_name: str, query_filters: Optional[Sequence[str]] = None) -> int:
        """Count the number ob items in ``table_name``."""
        pass

    def convert_data_to_row(
            self, data: MutableMapping[str, Any],
            columns: Sequence[Column]) \
            -> MutableMapping[str, Any]:
        """Convert a data mapping as contained in an asset to a valid
        database query input."""

        row: MutableMapping[str, Any] = {}

        for column in columns:

            data_value = data.get(column.db_name, None)

            if data_value is None and not column.required:
                row[column.db_name] = None
                continue

            elif data_value is None and column.required:
                raise MissingKeyException(
                    f'The required column {column.db_name} is missing!')

            row[column.db_name] = self._conversions[column.datatype](data_value)

        return row
