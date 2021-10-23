from authentication.factories import set_up_authentication
from orchestration.test_utils import GraphQLTestCase


class AllMetadataTest(GraphQLTestCase):
    def setUp(self):
        self.QUERY = """
            query allMetadata {
                allMetadata 
            }
        """
        self.auth = set_up_authentication()

    def test_ok(self):
        response, _ = self.query(
            self.QUERY,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
        )
        self.assertResponseNoErrors(response)
        # NOTE: I am not asserting the response body here as
        #       it changes as we add new blocks
