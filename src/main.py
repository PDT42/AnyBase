"""
:Author: PDT
:Since: 2020/05/24
"""

from flask import Flask

import server

from server.asset_type_server import create_asset_type, asset_types, asset_type

from config import Config

# Getting config values
template_folder = Config.get().read('frontend', 'template_folder', '../res/templates')

# Creating Flask Application
app = Flask(__name__, template_folder=template_folder)

# Adding Routes provided in server to app
app.add_url_rule('/', 'index', server.index, methods=['GET'])
app.add_url_rule('/create-asset-type', 'create-asset-type', create_asset_type, methods=['GET', 'POST'])
app.add_url_rule('/asset-types', 'asset-types', asset_types, methods=['GET'])
app.add_url_rule('/asset-type/<int:asset_type_id>', 'asset-type', asset_type, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
