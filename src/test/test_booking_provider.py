"""
:Author: PDT
:Since: 2020/09/27

These are tests for the ``BookingProvider``.
"""
import unittest
from datetime import datetime
from shutil import rmtree
from typing import List
from typing import MutableMapping

from asset import Asset
from asset.abstract_asset_manager import AAssetManager
from asset.asset_manager import AssetManager
from asset_type import AssetType
from asset_type.abstract_asset_type_manager import AAssetTypeManager
from asset_type.asset_type_manager import AssetTypeManager
from database import Column
from database import DataTypes
from providers.booking_provider import BookingProvider
from test.test_util import init_test_db


class BookingProviderTest(unittest.TestCase):

    def setUp(self) -> None:
        """Setup before tests."""

        self.tempdir, self.db_connection = init_test_db()

        self.asset_type_manager: AAssetTypeManager = AssetTypeManager()
        self.asset_manager: AAssetManager = AssetManager()

        # Creating the Provider we want to test
        # Providers need to be handed the managers
        # they are supposed to used.
        self.booking_provider: BookingProvider = BookingProvider(self.asset_type_manager, self.asset_manager)

        # Creating a test data structure
        # °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
        self.media_article: AssetType = AssetType(
            asset_name='Media Article',
            columns=[
                Column('Title', 'title', DataTypes.VARCHAR.value, required=True),
                Column('ISBN', 'isbn', DataTypes.VARCHAR.value, required=True),
                Column('Release Date', 'release_date', DataTypes.DATE.value, required=True)])
        self.media_article = self.asset_type_manager.create_asset_type(self.media_article)

        self.book: AssetType = AssetType(
            asset_name='Book', super_type=self.media_article.asset_type_id, bookable=True,
            columns=[Column('Author', 'author', DataTypes.VARCHAR.value, required=True)])
        self.book = self.asset_type_manager.create_asset_type(self.book)

        self.book_bookings_type: AssetType = self.asset_type_manager \
            .get_one_by_id(self.book.booking_type_id)

        self.borrow: AssetType = AssetType(
            asset_name='Borrow', super_type=self.book.booking_type_id, is_slave=True,
            columns=[Column('Employee No', 'employee_no', DataTypes.INTEGER.value, required=True)])
        self.borrow = self.asset_type_manager.create_asset_type(self.borrow)

        self.member: AssetType = AssetType(
            asset_name='Member', columns=[
                Column('Name', 'name', DataTypes.VARCHAR.value, required=True),
                Column('Bookings', 'bookings', DataTypes.ASSETLIST.value, asset_type_id=self.borrow.asset_type_id)
            ])
        self.member = self.asset_type_manager.create_asset_type(self.member)

        self.borrow.owner_id = self.member.asset_type_id
        self.borrow = self.asset_type_manager.update_asset_type(self.borrow, extend_columns=False)

        # Creating some test data
        # °°°°°°°°°°°°°°°°°°°°°°°
        self.crossfit_bible: Asset = Asset(data={
            'title': 'CrossFit Bible',
            'isbn': '666-666-666-666',
            'release_date': datetime(1986, 4, 20).date(),
            'author': 'J.C.'})
        self.crossfit_bible = self.asset_manager \
            .create_asset(self.book, self.crossfit_bible)

        self.max_mustermann: Asset = Asset(data={
            'name': 'Max Mustermann'})
        self.max_mustermann = self.asset_manager \
            .create_asset(self.member, self.max_mustermann)

        self.max_borrow: Asset = Asset(data={
            'from_time': datetime(2020, 4, 20),
            'until_time': datetime(2020, 6, 20),
            'booker_type_id': self.member.asset_type_id,
            'booker_id': self.max_mustermann.asset_id,
            'booked_asset_id': self.crossfit_bible.asset_id,
            'employee_no': 42})
        self.max_borrow = self.asset_manager \
            .create_asset(self.borrow, self.max_borrow)

        self.max_mustermann.data['bookings'] = [self.max_borrow]
        self.max_mustermann = self.asset_manager.update_asset(self.member, self.max_mustermann)

        # Checking if all went to plan
        # °°°°°°°°°°°°°°°°°°°°°°°°°°°°
        self.assertIsNotNone(self.crossfit_bible)

    def tearDown(self):
        """Clean up after tests."""
        self.db_connection.kill()
        rmtree(self.tempdir)

    def test_get_bookable_types(self):
        """Test ``get_bookable_types`` function of ``BookingProvider``."""

        bookable_types: List[AssetType] = self.booking_provider.get_bookable_types()
        self.assertEqual(bookable_types, [self.book])

    def test_get_base_bookings_for_type(self):
        """Test ``get_base_bookings_for_type`` function of ``BookingProvider``."""

        bookings: List[Asset] = self.booking_provider.get_base_bookings_for_type(self.book)
        cheated_bookings = self.asset_manager.get_all(self.book_bookings_type)
        self.assertEqual(bookings, cheated_bookings)

    def test_get_bookings_for_type(self):
        """Test ``get_bookings_for_type`` function of ``BookingProvider``."""

        typed_bookings: MutableMapping[AssetType, List[Asset]] = self.booking_provider \
            .get_bookings_for_type(self.book)
        self.assertEqual(typed_bookings, {self.borrow: [self.max_borrow]})

    def test_get_base_bookings_asset(self):
        """Test ``get_base_bookings_asset`` function of ``BookingProvider``."""

        bookings: List[Asset] = self.booking_provider \
            .get_base_bookings_asset(self.book, self.crossfit_bible)
        cheated_bookings = self.asset_manager.get_all(self.book_bookings_type)
        self.assertEqual(bookings, cheated_bookings)

    def test_get_bookings_asset(self):
        """Test ``get_bookings_asset`` function of ``BookingProvider``."""

        typed_bookings: MutableMapping[AssetType, List[Asset]] = self.booking_provider \
            .get_bookings_asset(self.book, self.crossfit_bible)
        self.assertEqual(typed_bookings, {self.borrow: [self.max_borrow]})
