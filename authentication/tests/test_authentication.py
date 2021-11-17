from authentication.factories import set_up_authentication, set_up_basic_authentication
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

    def test_request_has_valid_authorization_header_with_bearer_token(self):
        response, content = self.query(
            self.QUERY,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
        )
        self.assertResponseNoErrors(response)
        self.assertDictEqual(content["data"], {"ping": "pong"})

    def test_request_has_valid_authorization_header_with_basic_token(self):
        basic_auth = set_up_basic_authentication()
        response, content = self.query(
            self.QUERY,
            headers={"HTTP_AUTHORIZATION": f"Basic {basic_auth['token']}"},
        )
        self.assertResponseNoErrors(response)
        self.assertDictEqual(content["data"], {"ping": "pong"})
