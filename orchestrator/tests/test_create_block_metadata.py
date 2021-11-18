from authentication.factories import set_up_authentication
from orchestration.test_utils import GraphQLTestCase


class CreateBlockMetadataTest(GraphQLTestCase):
    def setUp(self):
        self.MUTATION = """
            mutation blockMetadata($blockType: BlockType!, $blockName: String!, $inputs: [JSON!], $validations: JSON!, $outputInterface: JSON!) {
                blockMetadata(blockType: $blockType, blockName: $blockName, inputs: $inputs, validations: $validations, outputInterface: $outputInterface) {
                    uniqueBlockId
                    blockId
                    status
                }
            }
        """
        self.auth = set_up_authentication()

    def test_adds_to_block_metadata_successfully(self):
        block_type = "SIGNAL_BLOCK"
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
        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            content["data"],
            {"blockMetadata": {"uniqueBlockId": 1, "blockId": 1, "status": True}},
        )

    def test_adds_multiple_to_block_metadata_successfully(self):
        pass

    def test_adds_to_block_metadata_failure_block_type_dne(self):
        pass

    def test_adds_to_block_metadata_failure_block_already_exists(self):
        pass

    def test_adds_to_block_metadata_failure_negative_block_id(self):
        pass

    # def test_email_exists_in_whitelist(self):
    #     AccountWhitelistFactory(email="valid@testcustomer.com", active=True)
    #     response, content = self.query(
    #         self.MUTATION,
    #         headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
    #         variables={"email": "valid@testcustomer.com"},
    #     )
    #     self.assertResponseNoErrors(response)
    #     self.assertDictEqual(content["data"], {"accountWhitelist": {"status": False}})
