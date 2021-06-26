from django.test import TestCase

from authentication.factories import set_up_authentication


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
    def test_ok(self):
        pass

    def test_indicator_name_ok(self):
        pass

    def test_name_pass(self):
        pass

    def test_block_type_dne(self):
        pass

    def test_block_id_dne(self):
        pass


class ValidateFlowTest(TestCase):
    pass


class RunFlowTest(TestCase):
    pass
