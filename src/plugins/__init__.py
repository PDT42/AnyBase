"""
:Author: PDT
:Since: 2020/06/23

This is the module for the plugins, the functional components of the software.
"""
from typing import Any, Mapping, NamedTuple


class Plugin(NamedTuple):
    """This is a plugin."""
    macro_path: str
    columns: Mapping[Any, str]
