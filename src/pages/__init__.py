"""
:Author: PDT
:Since: 2020/06/12

This is the package for all frontend creating stuff.
# TODO
"""
from typing import List, NamedTuple

from asset import Asset, AssetType
from plugin.plugin import Plugin


class PageLayout(NamedTuple):
    """This is a ``PageLayout``."""
    format: int  # TODO: Datatype for Format?
    plugins: List[Plugin]


class AssetDetailPage(NamedTuple):
    """This is an ``AssetDetailPage``."""
    asset: Asset
    page_layout: PageLayout


class AssetPage(NamedTuple):
    """This is an ``AssetPage``."""
    asset_type: AssetType
    page_layout: PageLayout
