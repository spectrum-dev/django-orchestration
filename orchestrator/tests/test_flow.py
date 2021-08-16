from django.test import TestCase

from orchestrator.services.flow.spectrum_event_flow import SpectrumEventFlow
from orchestrator.tests.data.test_data_validation import SINGLE_FULL_FLOW_VALID

class SpectrumEventFlowValidateTest(TestCase):
    def setUp(self):
        self.event_flow = SpectrumEventFlow(
            SINGLE_FULL_FLOW_VALID["nodeList"],
            SINGLE_FULL_FLOW_VALID["edgeList"]
        )
    
    def test_no_events_returns_invalid(self):
        response = {}
        self.assertDictEqual(
            response,
            {
                "isValid": False,
                "code": "VALIDATE-001",
                "description": "There are no tasks to be run"
            }
        )
    
