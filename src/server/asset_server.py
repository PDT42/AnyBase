"""
:Author: PDT
:Since: 2020/06/16

These are the routes for the ``AssetTypeManager``.
"""

import json
from concurrent.futures._base import ALL_COMPLETED, wait
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from typing import Dict, List

from flask import redirect, render_template, request
from flask_sse import sse

from asset import Asset
from asset.abstract_asset_manager import AAssetManager
from asset.asset_manager import AssetManager
from asset.asset_type_manager import AssetTypeManager
from config import Config
from database import DataTypes

DB_BATCH_SIZE = int(Config.get().read("local database", "batch_size", 1000))


def _th_request_asset_data(th_offset, asset_type, depth):
    """Load a batch of assets."""

    print(f"Running request task for offset: {th_offset}")  # TODO: Remove

    asset_manager: AAssetManager = AssetManager()
    return asset_manager.get_batch(
        asset_type=asset_type,
        offset=th_offset,
        limit=th_offset + DB_BATCH_SIZE,
        depth=depth
    )


def request_asset_data(asset_type_id: int, depth: int = 0):
    asset_type = AssetTypeManager().get_one(asset_type_id)
    asset_count = AssetManager().count(asset_type)

    with ThreadPoolExecutor() as exeqt:
        futures = {}

        offset = 0
        while offset < asset_count:
            # Creating task in a separate thread
            future = exeqt.submit(_th_request_asset_data, offset, asset_type, depth)

            # Updating iteration information
            futures[future] = offset
            offset += DB_BATCH_SIZE

        # Wait until there is nothing left to wait for
        while len(futures) > 0:
            done, not_done = wait(futures, timeout=1, return_when=ALL_COMPLETED)

            for future in done:
                result = future.result()
                sse.publish(json.dumps([asset.to_json() for asset in result]))
                futures.pop(future)
    return 0


def post_create_asset(asset_type_id: int):
    """This is a FlaskAppRoute that lets you create an ``Asset``."""

    asset_type_manager = AssetTypeManager()
    asset_type = asset_type_manager.get_one(asset_type_id)

    asset_manager = AssetManager()

    asset_data = {}

    for column in asset_type.columns:

        r = request  # TODO: remove

        # Column is missing in form but is required
        if column.required and column.db_name not in request.form.keys():
            return 1  # TODO: Validation

        # Column is missing and isn't required
        elif not column.required and column.db_name not in request.form.keys():
            continue

        # Column is present
        else:
            # TODO: Validate input
            if column.datatype is DataTypes.DATETIME.value:
                asset_data[column.db_name] = datetime.strptime(request.form[column.db_name], '%Y-%m-%dT%H:%M')
                continue
            if column.datatype is DataTypes.DATE.value:
                asset_data[column.db_name] = datetime.strptime(request.form[column.db_name], '%Y-%m-%d')
                continue
            asset_data[column.db_name] = str(request.form[column.db_name])

    asset = Asset(asset_id=None, data=asset_data)
    asset_manager.create_asset(asset_type, asset)

    return redirect(f'/asset-type/{asset_type_id}')


def get_create_asset(asset_type_id: int):
    """Handle get requests to this route. TODO"""

    asset_type_manager = AssetTypeManager()
    asset_type = asset_type_manager.get_one(asset_type_id)

    field_asset_ids = [column.asset_type_id for column in asset_type.columns if column.asset_type_id]
    assets: Dict[int, List[Asset]] = {}

    if field_asset_ids:

        asset_manager: AAssetManager = AssetManager()

        for asset_id in field_asset_ids:
            asset_t = asset_type_manager.get_one(asset_id)
            result = asset_manager.get_all(asset_t)
            assets[asset_t.asset_type_id] = result  # [asset.asset_id for asset in results]

    return render_template("create-asset.html", asset_type=asset_type, assets=assets)
