"""
:Author: PDT
:Since: 2020/06/16

These are the routes for the ``AssetTypeManager``.
"""

from flask import redirect, render_template, request

from asset import Asset
from asset.asset_manager import AssetManager
from asset.asset_type_manager import AssetTypeManager


def create_asset(asset_type_id: int):
    """This is a FlaskAppRoute that lets you create an ``Asset``."""

    asset_type_manager = AssetTypeManager()
    asset_type = asset_type_manager.get_one(asset_type_id)

    if request.method == 'POST':

        asset_manager = AssetManager()

        asset_data = {}

        for column in asset_type.columns:

            # Column is missing in form but is required
            if column.required and column.name not in request.form.keys():
                return 1  # TODO: Validation

            # Column is missing and isn't required
            elif not column.required and column.name not in request.form.keys():
                continue

            # Column is present
            else:
                asset_data[column.name] = column.datatype.convert(request.form[column.name])

        asset = Asset(asset_id=None, data=asset_data)
        asset_manager.create_asset(asset_type, asset)

        return redirect(f'/asset-type/{asset_type_id}')

    return render_template("create-asset.html", asset_type=asset_type)
