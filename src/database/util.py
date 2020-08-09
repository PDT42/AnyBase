"""
:Author: PDT
:Since: 2020/08/02

These are utility functions used in the database package.
"""


def convert_asset_to_dbtype(asset):
    return int(asset) if isinstance(asset, (int, str)) else asset.asset_id


def convert_assetlist_to_dbtype(assetlist):
    # TODO: Think about removing this, this should never be the case
    if all(isinstance(a, int) for a in assetlist):
        return ';'.join([str(a) for a in assetlist])
    return ';'.join([str(a.asset_id) for a in assetlist])
