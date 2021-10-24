from authentication.factories import set_up_authentication
from orchestration.test_utils import GraphQLTestCase


class AllMetadataTest(GraphQLTestCase):
    def setUp(self):
        self.QUERY = """
            query allMetadata($strategyType: StrategyType!) {
                allMetadata(strategyType: $strategyType)
            }
        """
        self.auth = set_up_authentication()

    def test_backtest_ok(self):
        response, content = self.query(
            self.QUERY,
            variables={"strategyType": "BACKTEST"},
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
        )

        # NOTE: I am not asserting the response body here as
        #       it changes as we add new blocks
        self.assertResponseNoErrors(response)
        assert "STRATEGY_BLOCK" in content["data"]["allMetadata"].keys()

    def test_screener_ok(self):
        response, content = self.query(
            self.QUERY,
            variables={"strategyType": "SCREENER"},
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
        )

        # NOTE: I am not asserting the response body here as
        #       it changes as we add new blocks
        self.assertResponseNoErrors(response)
        assert "STRATEGY_BLOCK" not in content["data"]["allMetadata"].keys()

    def test_pending_ok(self):
        response, content = self.query(
            self.QUERY,
            variables={"strategyType": "PENDING"},
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.auth['token']}"},
        )

        # NOTE: I am not asserting the response body here as
        #       it changes as we add new blocks
        self.assertResponseNoErrors(response)
        assert "STRATEGY_BLOCK" in content["data"]["allMetadata"].keys()
