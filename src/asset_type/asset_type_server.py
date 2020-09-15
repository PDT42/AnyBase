"""
:Author: PDT
:Since: 2020/06/16

These are the routes for the ``AssetTypeManager``.
"""

import asyncio
from asyncio import Task
from typing import Any
from typing import List
from typing import Mapping
from typing import Set

from quart import jsonify
from quart import make_response
from quart import redirect
from quart import render_template
from quart import request

from asset.asset_manager import AssetManager
from asset_type import AssetType
from asset_type.abstract_asset_type_manager import AAssetTypeManager
from asset_type.asset_type_manager import AssetTypeManager
from config import Config
from database import Column
from database import DataType
from database import DataTypes
from exceptions.asset import AssetTypeDoesNotExistException
from exceptions.asset import ColumnNameTakenError
from exceptions.common import IllegalStateException
from exceptions.server import ServerAlreadyInitializedError
from pages import ColumnInfo
from pages import PageLayout
from pages.page_manager import PageManager
from plugins import PluginRegister


class AssetTypeServer:
    """This is the AssetTypeServer. This is created as a singleton
    so we don't need to init all the constants again and again."""

    _instance = None
    _initialized = False
    json_response = None

    DB_BATCH_SIZE = None

    @staticmethod
    def get():
        """Get the instance of this singleton."""

        if not AssetTypeServer._instance:
            AssetTypeServer._instance = AssetTypeServer()
        return AssetTypeServer._instance

    def __init__(self):
        """Create a new AssetTypeServer."""

        self.DB_BATCH_SIZE = int(Config.get().read("local database", "batch_size", 1000))
        self.json_response = Config.get().read(
            'frontend', 'json_response', False) in ["True", "true", 1]

    @staticmethod
    def register_routes(app):
        """Register the routes of this server in the ``app``."""

        if AssetTypeServer.get()._initialized:
            raise ServerAlreadyInitializedError("AssetTypeServer already initialized!")

        app.add_url_rule(
            '/asset-types',
            'stream-asset-type-data',
            AssetTypeServer.stream_asset_type_data,
            methods=['GET']
        )

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

        AssetTypeServer.get()._initialized = True

    @staticmethod
    async def _th_request_asset_type_data(th_offset):
        """Threaded method that loads a batch of assets."""

        asset_type_manager: AAssetTypeManager = AssetTypeManager()
        return asset_type_manager.get_batch(
            limit=th_offset + AssetTypeServer.get().DB_BATCH_SIZE,
            offset=th_offset)

    @staticmethod
    async def stream_asset_type_data():
        """TODO"""

        # Get AssetType and number of assets of this type
        asset_type_count = AssetTypeManager().count(ignore_slaves=True)

        event_name = "asset-types"

        async def generate_response():
            """Generate a valid stream response."""

            # Creating a set to store tasks in, so we
            # can check for updates on their status
            tasks: Set[Task] = set()

            # We don't need to schedule and execute
            # any additional tasks, if there are no
            # items available as of yet.

            if asset_type_count < 1:
                result_dict: Mapping[str, Any] = {
                    "items": [],
                    "item_count": asset_type_count
                }

                result_str: str = str(result_dict).replace('\"', '\'')

                result_message: str = f"data: [{result_str}]"
                result_message += f"\nevent: {event_name}"
                result_message += "\r\n\r\n"

                yield result_message.encode('utf-8')

            # Counting up an offset by DB_BATCH_SIZE
            # in each step of the iteration. In each
            # step we create an asyncio task, that
            # queries asset types from the database
            # using offset and offset + DB_BATCH_SIZE
            # from the database.

            offset = 0
            while offset < asset_type_count:
                task = asyncio.create_task(
                    AssetTypeServer._th_request_asset_type_data(offset))
                tasks.add(task)
                offset += AssetTypeServer.get().DB_BATCH_SIZE

            # Asyncio as_completed will yield completed
            # tasks from the set of tasks, we filled
            # earlier.

            for result_task in asyncio.as_completed(tasks):

                # Each result task will have completed
                # here. We process the result and yield
                # an encoded message that can be sent.

                result = await result_task

                result_dict: Mapping[str, Any] = {
                    "items": [asset.as_dict() for asset in result],
                    "item_count": asset_type_count
                }

                result_str: str = str(result_dict).replace('\"', '\'')

                result_message: str = f"data: [{result_str}]"
                result_message += f"\nevent: {event_name}"
                result_message += "\r\n\r\n"

                yield result_message.encode('utf-8')

        # Using a generator function as the first
        # parameter of quarts make_response, will
        # yield results to a client initiated one
        # way connection. -> Read up on SSE

        response = await make_response(
            generate_response(),
            {
                'Content-Type': 'text/event-stream',
                'Cache-Control': 'no-cache',
                'Transfer-Encoding': 'chunked',
            }
        )

        response.timeout = None

        return response

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

        asset_type: AssetType = asset_type_manager \
            .get_one_by_id(asset_type_id, extend_columns=True)

        # TODO: REMOVE! ALARM, FIRE EVERYTHING! AGAIN!

        # Comment this out, if you dont want to create a
        # PageLayout for each Type by default
        if not page_manager.get_page(asset_type.asset_type_id, False):
            page_manager.create_page(PageLayout(
                asset_type_id=asset_type_id,
                asset_page_layout=False,
                layout=[
                    [ColumnInfo(
                        plugin=PluginRegister.LIST_ASSETS.value,
                        column_width=12,
                        field_mappings={
                            'title': 'title'
                        },
                        sources=None
                    )
                    ]],
                field_mappings={},
                sources={asset_type.asset_name.lower().replace(' ', '_').replace('-', '_')}
            ))
        # TODO: REMOVE! ALARM, FIRE EVERYTHING! AGAIN!

        # If there is no layout for this asset type yet, we render the layout editor.
        if not (page_layout := page_manager.get_page(asset_type.asset_type_id, False)):
            if AssetTypeServer.get().json_response:
                return jsonify({
                    'asset_type': asset_type.as_dict()
                })
            return await render_template("layout-editor.html", asset_type=asset_type)

        # If there is, we render it.
        if AssetTypeServer.get().json_response:
            return jsonify({
                'asset_type': asset_type.as_dict(),
                'page_layout': page_layout.as_dict()
            })

        return await render_template(
            template_name_or_list="asset-type.html",
            asset_type=asset_type,
            page_layout=page_layout
        )

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
