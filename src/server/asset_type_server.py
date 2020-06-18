"""
:Author: PDT
:Since: 2020/06/16

These are the routes for the ``AssetTypeManager``.
"""
from threading import Lock
from typing import List

from asset import AssetType
from asset.asset_manager import AssetManager
from asset.asset_type_manager import AssetTypeManager
from database import Column, DataTypes
from flask import redirect, render_template, request


def create_asset_type():
    """This is a FlaskAppRoute that lets you create ``AssetType`` dialog."""

    if request.method == 'POST':

        asset_name = request.form.get('assetName')

        columns: List[Column] = []
        for column_name, column_datatype, column_required in \
                [(f'columnName_{i}', f'columnDataType_{i}', f'columnRequired_{i}') for i in range(0, 26)]:
            if column_name in request.form.keys():
                columns.append(Column(
                    name=request.form.get(column_name),
                    datatype=request.form.get(DataTypes.__dict__[column_datatype]),
                    required=request.form.get(column_required) == 'checkboxTrue'
                ))
            else:
                break

        new_asset_type = AssetType(
            asset_name=asset_name,
            columns=columns
        )

        thread_lock = Lock()
        with thread_lock:
            asset_type_manager = AssetTypeManager()
            asset_type_manager.create_asset_type(new_asset_type)
            asset_type_manager.goodbye()

        return redirect('/asset-types')

    return render_template("create-asset-type.html")


def asset_types():
    """This is a FlaskAppRoute that shows ``AssetTypes`` available using asset-types.html."""

    thread_lock = Lock()

    with thread_lock:
        asset_type_manager = AssetTypeManager()
        asset_t = asset_type_manager.get_all()
        asset_type_manager.goodbye()

    return render_template("asset-types.html", asset_types=asset_t)


def asset_type(asset_type_id):
    """Show the Detail Page for an ``AssetType``."""

    thread_lock = Lock()

    with thread_lock:
        asset_type_manager = AssetTypeManager()
        asset_t = asset_type_manager.get_one(asset_type_id)

        if request.method == 'DELETE':
            asset_type_manager.delete_asset_type(asset_t)
            return redirect('/asset-types')

        asset_manager = AssetManager()
        assets = asset_manager.get_all(asset_t)
        asset_type_manager.goodbye()
        asset_manager.goodbye()

    return render_template("asset-type.html", asset_type=asset_t, assets=assets)
