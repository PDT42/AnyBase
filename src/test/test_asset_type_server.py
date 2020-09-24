"""
:Author: PDT
:Since: 2020/09/02

These are tests for the AssetTypeServer.
"""
import json
from datetime import datetime
from time import sleep
from typing import List

import aiounittest
import requests
from sseclient import SSEClient

from asset_type import AssetType
from asset_type.asset_type_manager import AssetTypeManager
from database import Column
from database import DataType
from database import DataTypes
from database.db_connection import DbConnection
from database.sqlite_connection import SqliteConnection
from plugins import PluginRegister


class TestAssetTypeServer(aiounittest.AsyncTestCase):

    def setUp(self) -> None:
        """Set up."""

        self.BASE_URL: str = 'http://localhost:4200'

        # Making sure the test server is running
        request = requests.get(self.BASE_URL)
        if not request.status_code == 200:
            raise Exception(f"{self.BASE_URL} could not be reached." +
                            f" Make sure the test server is running!")

        # print(f"Tempdir used in this tests: {self.tempdir}")

        self.db_connection: DbConnection = SqliteConnection.get()
        self.asset_type_manager: AssetTypeManager = AssetTypeManager()

        self.asset_type = AssetType(
            'Media Article',
            [
                Column('Name', 'name', DataTypes.VARCHAR.value, required=True),
                Column('ISBN', 'isbn', DataTypes.VARCHAR.value, required=True)
            ])

    def tearDown(self) -> None:
        """Tear down."""
        pass

    async def _post_create_asset_type(self):
        """Send request to 'post-create-asset-type'."""

        if self.asset_type_manager.check_asset_type_exists("Media Article"):
            return

        request_url: str = f'{self.BASE_URL}/asset-type/create'
        request_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        request_body = "assetName=Media Article" + \
                       "&column-name-0=Title" \
                       "&column-data-type-0=VARCHAR" \
                       "&column-required-0=checkboxTrue" \
                       "&column-name-1=ISBN" \
                       "&column-data-type-1=VARCHAR" \
                       "&column-required-1=checkboxTrue"

        request = requests.post(url=request_url, headers=request_headers, data=request_body)
        self.assertEqual(request.status_code, 200)

    async def test_stream_asset_type_data(self):
        """Test 'stream-asset-type-data'."""

        request_url: str = f'{self.BASE_URL}/asset-types'
        request_headers = {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Transfer-Encoding': 'chunked',
        }

        sse_client = SSEClient(request_url)

        for event in sse_client:
            print(event)

        # async with aiohttp.ClientSession() as session:
        #     async with session.get(request_url) as response:
        #
        #         self.assertEqual(response.status, 200)
        #
        #         while True:
        #             response_text = await response.content.read()
        #             if not response_text:
        #                 break
        #         print(response_text)

    async def test_get_create_asset_types(self):
        """Test 'get-configuration'."""

        create_type_url: str = f'{self.BASE_URL}/asset-type/create'
        request = requests.get(create_type_url)

        self.assertEqual(request.status_code, 200)

    async def test_post_create_asset_type(self):
        """Test 'post-create-asset'."""

        await self._post_create_asset_type()

        asset_type: AssetType = self.asset_type_manager.get_one_by_id(1)

        self.assertEqual(asset_type.asset_name, 'Media Article')
        self.assertEqual(asset_type.columns[0].name, 'Title')
        self.assertEqual(asset_type.columns[1].name, 'ISBN')

        sleep(1)

    async def test_get_one_asset_type(self):
        """Test GET 'asset-type'."""

        await self._post_create_asset_type()

        db_asset_type: AssetType = self.asset_type_manager.get_one_by_id(1)

        self.assertEqual(db_asset_type.asset_name, 'Media Article')
        self.assertEqual(db_asset_type.columns[0].name, 'Title')
        self.assertEqual(db_asset_type.columns[1].name, 'ISBN')

        request_url: str = f'{self.BASE_URL}/asset-type:{db_asset_type.asset_type_id}'
        request = requests.get(request_url)
        sleep(1)

        self.assertEqual(request.status_code, 200)

        json_content = json.loads(request.content)

        asset_type_dict = json_content['asset_type']

        columns: List[Column] = []
        for column_dict in asset_type_dict['columns']:
            column: Column = Column(**column_dict)
            column.datatype = DataType(**column_dict['datatype'])
            columns.append(column)

        request_asset_type: AssetType = AssetType(
            asset_name=asset_type_dict['asset_name'],
            asset_table_name=asset_type_dict['asset_table_name'],
            asset_type_id=asset_type_dict['asset_type_id'],
            created=datetime.fromtimestamp(asset_type_dict['created']),
            updated=datetime.fromtimestamp(asset_type_dict['updated']),
            owner_id=asset_type_dict['owner_id'],
            super_type=asset_type_dict['super_type'],
            columns=columns)

        available_plugins = [
            PluginRegister[pt['id'].upper().replace('-', '_')].value
            for pt in json_content['available_plugins']
        ]

        self.assertEqual(request_asset_type, db_asset_type)

        sleep(1)
