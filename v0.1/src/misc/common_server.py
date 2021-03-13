"""
:Author: PDT
:Since: 2020/06/16

This is the common server, used for index n'stuff.
"""
from collections import Mapping
from typing import List

from quart import jsonify
from quart import redirect
from quart import render_template
from quart import url_for

from asset_type.abstract_asset_type_manager import AAssetTypeManager
from asset_type.asset_type_manager import AssetTypeManager
from asset_type.asset_type_server import AssetTypeServer
from config import Config
from exceptions.server import ServerAlreadyInitializedError


class CommonServer:
    """This is the ``CommonServer`` it holds the common (...) routes,
    that don't really fit into one of the other servers."""

    _instance = None
    _initialized = False
    json_response = None

    @staticmethod
    def get():
        """Get the instance of this singleton."""

        if not CommonServer._instance:
            CommonServer._instance = CommonServer()
        return CommonServer._instance

    def __init__(self):
        """Create a new AssetTypeServer."""

        self.json_response = Config.get().read(
            'frontend', 'JSON_RESPONSE', False) in ["True", "true", 1]

    @staticmethod
    def register_routes(app):
        """Register the routes of this server in the ``app``."""

        if CommonServer.get()._initialized:
            raise ServerAlreadyInitializedError("AssetTypeServer already initialized!")

        app.add_url_rule('/', 'index', CommonServer.index, methods=['GET'])
        app.add_url_rule('/favicon', 'favicon', CommonServer.favicon, methods=['GET'])

        app.add_url_rule(
            '/asset-type/list',
            'list-asset-types',
            CommonServer.get_list_asset_types,
            methods=['GET']
        )

        app.add_url_rule(
            '/asset-type/config',
            'configure-asset-types',
            CommonServer.get_configure_asset_types,
            methods=['GET']
        )

        CommonServer.get()._initialized = True

    @staticmethod
    async def index():
        """Return home page_layout."""
        return await render_template("base.html")

    @staticmethod
    async def get_list_asset_types():
        """Handle get requests to ``asset-types``."""

        # TODO: Deprecated this. This should be replaced
        # TODO: using a PageLayout and stream_asset_type_data

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

        # TODO: Deprecate this. This should be replaced
        # TODO: using a PageLayout and stream_asset_type_data

        asset_type_manager = AssetTypeManager()
        asset_types: List[Mapping] = [at.as_dict() for at in asset_type_manager.get_all()]

        return await render_template("configuration.html", asset_types=asset_types)

    @staticmethod
    async def favicon():
        """Return favicon."""
        return redirect(url_for('static', filename='../../res/static/images/favicon.ico'))
