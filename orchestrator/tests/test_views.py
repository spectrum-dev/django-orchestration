import json
import responses

from django.test import TestCase

from authentication.factories import set_up_authentication
from orchestrator.tests.data.test_data_validation import (
    SINGLE_FULL_FLOW_INVALID,
    SINGLE_FULL_FLOW_VALID,
    FULL_FLOW_WITH_TWO_BACKTEST_BLOCKS,
)


class MetadataViewTest(TestCase):
    def test_ok(self):
        auth = set_up_authentication()
        block_type = "DATA_BLOCK"
        block_id = 1

        response = self.client.get(
            f"/orchestration/{block_type}/{block_id}/metadata",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(),
            {
                "blockName": "US Stock Data",
                "blockType": "DATA_BLOCK",
                "blockId": 1,
                "inputs": [
                    {
                        "fieldData": {"base": "/equityName?name=", "method": "GET"},
                        "fieldName": "Equity Name",
                        "fieldType": "search",
                        "fieldVariableName": "equity_name",
                    },
                    {
                        "fieldData": {
                            "data": [
                                "1min",
                                "5min",
                                "15min",
                                "30min",
                                "60min",
                                "1day",
                                "1week",
                                "1month",
                            ]
                        },
                        "fieldName": "Candlesticks",
                        "fieldType": "dropdown",
                        "fieldVariableName": "candlestick",
                    },
                    {
                        "fieldName": "Date Range",
                        "fieldType": "date_range",
                        "fieldVariableNames": ["start_date", "end_date"],
                    },
                ],
                "validation": {
                    "input": {"required": [], "allowed_blocks": []},
                    "output": [{"number": 1, "blockType": "DATA_BLOCK"}],
                },
                "outputInterface": {
                    "interface": ["open", "high", "low", "close", "volume"]
                },
            },
        )

    def test_block_type_dne(self):
        auth = set_up_authentication()
        block_type = "DATA_BLOCK_DNE"
        block_id = 1

        response = self.client.get(
            f"/orchestration/{block_type}/{block_id}/metadata",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(), {"error": "Block Type - ID Pair does not exist"}
        )

    def test_block_id_dne(self):
        auth = set_up_authentication()
        block_type = "DATA_BLOCK"
        block_id = -1  # This block ID DNE

        response = self.client.get(
            f"/orchestration/{block_type}/{block_id}/metadata",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(), {"error": "Block Type - ID Pair does not exist"}
        )


