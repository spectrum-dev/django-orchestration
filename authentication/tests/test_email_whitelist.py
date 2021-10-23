from authentication.factories import AccountWhitelistFactory, set_up_authentication
from orchestration.test_utils import GraphQLTestCase


class ValidateEmailWhitelistTest(GraphQLTestCase):
    def setUp(self):
        self.AUTHENTICATION_QUERY = """
            query accountWhitelistStatus($email: String!) {
                accountWhitelistStatus(email: $email) {
                    status
                }
            }
        """
        self.auth = set_up_authentication()

    def test_email_exists_and_active(self):
        AccountWhitelistFactory(email="valid@testcustomer.com", active=True)
        response, content = self.query(
            self.AUTHENTICATION_QUERY,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={"email": "valid@testcustomer.com"},
        )
        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            content["data"], {"accountWhitelistStatus": {"status": True}}
        )

    def test_email_exists_not_active(self):
        AccountWhitelistFactory(email="valid@testcustomer.com", active=False)
        response, content = self.query(
            self.AUTHENTICATION_QUERY,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={"email": "valid@testcustomer.com"},
        )
        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            content["data"], {"accountWhitelistStatus": {"status": False}}
        )

    def test_email_dne(self):
        response, content = self.query(
            self.AUTHENTICATION_QUERY,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={"email": "valid@testcustomer.com"},
        )
        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            content["data"], {"accountWhitelistStatus": {"status": False}}
        )
