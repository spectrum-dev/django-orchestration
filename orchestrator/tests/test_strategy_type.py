from django.test import TestCase

from orchestrator.services.flow.spectrum_flow import SpectrumFlow
from orchestrator.tests.data.test_data_strategy_type import BACKTEST_FLOW_OK, SCREENER_FLOW_OK

class SpectrumFlowStrategyTest(TestCase):
    def test_backtest_ok(self):
        spectrum_flow = SpectrumFlow(BACKTEST_FLOW_OK["nodeList"], BACKTEST_FLOW_OK["edgeList"])

        assert spectrum_flow.strategy_type == "BACKTEST"
    
    def test_screener_ok(self):
        spectrum_flow = SpectrumFlow(SCREENER_FLOW_OK["nodeList"], SCREENER_FLOW_OK["edgeList"])

        assert spectrum_flow.strategy_type == "SCREENER"

