"""
:Author: PDT
:Since: 2020/06/12

This is the package for all frontend creating stuff.
# TODO
"""
from dataclasses import dataclass
from typing import NamedTuple, Sequence

from asset import Asset, AssetType
from plugins import Plugin


@dataclass
class PageLayout:
    """This is a ``PageLayout``."""
    number_of_fields: int
    layout_macro_path: str
    plugins: Sequence[Plugin]  # TODO: Make this a Mapping?


@dataclass
class AssetDetailPage(PageLayout):
    """This is an ``AssetDetailPage``."""
    asset: Asset


@dataclass
class AssetTypePage(PageLayout):
    """This is an ``AssetTypePage``."""
    asset_type: AssetType
    assets: Sequence[Asset]
