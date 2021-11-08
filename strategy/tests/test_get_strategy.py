from authentication.factories import set_up_authentication
from orchestration.test_utils import GraphQLTestCase
from strategy.factories import (
    StrategyFactory,
    StrategySharingFactory,
    UserStrategyFactory,
)


class GetStrategyTest(GraphQLTestCase):
    def setUp(self):
        self.QUERY = """
            query STRATEGY($strategyId: ID!) {
                strategy(strategyId: $strategyId) {
                    strategy {
                        strategyId
                        strategyName
                    }
                    commitId
                    flowMetadata
                    input
                    output
                }
            }
        """

        self.QUERY_WITH_COMMIT = """
            query STRATEGY($strategyId: ID!, $commitId: ID) {
                strategy(strategyId: $strategyId, commitId: $commitId) {
                    strategy {
                        strategyId
                        strategyName
                    }
                    commitId
                    flowMetadata
                    input
                    output
                }
            }
        """

        self.auth = set_up_authentication()

    def test_no_commit_id_returns_latest_strategy(self):
        strategy_id = "5f4a0050-6766-40e1-946c-ddbd5533a3d1"
        commit_id_one = "28061176-a818-4525-a238-c9a73c6418f1"
        commit_id_two = "28061176-a818-4525-a238-c9a73c6418f2"
        user_strategy = UserStrategyFactory(
            user=self.auth["user"], strategy=strategy_id, strategy_name="Test Name"
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
            input={"test": "test"},
            output={},
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
                "strategy": {
                    "strategy": {
                        "strategyId": "5f4a0050-6766-40e1-946c-ddbd5533a3d1",
                        "strategyName": "Test Name",
                    },
                    "commitId": "28061176-a818-4525-a238-c9a73c6418f2",
                    "flowMetadata": {},
                    "input": {"test": "test"},
                    "output": {},
                }
            },
        )

    def test_commit_id_returns_specific_strategy(self):
        strategy_id = "5f4a0050-6766-40e1-946c-ddbd5533a3d1"
        commit_id_one = "28061176-a818-4525-a238-c9a73c6418f1"
        commit_id_two = "28061176-a818-4525-a238-c9a73c6418f2"
        user_strategy = UserStrategyFactory(
            user=self.auth["user"], strategy=strategy_id, strategy_name="Test Name"
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
            input={"test": "test"},
            output={},
        )

        response, content = self.query(
            self.QUERY_WITH_COMMIT,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={"strategyId": strategy_id, "commitId": commit_id_one},
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            content["data"],
            {
                "strategy": {
                    "strategy": {
                        "strategyId": "5f4a0050-6766-40e1-946c-ddbd5533a3d1",
                        "strategyName": "Test Name",
                    },
                    "commitId": "28061176-a818-4525-a238-c9a73c6418f1",
                    "flowMetadata": {},
                    "input": {},
                    "output": {},
                }
            },
        )

    def test_strategy_id_dne(self):
        strategy_id = "5f4a0050-6766-40e1-946c-ddbd5533a3d1"

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
                    "locations": [{"column": 17, "line": 3}],
                    "message": "You are not authorized to view this strategy",
                    "path": ["strategy"],
                }
            ],
        )

    def test_strategy_id_does_not_belong_to_user_and_is_not_shared(self):
        other_user = set_up_authentication()
        strategy_id = "5f4a0050-6766-40e1-946c-ddbd5533a3d1"
        commit_id = "28061176-a818-4525-a238-c9a73c6418f1"

        user_strategy = UserStrategyFactory(
            user=other_user["user"], strategy=strategy_id
        )

        StrategyFactory(
            strategy=user_strategy,
            commit=commit_id,
            flow_metadata={},
            input={},
            output={},
        )

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
                    "locations": [{"column": 17, "line": 3}],
                    "message": "You are not authorized to view this strategy",
                    "path": ["strategy"],
                }
            ],
        )

    def test_shared_user_can_view_strategy(self):
        shared_auth = set_up_authentication()
        strategy_id = "5f4a0050-6766-40e1-946c-ddbd5533a3d1"
        commit_id = "28061176-a818-4525-a238-c9a73c6418f1"

        user_strategy = UserStrategyFactory(
            user=self.auth["user"], strategy=strategy_id
        )
        StrategyFactory(
            strategy=user_strategy,
            commit=commit_id,
            flow_metadata={},
            input={},
            output={},
        )

        StrategySharingFactory(
            strategy=user_strategy, user=shared_auth["user"], permissions=2
        )

        response, content = self.query(
            self.QUERY,
            headers={"HTTP_AUTHORIZATION": f"Bearer {shared_auth['token']}"},
            variables={"strategyId": strategy_id},
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            content["data"],
            {
                "strategy": {
                    "strategy": {
                        "strategyId": "5f4a0050-6766-40e1-946c-ddbd5533a3d1",
                        "strategyName": "",
                    },
                    "commitId": "28061176-a818-4525-a238-c9a73c6418f1",
                    "flowMetadata": {},
                    "input": {},
                    "output": {},
                }
            },
        )

    def test_commit_id_dne(self):
        strategy_id = "5f4a0050-6766-40e1-946c-ddbd5533a3d1"
        commit_id = "26fed45a-20f3-47b0-819c-c17bfe22774a"

        UserStrategyFactory(user=self.auth["user"], strategy=strategy_id)

        response, content = self.query(
            self.QUERY_WITH_COMMIT,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={"strategyId": strategy_id, "commitId": commit_id},
        )

        self.assertResponseHasErrors(response)
        self.assertEqual(
            content["errors"],
            [
                {
                    "locations": [{"column": 17, "line": 3}],
                    "message": "The strategy and commit pair does not exist",
                    "path": ["strategy"],
                }
            ],
        )
