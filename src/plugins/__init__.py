"""
:Author: PDT
:Since: 2020/06/23

This is the module for the plugins, the functional components of the software.
"""
from dataclasses import dataclass
from typing import Sequence


@dataclass
class Plugin:
    """This is a plugin."""
    plugin_name: str
    plugin_macro_path: str
    plugin_id: int = None


@dataclass
class PluginSettings:
    """This is as set of plugin settings."""
    plugin: Plugin
    employed_columns: Sequence[str]
    plugin_settings_id: int = None
