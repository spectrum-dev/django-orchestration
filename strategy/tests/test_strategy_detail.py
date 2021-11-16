import uuid
from unittest.mock import patch

from authentication.factories import set_up_authentication
from orchestration.test_utils import GraphQLTestCase
from strategy.factories import UserStrategyFactory


def fixed_mock_uuid():
    return uuid.UUID(int=0)


class CreateUserStrategyTest(GraphQLTestCase):
    def setUp(self):
        self.QUERY = """
            query userStrategy($strategyId: ID!){
                userStrategy(strategyId: $strategyId) {
                    strategyId
                    strategyName
                }
            }
        """

        self.auth = set_up_authentication()

    @patch("uuid.uuid4", fixed_mock_uuid)
    def test_ok(self):
        strategy_name = "Strategy One"
        strategy_id = str(uuid.uuid4())
        UserStrategyFactory(
            user=self.auth["user"], strategy=strategy_id, strategy_name=strategy_name
        )

        response, content = self.query(
            self.QUERY,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={"strategyId": strategy_id},
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
    def test_strategy_id_dne(self):
        strategy_id = str(uuid.uuid4())

        response, content = self.query(
            self.QUERY,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={"strategyId": strategy_id},
        )

        self.assertResponseHasErrors(response)

        self.assertEqual(
            content["errors"],
            [
                {
                    "message": "This strategy ID does not exist",
                    "locations": [{"line": 3, "column": 17}],
                    "path": ["userStrategy"],
                }
            ],
        )
