"""
:Author: PDT
:Since: 2020/09/26

This is the abstract implementation of an 'AppFeature'. Every
AppFeature is basically a server (just like plugin servers).
It serves the needs of the Feature in the frontend.
"""
from abc import abstractmethod

from asset.abstract_asset_manager import AAssetManager
from asset.asset_manager import AssetManager
from asset_type.abstract_asset_type_manager import AAssetTypeManager
from asset_type.asset_type_manager import AssetTypeManager


class AAppFeature:
    """This is an ``AppFeature``."""

    _instance: 'AAppFeature' = None

    @staticmethod
    def get() -> 'AAppFeature':
        """Get the instance of this singleton."""

        if not AAppFeature._instance:
            AAppFeature._instance = AAppFeature
        return AAppFeature._instance

    def __init__(self):
        """Create a new ``AppFeature``."""

        self.asset_type_manager: AAssetTypeManager = AssetTypeManager()
        self.asset_manager: AAssetManager = AssetManager()

    @staticmethod
    @abstractmethod
    def register_routes(app):
        """Register the routes of this feature in the ``app``."""
        pass


