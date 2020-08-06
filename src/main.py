"""
:Author: PDT
:Since: 2020/05/24
"""

from flask import Flask

from config import Config
from server import configuration, index
from server.asset_server import create_asset
from server.asset_type_server import AssetTypeServer

# Getting config values
# ---------------------
template_folder = Config.get().read('frontend', 'template_folder', '/res/templates')

# Creating Flask Application
# --------------------------
app = Flask(__name__, template_folder=template_folder)

# Creating Servers
# ----------------
asset_type_server = AssetTypeServer.get()

# Adding Routes provided in server to app
# ---------------------------------------

# General Routes
# ~~~~~~~~~~~~~~
app.add_url_rule('/', 'index', index, methods=['GET'])
app.add_url_rule('/configuration', 'configuration', configuration, methods=['GET'])

# AssetType Routes
# ~~~~~~~~~~~~~~~~
app.add_url_rule(
    '/asset-type/create',
    'create-asset-type',
    asset_type_server.create_asset_type,
    methods=['GET', 'POST']
)
app.add_url_rule(
    '/asset-types',
    'asset-types',
    asset_type_server.get_all_asset_types,
    methods=['GET']
)
app.add_url_rule(
    '/asset-type/<int:asset_type_id>',
    'asset-type',
    asset_type_server.get_one_asset_type,
    methods=['GET']
)
app.add_url_rule(
    '/asset-type/<int:asset_type_id>',
    'delete-asset-type',
    asset_type_server.delete_asset_type,
    methods=['POST']
)

# Asset Routes
# ~~~~~~~~~~~~
app.add_url_rule('/asset-type/<int:asset_type_id>/create-asset', 'create-asset', create_asset, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)
