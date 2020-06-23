"""
:Author: PDT
:Since: 2020/06/12

This is the package for all frontend creating stuff.
# TODO
"""
from typing import NamedTuple, Sequence

from asset import Asset, AssetType
from plugins import Plugin


class PageLayout(NamedTuple):
    """This is a ``PageLayout``."""
    number_of_fields: int
    macro_path: str
    plugins: Sequence[Plugin]  # TODO: Make this a Mapping?


class AssetDetailPage(NamedTuple):
    """This is an ``AssetDetailPage``."""
    asset: Asset
    page_layout: PageLayout


class AssetTypePage(NamedTuple):
    """This is an ``AssetTypePage``."""
    asset_type: AssetType
    assets: Sequence[Asset]
    page_layout: PageLayout
