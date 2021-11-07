from authentication.factories import set_up_authentication
from orchestration.test_utils import GraphQLTestCase
from strategy.factories import StrategyFactory, UserStrategyFactory


class GetStrategyTest(GraphQLTestCase):
    def setUp(self):
        self.QUERY = """
            query STRATEGY($strategyId: ID!) {
                strategy(strategyId: $strategyId) {
                    strategy {
                        strategyName
                    }
                }
            }
        """

        self.auth = set_up_authentication()

    def test_ok(self):
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

        response, content = self.query(
            self.QUERY,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
            variables={"strategyId": strategy_id},
        )

        self.assertResponseHasErrors(response)
        self.assertDictEqual(content["data"], {})
