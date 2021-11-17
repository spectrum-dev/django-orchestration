from authentication.factories import AccountWhitelistFactory, set_up_authentication
from orchestration.test_utils import GraphQLTestCase


class CreateEmailWhitelistTest(GraphQLTestCase):
    def setUp(self):
        self.MUTATION = """
            mutation accountWhitelist($email: String!) {
                accountWhitelist(email: $email) {
                    status
                }
            }
        """
        self.auth = set_up_authentication()

    def test_adds_to_whitelist_successfully(self):
        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={"email": "valid@testcustomer.com"},
        )
        self.assertResponseNoErrors(response)
        self.assertDictEqual(content["data"], {"accountWhitelist": {"status": True}})

    def test_email_exists_in_whitelist(self):
        AccountWhitelistFactory(email="valid@testcustomer.com", active=True)
        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={"email": "valid@testcustomer.com"},
        )
        self.assertResponseNoErrors(response)
        self.assertDictEqual(content["data"], {"accountWhitelist": {"status": False}})
