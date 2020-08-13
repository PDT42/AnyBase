"""
:Author: PDT
:Since: 2020/06/16

These are the routes for the ``AssetTypeManager``.
"""
from typing import List

from flask import jsonify, redirect, render_template, request

from asset import AssetType, AssetTypePrefab, AssetTypePrefabs
from asset.abstract_asset_type_manager import AAssetTypeManager
from asset.asset_manager import AssetManager
from asset.asset_type_manager import AssetTypeManager
from config import Config
from database import Column, DataType, DataTypes
from exceptions.asset import AssetTypeDoesNotExistException
from exceptions.common import IllegalStateException
from pages import AssetTypePage, ColumnInfo, RowInfo
from pages.asset_type_page_manager import AssetTypePageManager
from server.asset_server import request_asset_data


class AssetTypeServer:
    """This is the AssetTypeServer. This is created as a singleton
    so we don't need to init all the constants again and again."""

    _instance = None
    json_response = None

    @staticmethod
    def get():
        """Get the instance of this singleton."""

        if not AssetTypeServer._instance:
            AssetTypeServer._instance = AssetTypeServer()
        return AssetTypeServer._instance

    def __init__(self):
        """Create a new AssetTypeServer."""

        self.prefab_names = AssetTypePrefabs.get_all_asset_type_prefab_names()
        self.json_response = Config.get().read('frontend', 'json_response', False) in ["True", "true", 1]

    @staticmethod
    def post_create_asset_type():
        """Handle POST request to create-asset-type.

        This will create the asset type defined by
        the request parameters."""

        columns: List[Column] = []
        asset_name = request.form.get('assetName')

        for column_number in range(0, 15):

            column_name = f'column-name-{column_number}'
            column_datatype = f'column-data-type-{column_number}'
            column_required = f'column-required-{column_number}'
            column_asset_type = f'column-asset-type-{column_number}'

            r = request  # TODO: remove, debug

            if column_name in request.form.keys():

                # Get the columns datatype from the form
                datatype_str = request.form.get(column_datatype)
                asset_type = request.form.get(column_asset_type)

                # Checking if the set data type is know to the system
                if datatype_str in DataTypes.get_all_type_names():
                    asset_type_id = 0
                    datatype = DataTypes[datatype_str].value

                    if datatype in [DataTypes.ASSET.value, DataTypes.ASSETLIST.value]:
                        asset_type_id = int(asset_type)

                # If the datatype is unknown an exception is raised
                # this should never be the case, since the drop down
                # menu of available data types is filled from the BE
                else:
                    raise AssetTypeDoesNotExistException(
                        "The data type you referenced does not exist!")

                column_name = request.form.get(column_name)
                column_db_name = column_name.replace(' ', '_').lower()

                required = request.form.get(column_required) == 'checkboxTrue'

                columns.append(Column(
                    name=column_name,
                    db_name=column_db_name,
                    datatype=datatype,
                    asset_type_id=asset_type_id,
                    required=required
                ))
            else:
                break

        if not columns:
            raise IllegalStateException("Can't create an asset type without any columns!")

        new_asset_type = AssetType(
            asset_name=asset_name,
            columns=columns
        )

        asset_type_manager = AssetTypeManager()
        asset_type_manager.create_asset_type(new_asset_type)

        return redirect('/configuration')

    @staticmethod
    def get_create_asset_type():
        """Handle get requests to create-asset-type.

        This will return a rendered template, containing
        a create form, which can be used to defined a
        new asset type in the system."""

        asset_type_manager: AAssetTypeManager = AssetTypeManager()
        asset_types = {
            asset_type.asset_name: asset_type.asset_type_id
            for asset_type in asset_type_manager.get_all()
        }

        # Checking if the request argument Prefab was provided
        if request_arg := request.args.get('prefab'):
            request_arg = request_arg.upper()
            prefab_names = AssetTypeServer.get().prefab_names

            if request_arg in prefab_names:
                prefab: AssetTypePrefab = AssetTypePrefabs[request_arg].value
                prefab_json = dict(jsonify(prefab).json)

                for column in prefab_json['columns']:
                    if column['asset_type_id'] > 0:
                        column['asset_type'] = asset_type_manager.get_one(column['asset_type_id'])

                return render_template(
                    "create-asset-type-from-prefab.html",
                    prefab=prefab_json
                )

        data_types: List[DataType] = DataTypes.get_all_data_types()

        # checking ig the output was requested as json
        if AssetTypeServer.get().json_response:
            return jsonify({
                "data_types": data_types,
                "asset_types": asset_types
            })

        return render_template(
            "create-asset-type.html",
            data_types=data_types,
            asset_types=asset_types
        )

    @staticmethod
    def get_all_asset_types():
        """This is a FlaskAppRoute that shows ``AssetTypes`` available using asset-types.html."""

        asset_type_manager = AssetTypeManager()
        asset_types = asset_type_manager.get_all()

        return render_template("asset-types.html", asset_types=asset_types)

    @staticmethod
    def get_one_asset_type(asset_type_id):
        """Show the Detail Page for an ``AssetType``."""

        asset_type_manager = AssetTypeManager()
        asset_type = asset_type_manager.get_one(asset_type_id)

        request_asset_data(asset_type.asset_type_id, depth=1)

        asset_manager = AssetManager()
        assets = asset_manager.get_all(asset_type, depth=1)

        # TODO: Get AssetTypePage from AssetTypePageManager

        asset_type_page = AssetTypePage(
            layout_id=0,
            asset_type=asset_type,
            assets=assets,  # TODO: Transmit query url instead of items
            layout=[
                RowInfo(columns=[
                    ColumnInfo(
                        column_width=12,
                        plugin_name='list-assets',
                        plugin_path='plugins/list-assets-plugin.html',
                        employed_columns=['name'],
                        column_id=0
                    )
                ]),
            ]
        )

        AssetTypePageManager().create_page(asset_type_page)
        page = AssetTypePageManager().get_page(asset_type)

        return render_template("asset-type.html", asset_type_page=page)

    @staticmethod
    def delete_asset_type(asset_type_id):
        """Delete the ``AssetType`` with id ``asset_type_id``."""

        asset_type_manager = AssetTypeManager()
        asset_type = asset_type_manager.get_one(asset_type_id)

        if request.form.get('deleteAsset') == 'True':
            asset_type_manager.delete_asset_type(asset_type)
            return redirect('/configuration')
