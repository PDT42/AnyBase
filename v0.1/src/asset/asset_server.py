"""
:Author: PDT
:Since: 2020/06/16

These are the routes for the ``AssetTypeManager``.
"""

import asyncio
from asyncio import Task
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Mapping
from typing import MutableMapping
from typing import Set

from flask import jsonify
from quart import make_response
from quart import redirect
from quart import render_template
from quart import request

from asset import Asset
from asset.abstract_asset_manager import AAssetManager
from asset.asset_manager import AssetManager
from asset_type import AssetType
from asset_type.abstract_asset_type_manager import AAssetTypeManager
from asset_type.asset_type_manager import AssetTypeManager
from config import Config
from database import DataType
from database import DataTypes
from exceptions.asset import AssetTypeDoesNotExistException
from exceptions.database import MissingValueException
from exceptions.plugins import PageAlreadyExistsException
from exceptions.server import ServerAlreadyInitializedError
from pages import PageLayout
from pages.abstract_page_manager import APageManager
from pages.page_manager import PageManager
from plugins import Plugin
from plugins import PluginRegister
from plugins import PluginType


class AssetServer:
    """This is a server singleton."""

    _instance: 'AssetServer' = None
    _initialized: bool = False

    DB_BATCH_SIZE: int = None  # The batch size for streaming

    # Conversion functions to convert values gotten
    # from the frontend, to the type used for that
    # DataType in the backend. TODO: (¬_¬ )

    _conversions: Mapping[DataType, callable] = {
        DataTypes.TEXT.value: str,
        DataTypes.NUMBER.value: float,
        DataTypes.INTEGER.value: int,
        DataTypes.BOOLEAN.value: bool,
        DataTypes.DATETIME.value: lambda dt: datetime.strptime(dt, '%Y-%m-%dT%H:%M'),
        DataTypes.DATE.value: lambda d: datetime.strptime(d, '%Y-%m-%d'),
        DataTypes.ASSET.value: int,
        DataTypes.ASSETLIST.value: lambda al: [int(a) for a in al.split(',')]
    }

    @classmethod
    def get(cls):
        """Get the instance of this singleton."""

        if not cls._instance:
            cls._instance = AssetServer()
        return cls._instance

    def __init__(self):
        """Create a new AssetServer."""

        # Get relevant info from the config
        self.DB_BATCH_SIZE = int(Config.get().read("local database", "batch_size", 1000))
        self.JSON_RESPONSE = Config.get().read(
            'frontend', 'JSON_RESPONSE', False) in ["True", "true", 1]

    @staticmethod
    def register_routes(app):
        """Register the routes of this server in the ``app``."""

        if AssetServer.get()._initialized:
            raise ServerAlreadyInitializedError("AssetServer already initialized!")

        app.add_url_rule(
            '/asset-type:<int:asset_type_id>/stream/<string:channel>',
            'stream-asset-data',
            AssetServer.stream_asset_data,
            methods=['GET']
        )

        app.add_url_rule(
            '/asset-type:<int:asset_type_id>/create-asset',
            'post-create-asset',
            AssetServer.post_create_asset,
            methods=['POST']
        )

        app.add_url_rule(
            '/asset-type:<int:asset_type_id>/create-asset',
            'get-create-asset',
            AssetServer.get_create_asset,
            methods=['GET']
        )

        app.add_url_rule(
            '/asset-type:<int:asset_type_id>/asset:<int:asset_id>/create-detail-view',
            'post-create-detail-view',
            AssetServer.post_create_detail_page_layout,
            methods=['POST']
        )

        app.add_url_rule(
            '/asset-type:<int:asset_type_id>/asset:<int:asset_id>',
            'get-asset',
            AssetServer.get_one_asset,
            methods=['GET']
        )

        app.add_url_rule(
            '/asset-type:<int:asset_type_id>/asset:<int:asset_id>/delete',
            'delete-asset',
            AssetServer.delete_asset,
            methods=['GET']
        )

        AssetServer.get()._initialized = True

    @staticmethod
    async def _th_request_asset_data(th_offset, asset_type, and_filters, depth, load_sub_depth):
        """Threaded method that loads a batch of assets."""

        asset_manager: AAssetManager = AssetManager()
        return asset_manager.get_batch(
            asset_type=asset_type,
            and_filters=and_filters,
            offset=th_offset,
            limit=th_offset + AssetServer.get().DB_BATCH_SIZE,
            depth=depth,
            load_sub_depth=load_sub_depth)

    @staticmethod
    async def stream_asset_data(asset_type_id: int, channel: str, depth: int = 0, load_sub_depth: int = 0):
        """TODO ಥ_ಥ"""

        # Get AssetType and number of assets of this type
        asset_type = AssetTypeManager().get_one_by_id(asset_type_id)

        and_filters: List[str] = AssetServer._get_filters_from_request(asset_type, request.args)

        if not asset_type:
            raise AssetTypeDoesNotExistException(
                f"Error in GET to 'stream-asset-data'. There is no " +
                f"AssetType with the id: {asset_type_id}!")

        asset_count = AssetManager().count(asset_type, and_filters=and_filters)

        async def generate_response():
            """Generate a valid stream response."""

            # Creating a set to store tasks in, so we
            # can check for updates on their status
            tasks: Set[Task] = set()

            # We don't need to schedule and execute
            # any additional tasks, if there are no
            # items available as of yet.

            if asset_count < 1:
                result_dict: Mapping[str, Any] = {
                    "items": [],
                    "item_count": asset_count
                }

                result_str: str = str(result_dict).replace('\"', '\'')

                result_message: str = f"data: [{result_str}]"
                result_message += f"\nevent: {channel}"
                result_message += "\r\n\r\n"

                yield result_message.encode('utf-8')

            # Counting up an offset by DB_BATCH_SIZE
            # in each step of the iteration. In each
            # step we create an asyncio task, that
            # queries assets from the database using
            # offset and offset + DB_BATCH_SIZE from
            # the database.

            offset = 0
            while offset < asset_count:
                task = asyncio.create_task(
                    AssetServer._th_request_asset_data(
                        th_offset=offset,
                        asset_type=asset_type,
                        and_filters=and_filters,
                        depth=depth,
                        load_sub_depth=load_sub_depth))
                tasks.add(task)
                offset += AssetServer.get().DB_BATCH_SIZE

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
                    "item_count": asset_count
                }

                result_str: str = str(result_dict).replace('\"', '\'')

                result_message: str = f"data: [{result_str}]"
                result_message += f"\nevent: {channel}"
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
    async def post_create_asset(asset_type_id: int):
        """This is a FlaskAppRoute that lets you create an ``Asset``."""

        asset_type_manager: AAssetTypeManager = AssetTypeManager()

        asset_type: AssetType = asset_type_manager \
            .get_one_by_id(asset_type_id)
        extended_type: AssetType = asset_type_manager \
            .get_one_by_id(asset_type_id, extend_columns=True)

        # Check if an asset type with the specified type exists
        if not asset_type:
            return AssetTypeDoesNotExistException(
                f"Error in GET to 'post_create_asset'. There is no " +
                f"AssetType with the the id: {asset_type_id}!"
            )

        # Get the values from form specified
        sync_form = await request.form
        asset_data: MutableMapping[str, Any] = {}

        for column in extended_type.columns:

            # Column is missing in form but is required
            if column.required and (column.db_name not in sync_form.keys() or
                                    sync_form[column.db_name] in ['']):
                raise MissingValueException(
                    f"The required value {column.db_name} is missing in the submitted form!")

            # Column is missing and isn't required
            elif not column.required and (
                    column.db_name not in sync_form.keys() or
                    sync_form[column.db_name] in ['']):
                continue

            # TODO: Validate input

            # Column present
            asset_data[column.db_name] = AssetServer \
                ._conversions[column.datatype](sync_form[column.db_name])

        asset_manager: AAssetManager = AssetManager()

        # Init new Asset and store it in the database
        asset: Asset = Asset(data=asset_data)
        asset_manager.create_asset(asset_type, asset)

        return redirect(f'/asset-type:{asset_type_id}')

    @staticmethod
    async def get_create_asset(asset_type_id: int):
        """Handle get requests to this route. TODO"""

        asset_type_manager: AAssetTypeManager = AssetTypeManager()

        asset_type: AssetType = asset_type_manager.get_one_by_id(
            asset_type_id, extend_columns=True)

        if not asset_type:
            return AssetTypeDoesNotExistException(
                f"Error in GET to 'get_create_asset'. There is no " +
                f"asset type with the the id: {asset_type_id}!"
            )

        assets: Dict[int, List[Asset]] = {}

        # If the asset type of this asset defines columns
        # that contain other assets, we need to load them
        # so we can present them to the user.

        if field_asset_ids := [field.asset_type_id for field in asset_type.columns if field.asset_type_id]:

            # Create asset_manager only if required
            asset_manager: AAssetManager = AssetManager()

            for asset_id in field_asset_ids:
                asset_t = asset_type_manager.get_one_by_id(asset_id)
                result = asset_manager.get_all(asset_t)
                assets[asset_t.asset_type_id] = result  # [asset.asset_id for asset in results]

        # converting t
        assets = {key: [a.as_dict() for a in value] for key, value in assets.items()}

        if AssetServer.get().JSON_RESPONSE:
            return jsonify({
                'asset_type_id': asset_type.as_dict(),
                'assets': assets
            })

        return await render_template("create-asset.html", asset_type=asset_type, assets=assets)

    @staticmethod
    async def get_one_asset(asset_type_id: int, asset_id: int):
        """Handle get requests to get-asset."""

        asset_type_manager: AAssetTypeManager = AssetTypeManager()
        asset_manager: AAssetManager = AssetManager()
        page_manager: PageManager = PageManager()

        # Get the extended AssetType -> it will contain all
        # the Columns of potential supertype AssetTypes.
        asset_type: AssetType = asset_type_manager \
            .get_one_by_id(asset_type_id, extend_columns=True)
        asset: Asset = asset_manager.get_one(asset_id, asset_type)

        # Setting a default page layout
        if not (page_layout := page_manager.get_page(asset_type.asset_type_id, True)):
            return await AssetServer.get_create_detail_page_layout(asset_type, asset_id)

        # Initialize all plugins required
        for row in page_layout.layout:
            for column_info in row:

                if (server := column_info.plugin.server) is not None:
                    column_info.sources = server.get().initialize(asset_type, asset)
                    page_layout.sources.update(column_info.sources)

        # --

        if AssetServer.get().JSON_RESPONSE:
            return jsonify({
                'asset_type': asset_type.as_dict(),
                'asset_page_layout': page_layout.as_dict(),
                'asset': asset.as_dict()
            })

        return await render_template(
            template_name_or_list="asset.html",
            page_layout=page_layout,
            asset_type=asset_type,
            asset=asset)

    @staticmethod
    async def get_create_detail_page_layout(asset_type: AssetType, asset_id: int):
        """Getting a page to create a layout for the detail view of this ``asset_type``."""

        available_plugins: List[Plugin] = list(filter(
            lambda plugin: plugin.type in [PluginType.ASSET, PluginType.HYBRID],
            PluginRegister.get_all_plugins()))

        if AssetServer.get().JSON_RESPONSE:
            return jsonify({
                'asset_type': asset_type.as_dict(),
                'available_plugins': [plugin.as_dict() for plugin in available_plugins]
            })

        return await render_template(
            "layout-editor.html", asset_type=asset_type, detail_view=True,
            create_url=f'/asset-type:{asset_type.asset_type_id}/asset:{asset_id}/create-detail-view',
            available_plugins=[plugin.as_dict() for plugin in available_plugins]
        )

    @staticmethod
    async def post_create_detail_page_layout(asset_type_id: int, asset_id: int):
        """Setting the page layout for the detail page of this ``AssetType``."""

        page_manager: PageManager = PageManager()
        asset_type_manager: AssetTypeManager = AssetTypeManager()
        asset_type: AssetType = asset_type_manager.get_one_by_id(asset_type_id)

        # Check if there already is a PageLayout for this asset_type_id
        if page_manager.check_page_exists(asset_type_id, True):
            raise PageAlreadyExistsException(
                f"The detail view for asset_type_id: {asset_type_id} already exists!")

        # Generate the form ids and get the values required
        # for constructing the layout from sync_form.

        page_layout: PageLayout = APageManager.get_page_layout_from_form_data(
            asset_type=asset_type, detail_view=True, form_data=await request.form)

        # Adding common sources
        page_layout.sources.update({})

        page_manager.create_page(page_layout)

        return redirect(f'/asset-type:{asset_type_id}/asset:{asset_id}')

    @staticmethod
    def delete_asset(asset_type_id: int, asset_id: int):
        """Handle requests """

        asset_type_manager: AAssetTypeManager = AssetTypeManager()
        asset_manager: AAssetManager = AssetManager()

        asset_type = asset_type_manager.get_one_by_id(
            int(asset_type_id), extend_columns=False)
        asset = asset_manager.get_one(asset_id, asset_type)

        asset_manager.delete_asset(asset_type, asset)

        return redirect(f'/asset-type:{asset_type_id}')

    @staticmethod
    def _get_filters_from_request(
            asset_type: AssetType,
            request_args: Mapping[str, str]
    ) -> List[str]:
        """Extract query filters from request arguments."""

        asset_manager: AAssetManager = AssetManager()

        and_filters: List[str] = []

        # TODO: This will produce so many errors ... o(*^＠^*)o

        for column in asset_type.columns:

            if filter_value := request_args.get(column.db_name):
                and_filters.append(f'{column.db_name} {filter_value}')

        for header in asset_manager.ASSET_HEADERS:

            if filter_value := request_args.get(header):
                and_filters.append(f'{header} {filter_value}')

        return and_filters
