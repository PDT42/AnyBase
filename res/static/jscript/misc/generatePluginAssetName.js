// Auth: PDT
// Since: 2020/12/05
//
// This script contains the function ``generatePluginAssetName``.

function generatePluginAssetName(plugin_name, asset_type_id, asset_id) {

    let plugin_asset_name = plugin_name.toLowerCase().replace('-', '_')

    plugin_asset_name += ('_at' + asset_type_id.toString())

    if (asset_id > 0) {
        plugin_asset_name += ('_a' + asset_id.toString())
    }

    return plugin_asset_name
}