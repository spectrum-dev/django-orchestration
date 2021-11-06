import uuid
from unittest.mock import patch

from authentication.factories import set_up_authentication
from orchestration.test_utils import GraphQLTestCase
from strategy.factories import UserStrategyFactory


def fixed_mock_uuid():
    return uuid.UUID(int=0)


class CreateUserStrategyTest(GraphQLTestCase):
    def setUp(self):
        self.MUTATION = """
            mutation userStrategy($strategyName: String!) {
                userStrategy(strategyName: $strategyName) {
                    strategyName
                    strategyId
                }
            }
        """
        self.auth = set_up_authentication()

    @patch("uuid.uuid4", fixed_mock_uuid)
    def test_ok(self):
        strategy_name = "Test Strategy"
        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={"strategyName": strategy_name},
        )

        self.assertResponseNoErrors(response)

        self.assertDictEqual(
            content["data"],
            {
                "userStrategy": {
                    "strategyId": "00000000-0000-0000-0000-000000000000",
                    "strategyName": strategy_name,
                }
            },
        )

    @patch("uuid.uuid4", fixed_mock_uuid)
    def test_strategy_user_pair_exists(self):
        UserStrategyFactory(user=self.auth["user"], strategy=uuid.uuid4())

        strategy_name = "Test Strategy"
        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={"strategyName": strategy_name},
        )

        self.assertResponseHasErrors(response)
        self.assertEqual(
            content["errors"],
            [
                {
                    "message": "The strategy ID - user pair already exists",
                    "locations": [{"line": 3, "column": 17}],
                    "path": ["userStrategy"],
                }
            ],
        )
