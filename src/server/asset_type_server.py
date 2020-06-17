"""
:Author: PDT
:Since: 2020/06/16

These are the routes for the ``AssetTypeManager``.
"""
from threading import Lock

from asset import AssetType
from asset.asset_manager import AssetManager
from asset.asset_type_manager import AssetTypeManager
from database import Column
from flask import render_template, request


def create_asset_type():
    """Create ``AssetType`` dialog."""

    thread_lock = Lock()

    if request.method == 'POST':
        asset_name = request.form.get('assetName')
        column = Column(
            name=request.form.get('columnName'),
            datatype=request.form.get('columnDataType'),
            required=request.form.get('columnRequired') == 'checkboxTrue'
        )
        new_asset_type = AssetType(
            asset_name=asset_name,
            columns=[column]
        )

        with thread_lock:
            asset_type_manager = AssetTypeManager()
            asset_type_manager.create_asset_type(new_asset_type)
            asset_type_manager.db_connection.kill()

        return "Success"

    return render_template("create-asset-type.html")


def asset_types():
    """Show all ``AssetTypes`` available."""

    thread_lock = Lock()

    with thread_lock:
        asset_type_manager = AssetTypeManager()
        asset_t = asset_type_manager.get_all()
        asset_type_manager.db_connection.kill()

    return render_template("asset-types.html", asset_types=asset_t)


def asset_type(asset_type_id):
    """Show the Detail Page for an ``AssetType``."""

    thread_lock = Lock()

    with thread_lock:
        asset_type_manager = AssetTypeManager()
        asset_t = asset_type_manager.get_one(asset_type_id)

        asset_manager = AssetManager()
        assets = asset_manager.get_all(asset_t)
        asset_manager.db_connection.kill()

    return render_template("asset-type.html", asset_type=asset_t, assets=assets)
