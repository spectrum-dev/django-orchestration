from authentication.factories import set_up_authentication
from orchestration.test_utils import GraphQLTestCase


class CreateBlockMetadataTest(GraphQLTestCase):
    def setUp(self):
        self.MUTATION = """
            mutation blockMetadata($blockType: BlockType!, $blockName: String!, $inputs: [JSON!], $validations: JSON!, $outputInterface: JSON!) {
                blockMetadata(blockType: $blockType, blockName: $blockName, inputs: $inputs, validations: $validations, outputInterface: $outputInterface) {
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


    def test_adds_to_block_metadata_successfully(self):
        block_type = "STRATEGY_BLOCK"
        block_name = "Test Block"
        inputs = [
            {
                "fieldName": "Commission ($)",
                "fieldVariableName": "commission",
                "fieldType": "input",
            },
        ]
        validations = {
            "input": {
                "required": [
                    {"blockType": ["DATA_BLOCK"], "number": 1},
                ],
                "allowed_blocks": [
                    {"blockId": "1", "blockType": "SIGNAL_BLOCK"},
                ],
            },
            "output": [{"blockType": "STRATEGY_BLOCK", "number": 1}],
        }
        output_interface = {"interface": ["timestamp", "order"]}

        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={
                "blockType": block_type,
                "blockName": block_name,
                "inputs": inputs,
                "validations": validations,
                "outputInterface": output_interface,
            },
        )
        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            content["data"],
            {
                "blockMetadata": {
                    "blockName": "Test Block",
                    "blockType": "STRATEGY_BLOCK",
                    "blockId": 3,  # Intentionally flaky test, strategy blocks should rarely be implemented but will increment if more blocks become available
                    "inputs": [
                        {
                            "field_name": "Commission ($)",
                            "field_variable_name": "commission",
                            "field_type": "input",
                        },
                    ],
                    "validations": {
                        "input": {
                            "required": [
                                {"block_type": ["DATA_BLOCK"], "number": 1},
                            ],
                            "allowed_blocks": [
                                {"block_id": "1", "block_type": "SIGNAL_BLOCK"},
                            ],
                        },
                        "output": [{"block_type": "STRATEGY_BLOCK", "number": 1}],
                    },
                    "outputInterface": {"interface": ["timestamp", "order"]},
                }
            },
        )

    def test_adds_to_block_metadata_failure_block_type_dne(self):
        block_type = "DATA_BLOCK_DNE"
        block_name = "Test Block"
        inputs = []
        validations = {}
        output_interface = {"interface": ["timestamp", "order"]}

        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={
                "blockType": block_type,
                "blockName": block_name,
                "inputs": inputs,
                "validations": validations,
                "outputInterface": output_interface,
            },
        )
        self.assertResponseHasErrors(response)
        self.assertEqual(
            content["errors"],
            [
                {
                    "locations": [{"column": 36, "line": 2}],
                    "message": "Variable '$blockType' got invalid value 'DATA_BLOCK_DNE'; Value "
                    "'DATA_BLOCK_DNE' does not exist in 'BlockType' enum. Did you "
                    "mean the enum value 'DATA_BLOCK'?",
                    "path": None,
                }
            ],
        )

    def test_adds_to_block_metadata_failure_missing_input(self):
        block_name = "Test Block"
        inputs = []
        validations = {}
        output_interface = {"interface": ["timestamp", "order"]}

        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={
                "blockName": block_name,
                "inputs": inputs,
                "validations": validations,
                "outputInterface": output_interface,
            },
        )
        self.assertResponseHasErrors(response)
        self.assertEqual(
            content["errors"],
            [
                {
                    "locations": [{"column": 36, "line": 2}],
                    "message": "Variable '$blockType' of required type 'BlockType!' was not "
                    "provided.",
                    "path": None,
                }
            ],
        )
