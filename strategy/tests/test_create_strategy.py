import uuid
from unittest.mock import patch

from authentication.factories import set_up_authentication
from orchestration.test_utils import GraphQLTestCase
from strategy.factories import (
    StrategyFactory,
    StrategySharingFactory,
    UserStrategyFactory,
)


def fixed_mock_uuid():
    return uuid.UUID(int=0)


class CreateStrategyTest(GraphQLTestCase):
    def setUp(self):
        self.MUTATION = """
            mutation strategy($strategyId: ID!, $commitId: ID, $metadata: JSON!, $inputs: JSON!, $outputs: JSON!) {
                strategy(strategyId: $strategyId, commitId: $commitId, metadata: $metadata, inputs: $inputs, outputs: $outputs)
            }
        """

        self.auth = set_up_authentication()

    def test_ok(self):
        strategy_id = "136f0d6e-1e32-4edb-ac5e-1676047425d2"
        commit_id = "c98d7e19-673b-4609-9b32-6f827fe515e6"

        UserStrategyFactory(user=self.auth["user"], strategy=strategy_id)

        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={
                "strategyId": strategy_id,
                "commitId": commit_id,
                "inputs": {},
                "outputs": {},
                "metadata": {},
            },
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(content["data"], {"strategy": True})

    def test_strategy_id_doesnt_exist(self):
        strategy_id = "136f0d6e-1e32-4edb-ac5e-1676047425d2"
        commit_id = "c98d7e19-673b-4609-9b32-6f827fe515e6"

        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={
                "strategyId": strategy_id,
                "commitId": commit_id,
                "inputs": {},
                "outputs": {},
                "metadata": {},
            },
        )

        self.assertResponseHasErrors(response)
        self.assertEqual(
            content["errors"],
            [
                {
                    "message": "This strategy does not exist",
                    "locations": [{"line": 3, "column": 17}],
                    "path": ["strategy"],
                }
            ],
        )

    def test_strategy_commit_already_exists(self):
        strategy_id = "136f0d6e-1e32-4edb-ac5e-1676047425d2"
        commit_id = "c98d7e19-673b-4609-9b32-6f827fe515e6"

        user_strategy = UserStrategyFactory(
            user=self.auth["user"], strategy=strategy_id
        )

        StrategyFactory(
            strategy=user_strategy,
            commit=commit_id,
            flow_metadata={},
            input={"1": {}},
            output={"1": {}},
        )

        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={
                "strategyId": strategy_id,
                "commitId": commit_id,
                "inputs": {},
                "outputs": {},
                "metadata": {},
            },
        )

        self.assertResponseHasErrors(response)
        self.assertEqual(
            content["errors"],
            [
                {
                    "message": "The strategy-commit pair already exist",
                    "locations": [{"line": 3, "column": 17}],
                    "path": ["strategy"],
                }
            ],
        )

    def test_strategy_id_not_valid(self):
        strategy_id = "strategy_id_invalid"
        commit_id = "c98d7e19-673b-4609-9b32-6f827fe515e6"

        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={
                "strategyId": strategy_id,
                "commitId": commit_id,
                "inputs": {},
                "outputs": {},
                "metadata": {},
            },
        )

        self.assertResponseHasErrors(response)
        self.assertEqual(
            content["errors"],
            [
                {
                    "message": "The strategy id is invalid",
                    "locations": [{"line": 3, "column": 17}],
                    "path": ["strategy"],
                }
            ],
        )

    def test_commit_id_not_valid(self):
        strategy_id = "136f0d6e-1e32-4edb-ac5e-1676047425d2"
        commit_id = "commit_id_invalid"

        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={
                "strategyId": strategy_id,
                "commitId": commit_id,
                "inputs": {},
                "outputs": {},
                "metadata": {},
            },
        )

        self.assertResponseHasErrors(response)
        self.assertEqual(
            content["errors"],
            [
                {
                    "message": "The commit id is invalid",
                    "locations": [{"line": 3, "column": 17}],
                    "path": ["strategy"],
                }
            ],
        )

    @patch("uuid.uuid4", fixed_mock_uuid)
    def test_saving_without_commit_id_generates_new_id_success(self):
        strategy_id = "136f0d6e-1e32-4edb-ac5e-1676047425d2"
        commit_id = None

        UserStrategyFactory(user=self.auth["user"], strategy=strategy_id)

        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={
                "strategyId": strategy_id,
                "commitId": commit_id,
                "inputs": {},
                "outputs": {},
                "metadata": {},
            },
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(content["data"], {"strategy": True})

    def test_shared_user_with_write_permissions_can_save(self):
        shared_auth = set_up_authentication()

        strategy_id = "136f0d6e-1e32-4edb-ac5e-1676047425d2"
        commit_id = "c98d7e19-673b-4609-9b32-6f827fe515e6"

        user_strategy = UserStrategyFactory(
            user=self.auth["user"], strategy=strategy_id
        )
        StrategySharingFactory(
            strategy=user_strategy, user=shared_auth["user"], permissions=2
        )

        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {shared_auth['token']}"},
            variables={
                "strategyId": strategy_id,
                "commitId": commit_id,
                "inputs": {},
                "outputs": {},
                "metadata": {},
            },
        )

        self.assertResponseNoErrors(response)
        self.assertDictEqual(content["data"], {"strategy": True})

    def test_shared_user_with_read_permissions_cannot_save(self):
        shared_auth = set_up_authentication()

        strategy_id = "136f0d6e-1e32-4edb-ac5e-1676047425d2"
        commit_id = "c98d7e19-673b-4609-9b32-6f827fe515e6"

        user_strategy = UserStrategyFactory(
            user=self.auth["user"], strategy=strategy_id
        )
        StrategySharingFactory(
            strategy=user_strategy, user=shared_auth["user"], permissions=1
        )

        response, content = self.query(
            self.MUTATION,
            headers={"HTTP_AUTHORIZATION": f"Bearer {shared_auth['token']}"},
            variables={
                "strategyId": strategy_id,
                "commitId": commit_id,
                "inputs": {},
                "outputs": {},
                "metadata": {},
            },
        )

        self.assertResponseHasErrors(response)
        self.assertEqual(
            content["errors"],
            [
                {
                    "message": "You only have read permissions on this strategy",
                    "locations": [{"line": 3, "column": 17}],
                    "path": ["strategy"],
                }
            ],
        )
