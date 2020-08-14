"""
:Author: PDT
:Since: 2020/06/16

These are the routes for the project.
"""
from quart import render_template

from asset.asset_type_manager import AssetTypeManager


async def index():
    """Return home page_layout."""
    return await render_template("base.html")


async def configuration():
    """Return Configuration page_layout."""

    asset_type_manager = AssetTypeManager()
    asset_types = asset_type_manager.get_all()

    return await render_template("configuration.html", asset_types=asset_types)
