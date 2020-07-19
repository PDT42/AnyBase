"""
:Author: PDT
:Since: 2020/06/16

These are the routes for the ``AssetTypeManager``.
"""

from typing import List

from flask import redirect, render_template, request

from asset import AssetType
from asset.asset_manager import AssetManager
from asset.asset_type_manager import AssetTypeManager
from database import Column, DataTypes
from pages import AssetTypePage
from plugins import Plugin


def create_asset_type():
    """This is a FlaskAppRoute that lets you create ``AssetType`` dialog."""

    asset_type_manager = AssetTypeManager()
    asset_types = {
        asset_type.asset_name: asset_type.asset_type_id
        for asset_type in asset_type_manager.get_all()
    }

    if request.method == 'POST':

        asset_name = request.form.get('assetName')

        columns: List[Column] = []
        for column_name, column_datatype, column_required in \
                [(f'columnName_{i}', f'columnDataType_{i}', f'columnRequired_{i}') for i in range(0, 15)]:
            if column_name in request.form.keys():

                # Get the columns datatype from the form
                datatype_str = request.form.get(column_datatype)

                # Checking if the set data type is know to the system
                if datatype_str in DataTypes.get_all_type_names():
                    asset_type = 0
                    datatype = DataTypes[datatype_str].value

                # If not, the only possible valid entry into this field
                # is another asset_type -> Check if it exists
                elif asset_type_manager.get_one(int(datatype_str)):
                    asset_type = int(datatype_str)
                    datatype = DataTypes.INTEGER.value

                else:
                    raise AssetTypeDoesNotExistException("The asset type you referenced does not exist!")

                columns.append(Column(
                    name=request.form.get(column_name),
                    db_name=request.form.get(column_name).replace(' ', '_'),
                    datatype=datatype,
                    asset_type=asset_type,
                    required=request.form.get(column_required) == 'checkboxTrue'
                ))
            else:
                break

        new_asset_type = AssetType(
            asset_name=asset_name,
            columns=columns
        )

        asset_type_manager = AssetTypeManager()
        asset_type_manager.create_asset_type(new_asset_type)

        return redirect('/asset-types')

    data_types = DataTypes.get_all_data_types()

    return render_template(
        "create-asset-type.html",
        data_types=data_types,
        asset_types=asset_types
    )


def get_all_asset_types():
    """This is a FlaskAppRoute that shows ``AssetTypes`` available using asset-types.html."""

    asset_type_manager = AssetTypeManager()
    asset_types = asset_type_manager.get_all()

    return render_template("asset-types.html", asset_types=asset_types)


def get_one_asset_type(asset_type_id):
    """Show the Detail Page for an ``AssetType``."""

    asset_type_manager = AssetTypeManager()
    asset_type = asset_type_manager.get_one(asset_type_id)

    if request.method == 'POST' and request.form.get('deleteAsset') == 'True':
        asset_type_manager.delete_asset_type(asset_type)
        return redirect('/asset-types')

    asset_manager = AssetManager()
    assets = asset_manager.get_all(asset_type)

    asset_type_page = AssetTypePage(
        asset_type=asset_type,
        assets=assets,
        number_of_fields=1,  # TODO: implement some kind of validation for this
        layout_macro_path='layouts/one_one_layout.html',
        plugins=[
            Plugin(
                plugin_macro_path='plugins/list_assets_plugin.html',
                employed_columns={
                    0: 'Test Column 1',
                    1: 'Test Column 2'
                }
            )
        ]
    )

    return render_template("asset-type.html", asset_type_page=asset_type_page, assets=assets)
