"""
:Author: PDT
:Since: 2020/06/16

These are the routes for the ``AssetTypeManager``.
"""

from typing import List, Set

from quart import jsonify, redirect, render_template, request

from asset import AssetType, AssetTypePrefab, AssetTypePrefabs
from asset.abstract_asset_type_manager import AAssetTypeManager
from asset.asset_manager import AssetManager
from asset.asset_type_manager import AssetTypeManager
from config import Config
from database import Column, DataType, DataTypes
from exceptions.asset import AssetTypeDoesNotExistException, ColumnNameTakenError
from exceptions.common import IllegalStateException, InvalidArgumentError
from exceptions.server import ServerAlreadyInitializedError
from pages import ColumnInfo, PageLayout
from pages.page_manager import PageManager


class AssetTypeServer:
    """This is the AssetTypeServer. This is created as a singleton
    so we don't need to init all the constants again and again."""

    _instance = None
    _initialized = False
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
        self.json_response = Config.get().read(
            'frontend', 'json_response', False) in ["True", "true", 1]

    @staticmethod
    def register_routes(app):
        """Register the routes of this server in the ``app``."""

        if AssetTypeServer.get()._initialized:
            raise ServerAlreadyInitializedError("AssetTypeServer already initialized!")

        app.add_url_rule(
            '/asset-type/list',
            'list-asset-types',
            AssetTypeServer.get_list_asset_types,
            methods=['GET']
        )

        app.add_url_rule(
            '/asset-type/config',
            'configure-asset-types',
            AssetTypeServer.get_configure_asset_types,
            methods=['GET']
        )

        app.add_url_rule(
            '/asset-type/create',
            'get-create-asset-type',
            AssetTypeServer.get_create_asset_type,
            methods=['GET']
        )

        app.add_url_rule(
            '/asset-type/create',
            'post-create-asset-type',
            AssetTypeServer.post_create_asset_type,
            methods=['POST']
        )

        app.add_url_rule(
            '/asset-type:<int:asset_type_id>',
            'asset-type',
            AssetTypeServer.get_one_asset_type,
            methods=['GET']
        )

        app.add_url_rule(
            '/asset-type:<int:asset_type_id>/delete',
            'delete-asset-type',
            AssetTypeServer.delete_asset_type,
            methods=['POST']
        )

        AssetTypeServer.get()._initialized = False

    @staticmethod
    async def get_list_asset_types():
        """Handle get requests to ``asset-types``."""

        asset_type_manager: AAssetTypeManager = AssetTypeManager()
        asset_types: List[Mapping] = [at.as_dict() for at in asset_type_manager.get_all()]

        # Checking if the output was requested as json
        if AssetTypeServer.get().json_response:
            return jsonify({
                "asset_types": [a.as_dict() for a in asset_types]
            })
        return await render_template("asset-types.html", asset_types=asset_types)

    @staticmethod
    async def get_configure_asset_types():
        """Return Configuration page_layout."""

        asset_type_manager = AssetTypeManager()
        asset_types = asset_type_manager.get_all()

        return await render_template("configuration.html", asset_types=asset_types)

    @staticmethod
    async def post_create_asset_type():
        """Handle POST request to create-asset-type.

        This will create the asset type in the database
        defined by the request parameters."""

        sync_form = await request.form

        columns: List[Column] = []
        column_names: Set[str] = set()
        asset_name = sync_form.get('assetName')
        super_type = int(sync_form.get('superType'))

        # TODO: Check no two columns have the same name

        column_number: int = 0

        while column_number is not None:

            column_name = f'column-name-{column_number}'
            column_datatype = f'column-data-type-{column_number}'
            column_required = f'column-required-{column_number}'
            column_asset_type = f'column-asset-type-{column_number}'

            if column_name in sync_form.keys():

                # Get the columns datatype from the form
                datatype_str = sync_form.get(column_datatype)
                asset_type = sync_form.get(column_asset_type)

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

                column_name = sync_form.get(column_name)
                column_db_name = column_name.replace(' ', '_').lower()

                if column_name in column_names:
                    raise ColumnNameTakenError(
                        'No two columns of an asset_type can have the same name!')

                required = sync_form.get(column_required) == 'checkboxTrue'

                columns.append(Column(
                    name=column_name,
                    db_name=column_db_name,
                    datatype=datatype,
                    asset_type_id=asset_type_id,
                    required=required
                ))
                column_number += 1
            else:
                break

        # Raise an error, if no columns could
        # be constructed from from input.

        if not columns:
            raise IllegalStateException(
                "Can't create an asset type without any columns!")

        # Initialize a new AssetType.

        new_asset_type = AssetType(
            asset_name=asset_name,
            columns=columns,
            super_type=super_type
        )

        asset_type_manager = AssetTypeManager()
        asset_type_manager.create_asset_type(new_asset_type)

        return redirect('/asset-type/config')

    @staticmethod
    async def get_create_asset_type():
        """Handle get requests to ``create-asset-type``.

        This will return a rendered template, containing
        a create form, which can be used to defined a
        new asset type in the system."""

        asset_type_manager: AAssetTypeManager = AssetTypeManager()

        asset_types = {
            asset_type.asset_type_id: asset_type
            for asset_type in asset_type_manager.get_all()
        }

        # Checking if the request argument Prefab was provided
        if prefab_arg := request.args.get('prefab'):

            if prefab_arg in [False, [], '']:
                raise InvalidArgumentError()

            prefab_arg = prefab_arg.upper()
            prefab_names = AssetTypeServer.get().prefab_names

            if prefab_arg in prefab_names:
                prefab: AssetTypePrefab = AssetTypePrefabs[prefab_arg].value
                prefab_dict = prefab.as_dict()

                for column in prefab_dict['columns']:
                    if column['asset_type_id'] > 0:
                        column['result_columns'] = asset_type_manager \
                            .get_one(column['asset_type_id'])

                return await render_template(
                    "create-asset-type-from-prefab.html",
                    prefab=prefab_dict
                )

        data_types: List[DataType] = DataTypes.get_all_data_types()

        # Checking if the output was requested as json
        if AssetTypeServer.get().json_response:
            return jsonify({
                "data_types": [d.as_dict() for d in data_types],
                "asset_types": {k: v.as_dict() for k, v in asset_types.items()}
            })
        return await render_template(
            "create-asset-type.html",
            data_types=[d.as_dict() for d in data_types],
            asset_types={k: v.as_dict() for k, v in asset_types.items()}
        )

    @staticmethod
    async def get_one_asset_type(asset_type_id):
        """Show the Detail Page for an ``AssetType``."""

        page_manager: PageManager = PageManager()
        asset_type_manager: AssetTypeManager = AssetTypeManager()

        asset_type: AssetType = asset_type_manager.get_one(asset_type_id, extend_columns=True)

        # TODO: REMOVE! ALARM, FIRE EVERYTHING! AGAIN!

        # Comment this out, if you dont want to create a
        # PageLayout for each Type by default

        page_manager.create_page(PageLayout(
            layout=[
                [
                    ColumnInfo(
                        plugin_name='list-assets',
                        plugin_path='plugins/list-assets-plugin.html',
                        column_width=12,
                        field_mappings={
                            'title': 'name'},
                        column_id=0
                    )
                ]
            ],
            asset_type=asset_type, items_url=f'/asset-type/{asset_type.asset_type_id}/stream-items'
        ))
        # TODO: REMOVE! ALARM, FIRE EVERYTHING! AGAIN!

        if not (page_layout := page_manager.get_page(asset_type)):
            if AssetTypeServer.get().json_response:
                return jsonify({
                    'asset_type': asset_type.as_dict()
                })
            return await render_template("layout-editor.html", asset_type=asset_type)

        if AssetTypeServer.get().json_response:
            return jsonify({
                'page_layout': page_layout.as_dict()
            })
        return await render_template("asset-type.html", page_layout=page_layout)

    @staticmethod
    async def delete_asset_type(asset_type_id):
        """Delete the ``AssetType`` with id ``asset_type_id``."""

        sync_form = await request.form

        asset_type_manager: AssetTypeManager = AssetTypeManager()
        asset_type: AssetType = asset_type_manager.get_one(asset_type_id)

        if sync_form.get('deleteAssetType') == 'True':

            # Deleting the assets of the super type, that are referenced
            # by the assets of the type being deleted.

            if (super_type_id := asset_type.get_super_type_id()) > 0:

                asset_manager: AssetManager = AssetManager()

                super_type: AssetType = asset_type_manager.get_one(super_type_id)

                for asset in asset_manager.get_all(asset_type):
                    asset_manager.delete_asset(super_type, asset)

            asset_type_manager.delete_asset_type(asset_type)
            return redirect('/asset-type/config')
