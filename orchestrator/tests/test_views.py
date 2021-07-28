import json
import responses

from django.test import TestCase

from authentication.factories import set_up_authentication
from orchestrator.tests.data.test_data_validation import (
    SINGLE_FULL_FLOW_INVALID,
    SINGLE_FULL_FLOW_VALID,
)


class AllMetadataViewTest(TestCase):
    def test_ok(self):
        auth = set_up_authentication()
        response = self.client.get(
            "/orchestration/metadata",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": {
                    "DATA_BLOCK": {
                        "1": {
                            "blockName": "US Stock Data",
                            "blockMetadata": "/orchestration/DATA_BLOCK/1/",
                        },
                        "2": {
                            "blockName": "Crypto Data",
                            "blockMetadata": "/orchestration/DATA_BLOCK/2/",
                        },
                    },
                    "COMPUTATIONAL_BLOCK": {
                        "1": {
                            "blockName": "Technical Analysis",
                            "blockMetadata": "/orchestration/COMPUTATIONAL_BLOCK/1/",
                        }
                    },
                    "SIGNAL_BLOCK": {
                        "1": {
                            "blockName": "Event",
                            "blockMetadata": "/orchestration/SIGNAL_BLOCK/1/",
                        },
                        "2": {
                            "blockName": "Saddle",
                            "blockMetadata": "/orchestration/SIGNAL_BLOCK/2/",
                        },
                    },
                    "STRATEGY_BLOCK": {
                        "1": {
                            "blockName": "Backtest",
                            "blockMetadata": "/orchestration/STRATEGY_BLOCK/1/",
                        }
                    },
                }
            },
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
                        "fieldData": {"base": "/candlestick", "method": "GET"},
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


class ValidateFlowTest(TestCase):
    def test_single_edge_invalid(self):
        request_payload = {
            "nodeList": {
                "1": {
                    "blockType": "DATA_BLOCK",
                    "blockId": 1,
                    "equity_name": {"value": "AAPL", "options": []},
                    "data_type": {
                        "value": "intraday",
                        "options": ["intraday", "daily_adjusted"],
                    },
                    "interval": {"value": "1min", "options": ["1min"]},
                    "outputsize": {"value": "compact", "options": ["compact", "full"]},
                    "start_date": {"value": "2021-06-21 19:58:00"},
                    "end_date": {"value": "2021-06-21 20:00:00"},
                },
                "4": {
                    "blockType": "SIGNAL_BLOCK",
                    "blockId": 1,
                    "event_type": {"value": "INTERSECT"},
                    "event_action": {"value": "BUY"},
                },
            },
            "edgeList": [
                {
                    "source": "1",
                    "sourceHandle": "output_id888",
                    "target": "4",
                    "targetHandle": "input_id891",
                    "type": "edge",
                    "id": "reactflow__edge-1output_id888-4input_id891",
                },
            ],
        }

        auth = set_up_authentication()
        response = self.client.post(
            "/orchestration/validate",
            json.dumps(request_payload),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(),
            {
                "valid": False,
                "edges": {
                    "reactflow__edge-1output_id888-4input_id891": {
                        "status": False,
                        "allowed_connections": ["Technical Analysis"],
                    }
                },
            },
        )

    def test_ok(self):
        auth = set_up_authentication()
        response = self.client.post(
            "/orchestration/validate",
            json.dumps(SINGLE_FULL_FLOW_VALID),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(),
            {
                "valid": True,
                "edges": {
                    "reactflow__edge-1output_id888-2input_id891": {
                        "status": True,
                        "allowed_connections": [],
                    },
                    "reactflow__edge-1output_id1136-3input_id1143": {
                        "status": True,
                        "allowed_connections": [],
                    },
                    "reactflow__edge-2output_id1356-4input_id1363": {
                        "status": True,
                        "allowed_connections": [],
                    },
                    "reactflow__edge-3output_id1576-4input_id1579": {
                        "status": True,
                        "allowed_connections": [],
                    },
                    "reactflow__edge-4output_id1796-5input_id1799": {
                        "status": True,
                        "allowed_connections": [],
                    },
                },
            },
        )

    def test_invalid(self):
        auth = set_up_authentication()
        response = self.client.post(
            "/orchestration/validate",
            json.dumps(SINGLE_FULL_FLOW_INVALID),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(),
            {
                "valid": False,
                "edges": {
                    "reactflow__edge-1output_id502-4input_id589": {
                        "status": False,
                        "allowed_connections": ["Technical Analysis"],
                    },
                    "reactflow__edge-4output_id986-2input_id1089": {
                        "status": False,
                        "allowed_connections": ["US Stock Data", "Crypto Data"],
                    },
                    "reactflow__edge-4output_id1230-3input_id1417": {
                        "status": False,
                        "allowed_connections": ["Technical Analysis"],
                    },
                },
            },
        )


