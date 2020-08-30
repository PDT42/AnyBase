"""
:Author: PDT
:Since: 2020/06/16

These are the routes for the ``AssetTypeManager``.
"""

from typing import List, Mapping, Set

from quart import jsonify, redirect, render_template, request

from asset import AssetType
from asset.abstract_asset_type_manager import AAssetTypeManager
from asset.asset_manager import AssetManager
from asset.asset_type_manager import AssetTypeManager
from config import Config
from database import Column, DataType, DataTypes
from exceptions.asset import AssetTypeDoesNotExistException, ColumnNameTakenError
from exceptions.common import IllegalStateException
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
            methods=['GET']
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
                "asset_types": asset_types
            })
        return await render_template("asset-types.html", asset_types=asset_types)

    @staticmethod
    async def get_configure_asset_types():
        """Return Configuration page_layout."""

        asset_type_manager = AssetTypeManager()
        asset_types: List[Mapping] = [at.as_dict() for at in asset_type_manager.get_all()]

        return await render_template("configuration.html", asset_types=asset_types)

    @staticmethod
    async def post_create_asset_type():
        """Handle POST request to create-asset-type.

        This will create the asset type in the database
        defined by the request parameters."""

        sync_form = await request.form

        asset_name: str = sync_form.get('assetName')
        super_type = int(sync_form.get('superType', 0))
        owner_id = int(sync_form.get('ownerId', 0))

        columns: List[Column] = []
        column_names: Set[str] = set()

        for column_number in range(0, 15):

            column_name_id = f'column-name-{column_number}'
            column_datatype_id = f'column-data-type-{column_number}'
            column_required_id = f'column-required-{column_number}'
            column_asset_type_id = f'column-asset-type-{column_number}'

            if column_name_id in sync_form.keys():

                # Getting the name intended for the column.
                column_name = sync_form.get(column_name_id)
                column_db_name = column_name.replace(' ', '_').lower()

                # We won't allow multiple columns to have the same name.
                if column_name in column_names:
                    raise ColumnNameTakenError(
                        'No two columns of an asset_type can have the same name!')

                # Get the columns datatype from the form
                datatype_str = sync_form.get(column_datatype_id)
                asset_type = sync_form.get(column_asset_type_id)

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

                # Checking whether the column is required or not.
                required = sync_form.get(column_required_id) == 'checkboxTrue'

                columns.append(Column(
                    name=column_name,
                    db_name=column_db_name,
                    datatype=datatype,
                    asset_type_id=asset_type_id,
                    required=required
                ))

        # Raise an error, if no columns could
        # be constructed from from input.

        if not columns:
            raise IllegalStateException(
                "Can't create an asset type without any columns!")

        # Initialize a new AssetType.

        new_asset_type = AssetType(
            asset_name=asset_name,
            columns=columns,
            super_type=super_type,
            owner_id=owner_id
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
            asset_types={k: v.as_dict() for k, v in asset_types.items()},
            owner_id=int(request.args.get('owner-id', 0))
        )

    @staticmethod
    async def get_one_asset_type(asset_type_id):
        """Show the Detail Page for an ``AssetType``."""

        page_manager: PageManager = PageManager()
        asset_type_manager: AssetTypeManager = AssetTypeManager()

        asset_type: AssetType = asset_type_manager.get_one_by_id(asset_type_id, extend_columns=True)

        # If no layout is defined for the asset type yet
        # this will a layout-editor html page.

        # TODO: REMOVE! ALARM, FIRE EVERYTHING! AGAIN!

        # Comment this out, if you dont want to create a
        # PageLayout for each Type by default
        if not page_manager.get_page(asset_type):
            page_manager.create_page(PageLayout(
                layout=[
                    [
                        ColumnInfo(
                            plugin_name='list-assets',
                            plugin_path='plugins/list-assets-plugin.html',
                            column_width=12,
                            field_mappings={
                                'title': 'name'
                            },
                            column_id=0
                        )
                    ]
                ],
                asset_type=asset_type,
                items_url=f'/asset-type:{asset_type.asset_type_id}/stream-items',
                field_mappings={'created': 'abintern_created'}
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

        asset_type_manager: AssetTypeManager = AssetTypeManager()
        asset_type: AssetType = asset_type_manager.get_one_by_id(asset_type_id)

        # Deleting the assets of the super type, that are referenced
        # by the assets of the type being deleted.

        if (super_type_id := asset_type.get_super_type_id()) > 0:

            asset_manager: AssetManager = AssetManager()

            super_type: AssetType = asset_type_manager.get_one_by_id(super_type_id)

            for asset in asset_manager.get_all(asset_type):
                asset_manager.delete_asset(super_type, asset)

        asset_type_manager.delete_asset_type(asset_type)
        return redirect('/asset-type/config')
