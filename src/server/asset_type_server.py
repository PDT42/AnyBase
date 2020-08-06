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
from config import Config
from database import Column, DataType, DataTypes
from exceptions.asset import AssetTypeDoesNotExistException
from exceptions.common import IllegalStateException
from pages import AssetTypePage
from plugins import Plugin, PluginSettings


class AssetTypeServer:
    """This is the AssetTypeServer."""

    _instance = None
    _json_response = None

    @staticmethod
    def get():
        """Get the instance of this singleton."""
        if not AssetTypeServer._instance:
            AssetTypeServer._instance = AssetTypeServer()
        return AssetTypeServer._instance

    def __init__(self):
        """Create a new AssetTypeServer."""
        self._json_response = bool(Config.get().read('frontend', 'json_response', False))

    @staticmethod
    def create_asset_type():
        """This is a FlaskAppRoute that lets you create ``AssetType`` dialog."""

        asset_type_manager = AssetTypeManager()
        asset_types = {
            asset_type.asset_name: asset_type.asset_type_id
            for asset_type in asset_type_manager.get_all()
        }

        # When this is called using POST, we create
        # an asset type in the database.
        if request.method == 'POST':

            columns: List[Column] = []
            asset_name = request.form.get('assetName')

            for column_number in range(0, 15):

                column_name = f'column-name-{column_number}'
                column_datatype = f'column-data-type-{column_number}'
                column_required = f'column-required-{column_number}'

                if column_name in request.form.keys():

                    # Get the columns datatype from the form
                    datatype_str = request.form.get(column_datatype)

                    # Checking if the set data type is know to the system
                    if datatype_str in DataTypes.get_all_type_names():
                        asset_type = 0
                        datatype = DataTypes[datatype_str].value

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
                        asset_type=asset_type,
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

        data_types: List[DataType] = DataTypes.get_all_data_types()

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

        asset_manager = AssetManager()
        assets = asset_manager.get_all(asset_type)

        asset_type_page = AssetTypePage(
            asset_type=asset_type,
            assets=assets,
            number_of_fields=1,
            layout_macro_path='layouts/one_one_layout.html',
            plugin_settings=[
                PluginSettings(
                    plugin=Plugin('list_assets', 'plugins/list_assets_plugin.html'),
                    employed_columns=['Column 1', 'Column 2']
                )
            ]
        )

        return render_template("asset-type.html", asset_type_page=asset_type_page, assets=assets)

    @staticmethod
    def delete_asset_type(asset_type_id):
        """Delete the ``AssetType`` with id ``asset_type_id``."""

        asset_type_manager = AssetTypeManager()
        asset_type = asset_type_manager.get_one(asset_type_id)

        if request.form.get('deleteAsset') == 'True':
            asset_type_manager.delete_asset_type(asset_type)
            return redirect('/configuration')
