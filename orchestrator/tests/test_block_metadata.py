from authentication.factories import set_up_authentication
from orchestration.test_utils import GraphQLTestCase


class MetadataViewTest(GraphQLTestCase):
    def setUp(self):
        self.QUERY = """
            query blockMetadata($blockType: BlockType!, $blockId: Int!) {
                blockMetadata(blockType: $blockType, blockId: $blockId) {
                    blockName
                    blockType
                    blockId
                    inputs
                    validations
                    outputInterface
                }
            }
        """
        self.auth = set_up_authentication()

    def test_ok(self):
        block_type = "DATA_BLOCK"
        block_id = 1

        response, content = self.query(
            self.QUERY,
            variables={"blockType": block_type, "blockId": block_id},
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            content["data"],
            {
                "blockMetadata": {
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
                }
            },
        )

    def test_block_type_dne(self):
        block_type = "DATA_BLOCK_DNE"
        block_id = 1

        response, content = self.query(
            self.QUERY,
            variables={"blockType": block_type, "blockId": block_id},
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
        )

        self.assertResponseHasErrors(response)
        self.assertEqual(
            content["errors"],
            [
                {
                    "locations": [{"column": 33, "line": 2}],
                    "message": "Variable '$blockType' got invalid value 'DATA_BLOCK_DNE'; Value "
                    "'DATA_BLOCK_DNE' does not exist in 'BlockType' enum. Did you "
                    "mean the enum value 'DATA_BLOCK'?",
                    "path": None,
                }
            ],
        )

    def test_block_id_dne(self):
        block_type = "DATA_BLOCK"
        block_id = -1  # This block ID DNE

        response, content = self.query(
            self.QUERY,
            variables={"blockType": block_type, "blockId": block_id},
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
        )

        self.assertResponseHasErrors(response)
        self.assertEqual(
            content["errors"],
            [
                {
                    "message": "Block Type - ID Pair does not exist",
                    "locations": [{"line": 3, "column": 17}],
                    "path": ["blockMetadata"],
                }
            ],
        )