class RunFlowTest(TestCase):
    @responses.activate
    def test_ok(self):
        auth = set_up_authentication()

        responses.add(
            responses.POST,
            "http://block-monolith:8000/DATA_BLOCK/1/run",
            content_type="application/json",
            json={
                "response": [
                    {
                        "timestamp": "01/01/2020",
                        "timezone": "UTC/EST",
                        "open": "10.00",
                        "high": "10.00",
                        "low": "10.00",
                        "close": "10.00",
                        "volume": "10.00",
                    },
                    {
                        "timestamp": "01/02/2020",
                        "timezone": "UTC/EST",
                        "open": "11.00",
                        "high": "11.00",
                        "low": "11.00",
                        "close": "11.00",
                        "volume": "11.00",
                    },
                    {
                        "timestamp": "01/03/2020",
                        "timezone": "UTC/EST",
                        "open": "12.00",
                        "high": "12.00",
                        "low": "12.00",
                        "close": "12.00",
                        "volume": "12.00",
                    },
                    {
                        "timestamp": "01/04/2020",
                        "timezone": "UTC/EST",
                        "open": "13.00",
                        "high": "13.00",
                        "low": "13.00",
                        "close": "13.00",
                        "volume": "13.00",
                    },
                    {
                        "timestamp": "01/05/2020",
                        "timezone": "UTC/EST",
                        "open": "14.00",
                        "high": "14.00",
                        "low": "14.00",
                        "close": "14.00",
                        "volume": "14.00",
                    },
                ]
            },
            status=200,
        )

        responses.add(
            responses.POST,
            "http://block-monolith:8000/COMPUTATIONAL_BLOCK/1/run",
            content_type="application/json",
            json={
                "response": [
                    {"timestamp": "01/01/2020", "data": None},
                    {"timestamp": "01/02/2020", "data": 10.5},
                    {"timestamp": "01/03/2020", "data": 12.0},
                    {"timestamp": "01/04/2020", "data": 12.5},
                    {"timestamp": "01/05/2020", "data": 13.0},
                ]
            },
            status=200,
        )

        responses.add(
            responses.POST,
            "http://block-monolith:8000/SIGNAL_BLOCK/1/run",
            content_type="application/json",
            json={
                "response": [
                    {"timestamp": "2020-01-02", "order": "BUY"},
                    {"order": "BUY", "timestamp": "2020-01-04"},
                ]
            },
            status=200,
        )

        responses.add(
            responses.POST,
            "http://block-monolith:8000/STRATEGY_BLOCK/1/run",
            content_type="application/json",
            json={
                "response": {
                    "portVals": [
                        {"value": 10000.0, "timestamp": "01/01/2020"},
                        {"value": 8995.150000000009, "timestamp": "01/02/2020"},
                        {"value": 18085.15000000001, "timestamp": "01/03/2020"},
                    ],
                    "trades": [
                        {
                            "date": "01/02/2020",
                            "symbol": "close",
                            "order": "BUY",
                            "monetary_amount": 100000.0,
                            "trade_id": "",
                            "stop_loss": "",
                            "take_profit": "",
                            "shares": 9090,
                            "cash_value": 100989.9,
                        }
                    ],
                }
            },
            status=200,
        )

        response = self.client.post(
            "/orchestration/run",
            json.dumps(SINGLE_FULL_FLOW_VALID),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(),
            {
                "response": {
                    "DATA_BLOCK-1-1": [
                        {
                            "timestamp": "01/01/2020",
                            "timezone": "UTC/EST",
                            "open": "10.00",
                            "high": "10.00",
                            "low": "10.00",
                            "close": "10.00",
                            "volume": "10.00",
                        },
                        {
                            "timestamp": "01/02/2020",
                            "timezone": "UTC/EST",
                            "open": "11.00",
                            "high": "11.00",
                            "low": "11.00",
                            "close": "11.00",
                            "volume": "11.00",
                        },
                        {
                            "timestamp": "01/03/2020",
                            "timezone": "UTC/EST",
                            "open": "12.00",
                            "high": "12.00",
                            "low": "12.00",
                            "close": "12.00",
                            "volume": "12.00",
                        },
                        {
                            "timestamp": "01/04/2020",
                            "timezone": "UTC/EST",
                            "open": "13.00",
                            "high": "13.00",
                            "low": "13.00",
                            "close": "13.00",
                            "volume": "13.00",
                        },
                        {
                            "timestamp": "01/05/2020",
                            "timezone": "UTC/EST",
                            "open": "14.00",
                            "high": "14.00",
                            "low": "14.00",
                            "close": "14.00",
                            "volume": "14.00",
                        },
                    ],
                    "COMPUTATIONAL_BLOCK-1-2": [
                        {"timestamp": "01/01/2020", "data": None},
                        {"timestamp": "01/02/2020", "data": 10.5},
                        {"timestamp": "01/03/2020", "data": 12.0},
                        {"timestamp": "01/04/2020", "data": 12.5},
                        {"timestamp": "01/05/2020", "data": 13.0},
                    ],
                    "COMPUTATIONAL_BLOCK-1-3": [
                        {"timestamp": "01/01/2020", "data": None},
                        {"timestamp": "01/02/2020", "data": 10.5},
                        {"timestamp": "01/03/2020", "data": 12.0},
                        {"timestamp": "01/04/2020", "data": 12.5},
                        {"timestamp": "01/05/2020", "data": 13.0},
                    ],
                    "SIGNAL_BLOCK-1-4": [
                        {"timestamp": "2020-01-02", "order": "BUY"},
                        {"order": "BUY", "timestamp": "2020-01-04"},
                    ],
                    "STRATEGY_BLOCK-1-5": {
                        "portVals": [
                            {"value": 10000.0, "timestamp": "01/01/2020"},
                            {"value": 8995.150000000009, "timestamp": "01/02/2020"},
                            {"value": 18085.15000000001, "timestamp": "01/03/2020"},
                        ],
                        "trades": [
                            {
                                "date": "01/02/2020",
                                "symbol": "close",
                                "order": "BUY",
                                "monetary_amount": 100000.0,
                                "trade_id": "",
                                "stop_loss": "",
                                "take_profit": "",
                                "shares": 9090,
                                "cash_value": 100989.9,
                            }
                        ],
                    },
                }
            },
        )
