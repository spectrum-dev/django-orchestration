import json

from django.test import TestCase

from authentication.factories import AccountWhitelistFactory


class ValidateEmailWhitelistTest(TestCase):
    def test_email_exists_and_active(self):
        account_whitelist = AccountWhitelistFactory(
            email="valid@testcustomer.com", active=True
        )

        payload = {"email": account_whitelist.email}

        response = self.client.post(
            "/authentication/validate",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(response.json(), {"status": True})

    def test_email_exists_not_active(self):
        account_whitelist = AccountWhitelistFactory(
            email="valid@testcustomer.com", active=False
        )

        payload = {"email": account_whitelist.email}

        response = self.client.post(
            "/authentication/validate",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(response.json(), {"status": False})

    def test_email_dne(self):
        payload = {"email": "valid@testuser.com"}

        response = self.client.post(
            "/authentication/validate",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(response.json(), {"status": False})

    def test_email_field_empty(self):
        payload = {"email": ""}

        response = self.client.post(
            "/authentication/validate",
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertDictEqual(
            response.json(), {"email": ["This field may not be blank."]}
        )
