from authentication.factories import set_up_authentication
from orchestration.test_utils import GraphQLTestCase


class AuthenticationTest(GraphQLTestCase):
    def setUp(self):
        self.QUERY = """
            query {
                ping
            }
        """
        self.auth = set_up_authentication()

    def test_request_missing_authorization_header(self):
        response, content = self.query(
            self.QUERY,
        )
        self.assertResponseHasErrors(response)
        assert content["errors"][0]["message"] == "User is not authenticated"

    def test_request_has_invalid_authorization_header(self):
        response, content = self.query(
            self.QUERY,
            headers={"HTTP_AUTHORIZATION": f"Bearer invalid-token"},
        )
        self.assertResponseHasErrors(response)
        assert content["errors"][0]["message"] == "User is not authenticated"

    def test_request_has_valid_authorization_header(self):
        response, content = self.query(
            self.QUERY,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
        )
        self.assertResponseNoErrors(response)
        self.assertDictEqual(content["data"], {"ping": "pong"})
