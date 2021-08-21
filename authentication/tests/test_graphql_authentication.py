from django.test import TestCase

from authentication.factories import set_up_authentication


class GraphQLAuthenticationTest(TestCase):
    def test_request_missing_authorization_header(self):
        query = """
            query {
                ping
            }
        """
        response = self.client.post(
            "/graphql/",
            {"query": query},
            content_type="application/json",
        )

        response = response.json()

        assert response["data"] == None
        assert response["errors"][0]["message"] == "User is not authenticated"

    def test_request_has_invalid_authorization_header(self):
        query = """
            query {
                ping
            }
        """
        response = self.client.post(
            "/graphql/",
            {"query": query},
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer invalid-token"},
        )

        response = response.json()

        assert response["data"] == None
        assert response["errors"][0]["message"] == "User is not authenticated"

    def test_request_has_valid_authorization_header(self):
        auth = set_up_authentication()

        query = """
            query {
                ping
            }
        """
        response = self.client.post(
            "/graphql/",
            {"query": query},
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(response.json(), {"data": {"ping": "pong"}})
