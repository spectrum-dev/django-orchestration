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
                            "blockName": "Raw Data",
                            "blockMetadata": "/orchestration/$DATA_BLOCK/$1/",
                        }
                    },
                    "COMPUTATIONAL_BLOCK": {
                        "1": {
                            "blockName": "Technical Analysis",
                            "blockMetadata": "/orchestration/$COMPUTATIONAL_BLOCK/$1/",
                        }
                    },
                    "SIGNAL_BLOCK": {
                        "1": {
                            "blockName": "Event",
                            "blockMetadata": "/orchestration/$SIGNAL_BLOCK/$1/",
                        }
                    },
                    "STRATEGY_BLOCK": {
                        "1": {
                            "blockName": "Backtest",
                            "blockMetadata": "/orchestration/$STRATEGY_BLOCK/$1/",
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
                "blockName": "Raw Data",
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
                        "fieldData": {"base": "/dataType", "method": "GET"},
                        "fieldName": "Data Type",
                        "fieldType": "dropdown",
                        "fieldVariableName": "data_type",
                    },
                    {
                        "fieldData": {"base": "/interval", "method": "GET"},
                        "fieldName": "Interval",
                        "fieldType": "dropdown",
                        "fieldVariableName": "interval",
                    },
                    {
                        "fieldData": {"base": "/outputSize", "method": "GET"},
                        "fieldName": "Output Size",
                        "fieldType": "dropdown",
                        "fieldVariableName": "outputsize",
                    },
                    {
                        "fieldName": "Start Date",
                        "fieldType": "input",
                        "fieldVariableName": "start_date",
                    },
                    {
                        "fieldName": "End Date",
                        "fieldType": "input",
                        "fieldVariableName": "end_date",
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

    def test_block_type_dne(self):
        auth = set_up_authentication()
        block_type = "DATA_BLOCK_DNE"
        block_id = 1
        action_name = "dataType"

        response = self.client.get(
            f"/orchestration/{block_type}/{block_id}/{action_name}",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(response.json(), {"error": "Unhandled error"})

    def test_block_id_dne(self):
        auth = set_up_authentication()
        block_type = "DATA_BLOCK"
        block_id = -1
        action_name = "dataType"

        response = self.client.get(
            f"/orchestration/{block_type}/{block_id}/{action_name}",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(response.json(), {"error": "Unhandled error"})


class ValidateFlowTest(TestCase):
    def test_ok(self):
        auth = set_up_authentication()
        response = self.client.post(
            "/orchestration/validate",
            json.dumps(SINGLE_FULL_FLOW_VALID),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(response.json(), {"valid": True})

    def test_invalid(self):
        auth = set_up_authentication()
        response = self.client.post(
            "/orchestration/validate",
            json.dumps(SINGLE_FULL_FLOW_INVALID),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(response.json(), {"valid": False})


class RunFlowTest(TestCase):
    pass
