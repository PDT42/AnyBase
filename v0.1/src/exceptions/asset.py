"""
:Author: PDT
:Since: 2020/07/02

These are exceptions for the asset package.
"""


class AssetTypeAlreadyExistsException(Exception):
    pass


class AssetTypeDoesNotExistException(Exception):
    pass


class AssetTypeInconsistencyException(Exception):
    pass


class TooFewColumnsException(Exception):
    pass


class AssetTypeChangedException(Exception):
    pass


class AssetChangedException(Exception):
    pass


class SuperTypeDoesNotExistException(Exception):
    pass


class SuperAssetDoesNotExistException(Exception):
    pass


class MissingAssetError(Exception):
    pass


class ColumnNameTakenError(Exception):
    pass
