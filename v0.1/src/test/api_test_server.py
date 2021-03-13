"""
:Author: PDT
:Since: 2020/09/16

This module exists to contain a test server for API tests.
"""

from threading import Thread

from quart import Quart

from asset.asset_server import AssetServer
from asset_type.asset_type_server import AssetTypeServer
from misc.common_server import CommonServer
from config import Config
from test.test_util import init_test_db

# Getting config values
# ---------------------

Config.get().change_path('U:/projects/anybase_modular_management/res/config.ini')
template_folder = Config.get().read('frontend', 'template_folder', '/res/templates')
static_folder = Config.get().read('frontend', 'static_folder', 'res/static')

# Creating Quart Application
# --------------------------
app = Quart(
    import_name=__name__,
    template_folder=template_folder,
    static_url_path='/static',
    static_folder=static_folder
)

app.secret_key = "SomeSecret"

# Initializing redis connection
# -----------------------------
# strict_redis = redis.StrictRedis(host='localhost', port=6379)
# strict_redis.execute_command('FLUSHDB')

# Initialization
# --------------

# Database
# ~~~~~~~~

tempdir, db_connection = init_test_db()

print(f"\nUsing temporary directory: {tempdir}\n")

# Adding Routes provided by the server to app
# -------------------------------------------

# Test Server Routes
# ~~~~~~~~~~~~~~~~~~
CommonServer.get().register_routes(app=app)
AssetServer.get().register_routes(app=app)
AssetTypeServer.get().register_routes(app=app)

AssetTypeServer.get().JSON_RESPONSE = True

if __name__ == '__main__':
    app.run('localhost', port=4200, debug=True)


def th_run_app():
    thread = Thread(
        target=app.run,
        args=('localhost',),
        kwargs={
            'port': 4200,
            'debug': True
        })
    thread.daemon = True
    thread.start()

    return app, thread, tempdir
