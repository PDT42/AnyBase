"""
:Author: PDT
:Since: 2020/05/24

This is the main application of AnyBase. Run this.
"""
from quart import Quart

from config import Config
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from server import favicon, index
from server.asset_server import AssetServer
from server.asset_type_server import AssetTypeServer

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
db_path = Config.get().read('local database', 'path')
db_connection: DbConnection = SqliteConnection.get(db_path)

# Creating Servers
# ~~~~~~~~~~~~~~~~
asset_type_server = AssetTypeServer.get()
asset_server = AssetServer.get()

# Adding Routes provided in server to app
# ---------------------------------------

# General Routes
# ~~~~~~~~~~~~~~
app.add_url_rule('/', 'index', index, methods=['GET'])
app.add_url_rule('/favicon', 'favicon', favicon, methods=['GET'])

# AssetType Routes
# ~~~~~~~~~~~~~~~~
app.add_url_rule(
    '/asset-type/create',
    'get-create-asset-type',
    asset_type_server.get_create_asset_type,
    methods=['GET']
)

app.add_url_rule(
    '/asset-type/create',
    'post-create-asset-type',
    asset_type_server.post_create_asset_type,
    methods=['POST']
)

app.add_url_rule(
    '/asset-type/list',
    'list-asset-types',
    asset_type_server.get_list_asset_types,
    methods=['GET']
)

app.add_url_rule(
    '/asset-type/config',
    'configure-asset-types',
    asset_type_server.get_configure_asset_types,
    methods=['GET']
)

app.add_url_rule(
    '/asset-type/<int:asset_type_id>',
    'asset-type',
    asset_type_server.get_one_asset_type,
    methods=['GET']
)

app.add_url_rule(
    '/asset-type/<int:asset_type_id>/delete',
    'delete-asset-type',
    asset_type_server.delete_asset_type,
    methods=['POST']
)

# Asset Routes
# ~~~~~~~~~~~~
app.add_url_rule(
    '/asset-type/<int:asset_type_id>/create-asset',
    'get-create-asset',
    asset_server.get_create_asset,
    methods=['GET']
)

app.add_url_rule(
    '/asset-type/<int:asset_type_id>/create-asset',
    'post-create-asset',
    asset_server.post_create_asset,
    methods=['POST']
)

app.add_url_rule(
    '/asset-type/<int:asset_type_id>/stream-items',
    'stream-asset-data',
    asset_server.stream_asset_data,
    methods=['GET']
)

app.add_url_rule(
    '/asset-type/<int:asset_type_id>/<int:asset_id>',
    'get-asset',
    asset_server.get_one_asset,
    methods=['GET']
)

if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)
