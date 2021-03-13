"""
:Author: PDT
:Since: 2020/10/03

This is a manager extension for the AssetTypeManager, that handles ``Bookables``.
"""

from asset_type import AssetType
from asset_type.asset_type_manager import AssetTypeManager
from database import Column
from database import DataTypes
from exceptions.common import IllegalStateException


class BookableManager(AssetTypeManager):
    """This is the BookableManager."""

    def __init__(self):
        """Create a new ``BookableManager``."""
        super().__init__()

    def init_bookable_type(self, asset_type: AssetType):
        """Make an AssetType a bookable AssetType if it is not already."""

        if asset_type.bookable is True:
            raise IllegalStateException("Can't init AssetType as bookable if it already is!")

        # Creating Booking Type for asset_type.

        booking_type: AssetType = AssetType(
            asset_name=f'abbookings_{asset_type.asset_name}'.replace(' ', '_').lower(),
            columns=[Column('Booked Asset Id', 'booked_asset_id', DataTypes.INTEGER.value, required=True)],
            owner_id=asset_type.asset_type_id)

        # NOTE: The BookingType extends the BookingType of its owners
        # NOTE: super type, if its owners supertype is bookable.

        if (super_type_id := asset_type.super_type) > 0:

            super_type: AssetType = self.get_one_by_id(super_type_id)

            if super_type.bookable is True:
                booking_type.super_type = super_type.booking_type_id

        # The "super most" booking type must define
        # the booking type good stuff shizzle.
        if not booking_type.super_type > 0:
            booking_type.columns.extend([
                Column('From', 'from_time', DataTypes.DATETIME.value, required=True),
                Column('Until', 'until_time', DataTypes.DATETIME.value, required=True),
                Column('Booker Type Id', 'booker_type_id', DataTypes.INTEGER.value, required=True),
                Column('Booker Id', 'booker_id', DataTypes.INTEGER.value, required=True),
            ])

        booking_type = self.create_asset_type(booking_type)

        # Updating asset_type to be bookable
        asset_type.booking_type_id = booking_type.asset_type_id
        asset_type.bookable = True

        return self.update_asset_type(asset_type, extend_columns=False)
