"""
:Author: PDT
:Since: 2020/06/16

These are the routes for the ``AssetTypeManager``.
"""

import asyncio
from asyncio import Task
from datetime import datetime
from typing import Any, Dict, List, Mapping, MutableMapping, Set

from flask import jsonify
from quart import make_response, redirect, render_template, request

from asset import Asset, AssetType
from asset.abstract_asset_manager import AAssetManager
from asset.abstract_asset_type_manager import AAssetTypeManager
from asset.asset_manager import AssetManager
from asset.asset_type_manager import AssetTypeManager
from config import Config
from database import DataTypes
from exceptions.server import ServerAlreadyInitializedError
from pages import AssetPageLayout, ColumnInfo
from pages.page_manager import PageManager


class AssetServer:
    """This is a server singleton."""

    _instance = None
    _initialized = False

    DB_BATCH_SIZE = None

    @classmethod
    def get(cls):
        """Get the instance of this singleton."""
        if not cls._instance:
            cls._instance = AssetServer()
        return cls._instance

    def __init__(self):
        """Create a new AssetServer."""
        self.DB_BATCH_SIZE = int(Config.get().read("local database", "batch_size", 1000))
        self.json_response = Config.get().read(
            'frontend', 'json_response', False) in ["True", "true", 1]

    @staticmethod
    def register_routes(app):
        """Register the routes of this server in the ``app``."""

        if AssetServer.get()._initialized:
            raise ServerAlreadyInitializedError("AssetServer already initialized!")

        app.add_url_rule(
            '/asset-type:<int:asset_type_id>/stream-items',
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
            '/asset-type:<int:asset_type_id>/<int:asset_id>',
            'get-asset',
            AssetServer.get_one_asset,
            methods=['GET']
        )

        app.add_url_rule(
            '/asset-type:<int:asset_type_id>/<int:asset_id>/delete',
            'delete-asset',
            AssetServer.delete_asset,
            methods=['GET']
        )

        AssetServer.get()._initialized = True

    @staticmethod
    async def th_request_asset_data(th_offset, asset_type, depth):
        """Threaded method that loads a batch of assets."""

        asset_manager: AAssetManager = AssetManager()
        return asset_manager.get_batch(
            asset_type=asset_type,
            offset=th_offset,
            limit=th_offset + AssetServer.get().DB_BATCH_SIZE,
            depth=depth
        )

    @staticmethod
    async def stream_asset_data(asset_type_id: int, depth: int = 0):
        """Check if more assets are available."""

        # Get AssetType and number of assets of this type
        asset_type = AssetTypeManager().get_one(asset_type_id)
        asset_count = AssetManager().count(asset_type)

        event_name = "items-data"

        async def generate_response():
            """Generate utf-8 encoded messages containing
             """

            # Creating a set to store tasks in, so we
            # can check for updates on their status
            tasks: Set[Task] = set()

            # Counting up an offset by DB_BATCH_SIZE
            # in each step of the iteration. In each
            # step we create an asyncio task, that
            # queries assets from the database using
            # offset and offset + DB_BATCH_SIZE from
            # the database.

            offset = 0
            while offset < asset_count:
                task = asyncio.create_task(AssetServer.th_request_asset_data(offset, asset_type, depth))
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

                # Get the items
                result_dict: Mapping[str, Any] = {
                    "items": [asset.as_dict() for asset in result],
                    "item_count": asset_count
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
    async def post_create_asset(asset_type_id: int):
        """This is a FlaskAppRoute that lets you create an ``Asset``."""

        asset_type_manager: AAssetTypeManager = AssetTypeManager()
        asset_manager: AAssetManager = AssetManager()

        extended_type: AssetType = asset_type_manager.get_one(asset_type_id, extend_columns=True)
        asset_type: AssetType = asset_type_manager.get_one(asset_type_id)

        sync_form = await request.form
        asset_data: MutableMapping[str, Any] = {}

        for column in extended_type.columns:

            # Column is missing in form but is required
            if column.required and column.db_name not in sync_form.keys():
                return 1  # TODO: Validation

            # Column is missing and isn't required
            elif not column.required and column.db_name not in sync_form.keys():
                continue

            # Column is present
            # TODO: This should be done in a cleaner way - The DataTypes feel kinda muddled
            else:
                # TODO: Validate input
                if column.datatype is DataTypes.DATETIME.value:
                    asset_data[column.db_name] = datetime.strptime(sync_form[column.db_name], '%Y-%m-%dT%H:%M')
                    continue
                if column.datatype is DataTypes.DATE.value:
                    asset_data[column.db_name] = datetime.strptime(sync_form[column.db_name], '%Y-%m-%d')
                    continue
                asset_data[column.db_name] = str(sync_form[column.db_name])

        # Init new Asset and store it in the database
        asset: Asset = Asset(data=asset_data)
        asset_manager.create_asset(asset_type, asset)

        return redirect(f'/asset-type:{asset_type_id}')

    @staticmethod
    async def get_create_asset(asset_type_id: int):
        """Handle get requests to this route. TODO"""

        asset_type_manager: AAssetTypeManager = AssetTypeManager()

        asset_type: AssetType = asset_type_manager.get_one(
            asset_type_id, extend_columns=True)

        assets: Dict[int, List[Asset]] = {}

        # If the asset type of this asset defines columns
        # that contain other assets, we need to load them
        # so we can present them to the user.

        if field_asset_ids := \
                [column.asset_type_id for column in asset_type.columns
                 if column.asset_type_id]:

            # Create only one asset_manager, if required
            asset_manager: AAssetManager = AssetManager()

            for asset_id in field_asset_ids:
                asset_t = asset_type_manager.get_one(asset_id)
                result = asset_manager.get_all(asset_t)
                assets[asset_t.asset_type_id] = result  # [asset.asset_id for asset in results]

        if AssetServer.get().json_response:
            return jsonify({
                'asset_type': asset_type.as_dict(),
                'assets': {key: [a.as_dict() for a in value] for key, value in assets.items()}
            })
        return await render_template("create-asset.html", asset_type=asset_type, assets=assets)

    @staticmethod
    async def get_one_asset(asset_type_id: int, asset_id: int):
        """Handle get requests to get-asset."""

        asset_type_manager: AAssetTypeManager = AssetTypeManager()
        asset_manager: AAssetManager = AssetManager()

        asset_type: AssetType = asset_type_manager.get_one(asset_type_id)
        asset: Asset = asset_manager.get_one(asset_id, asset_type)

        asset_page_layout: AssetPageLayout = AssetPageLayout(
            layout=[[]],
            asset_type=asset_type,
            layout_id=0,
            items_url=None,
            asset=asset,
            field_mappings={
                'header': 'name'
            }
        )

        if AssetServer.get().json_response:
            return jsonify({
                'asset_page_layout': asset_page_layout.as_dict()
            })
        return await render_template("asset.html", asset_page_layout=asset_page_layout)

    @staticmethod
    def delete_asset(asset_type_id: int, asset_id: int):
        """Handle requests """

        asset_type_manager: AAssetTypeManager = AssetTypeManager()
        asset_manager: AAssetManager = AssetManager()

        asset_type = asset_type_manager.get_one(
            int(asset_type_id), extend_columns=False)
        asset = asset_manager.get_one(asset_id, asset_type)
        asset_manager.delete_asset(asset_type, asset)
        return redirect(f'/asset-type:{asset_type_id}')
