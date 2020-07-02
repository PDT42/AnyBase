"""
:Author: PDT
:Since: 2020/07/02

These are exceptions for the asset package.
"""


class AssetTypeAlreadyExistsException(Exception):
    pass


class AssetTypeDoesNotExistException(Exception):
    pass