class ProxyBlockActionViewTest(TestCase):
    @responses.activate
    def test_ok(self):
        auth = set_up_authentication()
        block_type = "DATA_BLOCK"
        block_id = 1
        action_name = "dataType"

        responses.add(
            responses.GET,
            "http://block-monolith:8000/DATA_BLOCK/1/dataType",
            json={
                "response": ["intraday", "daily_adjusted"],
            },
            status=200,
        )

        response = self.client.get(
            f"/orchestration/{block_type}/{block_id}/{action_name}",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(), {"response": ["intraday", "daily_adjusted"]}
        )

    @responses.activate
    def test_name_query_param_ok(self):
        auth = set_up_authentication()
        block_type = "DATA_BLOCK"
        block_id = 1
        action_name = "equityName"

        responses.add(
            responses.GET,
            "http://block-monolith:8000/DATA_BLOCK/1/equityName?name=BA",
            json={
                "response": [
                    "BA",
                    "BAB",
                    "BA.LON",
                    "BABA",
                    "BA3.FRK",
                    "BAAPX",
                    "BABAF",
                    "BAAAAX",
                    "BABA34.SAO",
                    "BAAX39.SAO",
                ]
            },
            status=200,
        )

        response = self.client.get(
            f"/orchestration/{block_type}/{block_id}/{action_name}?name=BA",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    "BA",
                    "BAB",
                    "BA.LON",
                    "BABA",
                    "BA3.FRK",
                    "BAAPX",
                    "BABAF",
                    "BAAAAX",
                    "BABA34.SAO",
                    "BAAX39.SAO",
                ]
            },
        )

    @responses.activate
    def test_indicator_name_query_param_ok(self):
        auth = set_up_authentication()
        block_type = "COMPUTATIONAL_BLOCK"
        block_id = 1
        action_name = "indicatorField"

        responses.add(
            responses.GET,
            "http://block-monolith:8000/COMPUTATIONAL_BLOCK/1/indicatorField?indicatorName=MA",
            json={
                "response": [
                    {
                        "fieldName": "Lookback Period",
                        "fieldType": "input",
                        "fieldVariableName": "lookback_period",
                    },
                    {
                        "fieldName": "Lookback Unit",
                        "fieldType": "dropdown",
                        "fieldVariableName": "lookback_unit",
                        "fieldData": {"options": ["DATA_POINT"]},
                    },
                ]
            },
            status=200,
        )

        response = self.client.get(
            f"/orchestration/{block_type}/{block_id}/{action_name}?indicatorName=MA",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {
                        "fieldName": "Lookback Period",
                        "fieldType": "input",
                        "fieldVariableName": "lookback_period",
                    },
                    {
                        "fieldName": "Lookback Unit",
                        "fieldType": "dropdown",
                        "fieldVariableName": "lookback_unit",
                        "fieldData": {"options": ["DATA_POINT"]},
                    },
                ]
            },
        )

    @responses.activate
    def test_block_type_dne(self):
        auth = set_up_authentication()
        block_type = "DATA_BLOCK_DNE"
        block_id = 1
        action_name = "dataType"

        responses.add(
            responses.GET,
            "http://block-monolith:8000/DATA_BLOCK_DNE/1/dataType",
            json={"error": "Unhandled error"},
            status=404,
        )

        response = self.client.get(
            f"/orchestration/{block_type}/{block_id}/{action_name}",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(response.json(), {"error": "Unhandled error"})

    @responses.activate
    def test_block_id_dne(self):
        auth = set_up_authentication()
        block_type = "DATA_BLOCK"
        block_id = -1
        action_name = "dataType"

        responses.add(
            responses.GET,
            "http://block-monolith:8000/DATA_BLOCK/-1/dataType",
            json={"error": "Unhandled error"},
            status=404,
        )

        response = self.client.get(
            f"/orchestration/{block_type}/{block_id}/{action_name}",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(response.json(), {"error": "Unhandled error"})


class RunOverlays(TestCase):
    def test_two_streams_complete_overlap(self):
        auth = set_up_authentication()

        payload = {
            "base": [
                {
                    "open": 126.01,
                    "high": 126.01,
                    "low": 126.0,
                    "close": 126.01,
                    "volume": 2835.0,
                    "timestamp": "2021-06-04T20:00:00.000000000",
                },
                {
                    "open": 126.01,
                    "high": 126.01,
                    "low": 125.99,
                    "close": 126.01,
                    "volume": 788.0,
                    "timestamp": "2021-06-04T19:59:00.000000000",
                },
                {
                    "open": 126.0,
                    "high": 126.01,
                    "low": 126.0,
                    "close": 126.01,
                    "volume": 3693.0,
                    "timestamp": "2021-06-04T19:58:00.000000000",
                },
            ],
            "2": [
                {
                    "timestamp": "2021-06-04T20:00:00.000000000",
                    "value": 10.00,
                },
                {
                    "timestamp": "2021-06-04T19:59:00.000000000",
                    "value": 11.00,
                },
                {
                    "timestamp": "2021-06-04T19:58:00.000000000",
                    "value": 10.00,
                },
            ],
        }

        response = self.client.post(
            "/orchestration/overlay",
            json.dumps(payload),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {
                        "open": 126.01,
                        "high": 126.01,
                        "low": 126.0,
                        "close": 126.01,
                        "volume": 2835.0,
                        "2": 10.0,
                        "timestamp": "2021-06-04T20:00:00.000000000",
                    },
                    {
                        "open": 126.01,
                        "high": 126.01,
                        "low": 125.99,
                        "close": 126.01,
                        "volume": 788.0,
                        "2": 11.0,
                        "timestamp": "2021-06-04T19:59:00.000000000",
                    },
                    {
                        "open": 126.0,
                        "high": 126.01,
                        "low": 126.0,
                        "close": 126.01,
                        "volume": 3693.0,
                        "2": 10.0,
                        "timestamp": "2021-06-04T19:58:00.000000000",
                    },
                ]
            },
        )

    def test_two_streams_partial_overlap(self):
        auth = set_up_authentication()

        payload = {
            "base": [
                {
                    "open": 126.01,
                    "high": 126.01,
                    "low": 126.0,
                    "close": 126.01,
                    "volume": 2835.0,
                    "timestamp": "2021-06-04T20:00:00.000000000",
                },
                {
                    "open": 126.01,
                    "high": 126.01,
                    "low": 125.99,
                    "close": 126.01,
                    "volume": 788.0,
                    "timestamp": "2021-06-04T19:59:00.000000000",
                },
                {
                    "open": 126.0,
                    "high": 126.01,
                    "low": 126.0,
                    "close": 126.01,
                    "volume": 3693.0,
                    "timestamp": "2021-06-04T19:58:00.000000000",
                },
            ],
            "2": [
                {
                    "timestamp": "2021-06-04T20:00:00.000000000",
                    "value": 10.00,
                },
            ],
        }

        response = self.client.post(
            "/orchestration/overlay",
            json.dumps(payload),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": [
                    {
                        "open": 126.01,
                        "high": 126.01,
                        "low": 126.0,
                        "close": 126.01,
                        "volume": 2835.0,
                        "2": 10.0,
                        "timestamp": "2021-06-04T20:00:00.000000000",
                    },
                    {
                        "open": 126.01,
                        "high": 126.01,
                        "low": 125.99,
                        "close": 126.01,
                        "volume": 788.0,
                        "2": None,
                        "timestamp": "2021-06-04T19:59:00.000000000",
                    },
                    {
                        "open": 126.0,
                        "high": 126.01,
                        "low": 126.0,
                        "close": 126.01,
                        "volume": 3693.0,
                        "2": None,
                        "timestamp": "2021-06-04T19:58:00.000000000",
                    },
                ]
            },
        )
