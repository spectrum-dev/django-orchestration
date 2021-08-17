from django.test import TestCase
from orchestrator.services.flow import spectrum_event_flow

from orchestrator.services.flow.spectrum_event_flow import SpectrumEventFlow

# Test Data
from orchestrator.tests.data.test_event_flow_data import (
    SINGLE_NODE_DATA_FLOW_RETURNS_OK,
    TWO_NODE_INVALID_CONNECTION_RETURNS_002,
    SINGLE_NODE_DATA_FLOW_RETURNS_003,
    TWO_NODE_NOT_CONNECTED_RETURNS_004,
    
)

class SpectrumEventFlowValidateTest(TestCase):
    def test_empty_flow_returns_001(self):
        spectrum_event_flow = SpectrumEventFlow({}, [])
        
        self.assertDictEqual(
            spectrum_event_flow.validate(),
            {
                "isValid": False,
                "code": "VALIDATE-001",
                "description": "There are no tasks to be run"
            }
        )
    
    def test_single_node_data_field_empty_003(self):
        spectrum_event_flow = SpectrumEventFlow(
            SINGLE_NODE_DATA_FLOW_RETURNS_003["nodeList"],
            SINGLE_NODE_DATA_FLOW_RETURNS_003["edgeList"]
        )
        
        self.assertDictEqual(
            spectrum_event_flow.validate(),
            {
                "isValid": False,
                "code": "VALIDATE-003",
                "description": "The value for key end_date in block id 1 is invalid / empty"
            }
        )

    def test_single_node_data_flow_returns_ok(self):
        spectrum_event_flow = SpectrumEventFlow(
            SINGLE_NODE_DATA_FLOW_RETURNS_OK["nodeList"],
            SINGLE_NODE_DATA_FLOW_RETURNS_OK["edgeList"]
        )
        
        self.assertDictEqual(
            spectrum_event_flow.validate(),
            {
                "isValid": True,
                "code": "VALIDATE-OK",
                "description": ""
            }
        )
    
    def test_two_nodes_invalid_connection_returns_002(self):
        spectrum_event_flow = SpectrumEventFlow(
            TWO_NODE_INVALID_CONNECTION_RETURNS_002["nodeList"],
            TWO_NODE_INVALID_CONNECTION_RETURNS_002["edgeList"],
        )

        self.assertDictEqual(
            spectrum_event_flow.validate(),
            {
                "isValid": False,
                "code": "VALIDATE-002",
                "description": f"Input into target block with block type DATA_BLOCK and block id 1"
            }
        )

    def test_two_nodes_not_connected_returns_004(self):
        spectrum_event_flow = SpectrumEventFlow(
            TWO_NODE_NOT_CONNECTED_RETURNS_004["nodeList"],
            TWO_NODE_NOT_CONNECTED_RETURNS_004["edgeList"]
        )
        
        self.assertDictEqual(
            spectrum_event_flow.validate(),
            {
                "isValid": False,
                "code": "VALIDATE-004",
                "description": "The block of type COMPUTATIONAL_BLOCK and id 1. The required number of inputs is 1 but there were 0."
            }
        )

    
