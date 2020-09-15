"""
:Author: PDT
:Since: 2020/09/02

These are tests for the AssetTypeServer.
"""

from datetime import datetime
from shutil import rmtree
from typing import Optional

import pytest
from quart import Quart

from asset_type import AssetType
from asset_type.asset_type_manager import AssetTypeManager
from database import Column, DataTypes
from database.db_connection import DbConnection
from asset_type.asset_type_server import AssetTypeServer
from test.test_util import init_test_db

db_connection: Optional[DbConnection] = None
tempdir = None


@pytest.fixture
def asset_type_manager():
    return AssetTypeManager()


def set_up() -> Quart:
    """Set up before tests."""

    global tempdir, db_connection

    tempdir, db_connection = init_test_db()
    # print(f"Tempdir used in this tests: {self.tempdir}")

    test_app: Quart = Quart(import_name='test_app')

    AssetTypeServer.get().register_routes(app=test_app)
    AssetTypeServer.json_response = True

    asset_type_manager = AssetTypeManager()

    created: datetime = datetime.now()
    media_article = AssetType(
        asset_name='Media Article',
        columns=[
            Column('Title', 'title', DataTypes.VARCHAR.value, required=True),
            Column('ISBN', 'isbn', DataTypes.VARCHAR.value, required=True, unique=True)
        ], created=created,
        updated=created
    )
    media_article = asset_type_manager \
        .create_asset_type(media_article)

    book = AssetType(
        asset_name='Book',
        columns=[
            Column('Number of Pages', 'number_of_pages', DataTypes.INTEGER.value)
        ], super_type=media_article.asset_type_id,
        created=created,
        updated=created
    )
    book = asset_type_manager \
        .create_asset_type(book)

    return test_app


def tear_down(self) -> None:
    """Clean up after each test."""

    global tempdir, db_connection

    db_connection.kill()
    rmtree(self.tempdir)


@pytest.mark.asyncio
async def test_get_list_asset_types():
    """Test the route 'list-asset-type'."""

    test_app = set_up()

    with test_app.test_client() as test_client:
        get_list_request = await test_client.get('/asset-type/list')
        assert (get_list_request.status_code == 200)
