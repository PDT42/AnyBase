"""
:Author: PDT
:Since: 2020/06/16

These are the routes for the project.
"""

from flask import render_template

from asset.asset_type_manager import AssetTypeManager


def index():
    """Return home page."""
    return render_template("base.html")


def configuration():
    """Return Configuration page."""

    asset_type_manager = AssetTypeManager()
    asset_types = asset_type_manager.get_all()

    return render_template("configuration.html", asset_types=asset_types)
