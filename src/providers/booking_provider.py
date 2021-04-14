# class BookingProvider():
#     """This is the ``BookingProvider``."""
#
#     def get_bookable_types(self):
#         """Get a list of bookable types."""
#
#         bookable_filter = ['"booking_type_id" > 0']
#         bookable_types: List[AssetType] = self.asset_type_manager \
#             .get_all_filtered(and_filters=bookable_filter)
#         return bookable_types
#
#     def get_base_bookings_for_type(self, asset_type) -> List[Asset]:
#         """Get all the bookings that exist for an ``asset_type``."""
#
#         if isinstance(asset_type, int):
#             asset_type = self.asset_type_manager.get_one_by_id(asset_type)
#
#         # Making sure the supplied asset_type is bookable
#         if not asset_type.bookable or asset_type.booking_type_id < 0:
#             raise IllegalStateException(
#                 "Can't get the bookings of an asset type that is not bookable!")
#
#         bookings_type: AssetType = self.asset_type_manager \
#             .get_one_by_id(asset_type.booking_type_id)
#         bookings: List[Asset] = self.asset_manager.get_all(bookings_type)
#         return bookings
#
#     def get_bookings_for_type(self, asset_type, depth: int = 0) \
#             -> MutableMapping[AssetType, List[Asset]]:
#         """Get a typed map of bookings for an ``asset_type``."""

#
#         if isinstance(asset_type, int):
#             asset_type = self.asset_type_manager.get_one_by_id(asset_type)
#
#         # Making sure the supplied asset_type is bookable
#         if not asset_type.bookable or asset_type.booking_type_id < 0:
#             raise IllegalStateException(
#                 "Can't get the bookings of an asset type that is not bookable!")
#
#         bookings_type: AssetType = self.asset_type_manager \
#             .get_one_by_id(asset_type.booking_type_id)
#
#         # Getting the children of the bookable type
#         type_children: List[AssetType] = self.asset_type_manager \
#             .get_type_children(bookings_type, ignore_slaves=False)
#
#         typed_bookings: MutableMapping[AssetType, List[Asset]] = {}
#
#         # For each of the child types create a key in the bookings map.
#         for child_type in type_children:
#             typed_bookings[child_type] = self.asset_manager.get_all(child_type)
#
#             # Get children's children if depth is greater zero.
#             if depth > 0:
#                 typed_bookings.update(self.get_bookings_for_type(child_type, depth - 1))
#         return typed_bookings
#
#     def get_base_bookings_asset(
#             self, asset_type: Union[AssetType, int],
#             asset: Union[Asset, int]
#     ) -> List[Asset]:
#         """Get the booking items on record for ``asset_type``"""
#
#         if isinstance(asset_type, int):
#             asset_type = self.asset_type_manager.get_one_by_id(asset_type)
#         if isinstance(asset, int):
#             asset = self.asset_manager.get_one(asset, asset_type)
#
#         # Making sure the supplied asset_type is bookable
#         if not asset_type.bookable or asset_type.booking_type_id < 0:
#             raise IllegalStateException(
#                 "Can't get the bookings of an asset type that is not bookable!")
#
#         bookings_type: AssetType = self.asset_type_manager\
#             .get_one_by_id(asset_type.booking_type_id)
#
#         filters: List[str] = [f'booked_asset_id = {asset.asset_id}']
#
#         bookings: List[Asset] = self.asset_manager\
#             .get_all_filtered(bookings_type, and_filters=filters)
#         return bookings
#
#     def get_bookings_asset(
#             self, asset_type: Union[AssetType, int],
#             asset: Union[Asset, int], depth: int = 0
#     ) -> MutableMapping[AssetType, List[Asset]]:
#         """Get a typed map of bookings for an ``asset``."""
#
#         if isinstance(asset_type, int):
#             asset_type = self.asset_type_manager.get_one_by_id(asset_type)
#         if isinstance(asset, int):
#             asset = self.asset_manager.get_one(asset, asset_type)
#
#         # Making sure the supplied asset_type is bookable
#         if not asset_type.bookable or asset_type.booking_type_id < 0:
#             raise IllegalStateException(
#                 "Can't get the bookings of an asset type that is not bookable!")
#
#         bookings_type: AssetType = self.asset_type_manager \
#             .get_one_by_id(asset_type.booking_type_id)
#
#         # Getting the children of the bookable type
#         type_children: List[AssetType] = self.asset_type_manager \
#             .get_type_children(bookings_type, depth=depth, ignore_slaves=False)
#         typed_bookings: MutableMapping[AssetType, List[Asset]] = {}
#
#         filters: List[str] = [f"booked_asset_id = {asset.asset_id}"]
#
#         for child_type in type_children:
#             typed_bookings[child_type] = self.asset_manager\
#                 .get_all_filtered(child_type, and_filters=filters)
#
#         return typed_bookings
