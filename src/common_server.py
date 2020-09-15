"""
:Author: PDT
:Since: 2020/06/16

This is the common server, used for index n'stuff.
"""

from quart import redirect
from quart import render_template
from quart import url_for

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
            'frontend', 'json_response', False) in ["True", "true", 1]

    @staticmethod
    def register_routes(app):
        """Register the routes of this server in the ``app``."""

        if CommonServer.get()._initialized:
            raise ServerAlreadyInitializedError("AssetTypeServer already initialized!")

        app.add_url_rule('/', 'index', CommonServer.index, methods=['GET'])
        app.add_url_rule('/favicon', 'favicon', CommonServer.favicon, methods=['GET'])

        CommonServer.get()._initialized = True

    @staticmethod
    async def index():
        """Return home page_layout."""
        return await render_template("base.html")

    @staticmethod
    async def favicon():
        """Return favicon."""
        return redirect(url_for('static', filename='images/favicon.ico'))
