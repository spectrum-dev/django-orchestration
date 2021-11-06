import uuid
from unittest.mock import patch

from authentication.factories import set_up_authentication
from orchestration.test_utils import GraphQLTestCase
from strategy.factories import StrategyFactory, UserStrategyFactory
from strategy.models import Strategy, UserStrategy


def fixed_mock_uuid():
    return uuid.UUID(int=0)


class DeleteStrategyViewTest(GraphQLTestCase):
    def setUp(self):
        self.MUTATION = """
            mutation deleteStrategy($strategyId: ID!){
                deleteStrategy(strategyId: $strategyId)
            }
        """

        self.auth = set_up_authentication()

    @patch("uuid.uuid4", fixed_mock_uuid)
    def test_ok(self):
        strategy_id = str(uuid.uuid4())
        UserStrategyFactory(user=self.auth["user"], strategy=strategy_id)

        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={"strategyId": strategy_id},
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(content["data"], {"deleteStrategy": True})

        assert len(UserStrategy.objects.all()) == 0
        assert len(Strategy.objects.all()) == 0

    @patch("uuid.uuid4", fixed_mock_uuid)
    def test_strategy_delete_with_single_commit(self):
        strategy_id = str(uuid.uuid4())
        user_strategy = UserStrategyFactory(
            user=self.auth["user"], strategy=strategy_id
        )

        StrategyFactory(
            strategy=user_strategy,
            commit=uuid.uuid4(),
            flow_metadata={},
            input={},
            output={},
        )

        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={"strategyId": strategy_id},
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(content["data"], {"deleteStrategy": True})

        assert len(UserStrategy.objects.all()) == 0
        assert len(Strategy.objects.all()) == 0

    def test_strategy_delete_with_multiple_commits(self):
        strategy_id = str(uuid.uuid4())
        commit_id_one = "fbdd81fe-7c99-4921-9148-e11466430823"
        commit_id_two = "5385886d-b11a-4d2a-9178-ed31259d1ede"
        user_strategy = UserStrategyFactory(
            user=self.auth["user"], strategy=strategy_id
        )

        StrategyFactory(
            strategy=user_strategy,
            commit=commit_id_one,
            flow_metadata={},
            input={},
            output={},
        )

        StrategyFactory(
            strategy=user_strategy,
            commit=commit_id_two,
            flow_metadata={},
            input={},
            output={},
        )

        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={"strategyId": strategy_id},
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(content["data"], {"deleteStrategy": True})

        assert len(UserStrategy.objects.all()) == 0
        assert len(Strategy.objects.all()) == 0

    def test_strategy_id_dne(self):
        strategy_id = str(uuid.uuid4())

        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={"strategyId": strategy_id},
        )

        self.assertResponseHasErrors(response)
        self.assertEqual(
            content["errors"],
            [
                {
                    "message": "Strategy does not exist",
                    "locations": [{"line": 3, "column": 17}],
                    "path": ["deleteStrategy"],
                }
            ],
        )

    @patch("uuid.uuid4", fixed_mock_uuid)
    def test_different_user_tries_to_delete_strategy(self):
        strategy_id = str(uuid.uuid4())

        auth_user_two = set_up_authentication()
        UserStrategyFactory(user=auth_user_two["user"], strategy=strategy_id)

        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={"strategyId": strategy_id},
        )

        self.assertResponseHasErrors(response)
        self.assertEqual(
            content["errors"],
            [
                {
                    "message": "Strategy does not exist",
                    "locations": [{"line": 3, "column": 17}],
                    "path": ["deleteStrategy"],
                }
            ],
        )
