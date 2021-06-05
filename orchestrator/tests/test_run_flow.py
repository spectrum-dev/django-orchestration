from django.test import TestCase

from orchestrator.services.flow.spectrum_flow_v2 import SpectrumFlow
from orchestrator.tests.data.test_full_single_flow_valid import TEST_FULL_SINGLE_FLOW_VALID
from orchestrator.tests.data.test_data_validation import SINGLE_FULL_FLOW_VALID

class RunFlowTest(TestCase):
    def test_full_single_flow_valid(self):
        flow = SpectrumFlow(SINGLE_FULL_FLOW_VALID["nodeList"], SINGLE_FULL_FLOW_VALID["edgeList"])

        flow.run(mode="RUN")

        # self.assertDictEqual(response, TEST_FULL_SINGLE_FLOW_VALID)
        
        pass
