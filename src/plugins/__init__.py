"""
:Author: PDT
:Since: 2020/06/23

This is the module for the plugins, the functional components of the software.
"""
from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class Plugin:
    """This is a plugin."""
    plugin_name: str
    plugin_macro_path: str


@dataclass
class PluginSettings:
    """This is as set of plugin settings."""
    plugin: Plugin
    employed_columns: Mapping[Any, str]
