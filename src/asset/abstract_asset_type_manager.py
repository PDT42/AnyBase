from abc import abstractmethod

from asset import AssetType


class AAssetTypeManager:
    """This is the abstract class for AssetTypeManagers."""

    @abstractmethod
    def create_asset_type(self, asset_type):
        """Create a new ``asset_type`` in the asset type registry."""
        pass

    @abstractmethod
    def delete_asset_type(self, asset_type):
        """Delete ``asset_type`` and all it's assets from the system."""
        pass

    @abstractmethod
    def update_asset_type(self, asset_type):
        """Update an ``asset_type`` in the database."""
        pass

    @abstractmethod
    def check_asset_type_exists(self, asset_type):
        """Check if ``asset_type`` with that name already exists."""
        pass

    @abstractmethod
    def get_all(self):
        """Get all ``AssetTypes`` registered in the database."""
        pass

    @abstractmethod
    def get_one(self, asset_type_id):
        """Get the ``AssetType`` with id ``asset_type_id``."""
        pass

    @staticmethod
    def generate_asset_table_name(asset_type: AssetType) -> str:
        """Generate an ``asset_table_name`` from the ``asset type``.
        This method is part of the abstract asset type manager, to
        ensure, that future implementations still support the same
        naming convention."""

        asset_name = asset_type.asset_name.replace(' ', '_').lower()
        return f"abasset_table_{asset_name}"
