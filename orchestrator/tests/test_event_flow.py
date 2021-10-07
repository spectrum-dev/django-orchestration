from django.test import TestCase
from orchestrator.services.flow.spectrum_flow import SpectrumEventFlow

# Test Data
from orchestrator.tests.data.test_event_flow_data import (
    SINGLE_NODE_DATA_FLOW_RETURNS_OK,
    TWO_NODE_INVALID_CONNECTION_RETURNS_002,
    SINGLE_NODE_DATA_FLOW_RETURNS_003,
    TWO_NODE_NOT_CONNECTED_RETURNS_004,
    MULTIPLE_BLOCKS_NOT_IN_ASSEMBLED_DEPEDENCY_LIST_RETURNS_005,
    INVALID_BLOCK_RETURNS_007,
    MOVING_AVERAGE_CROSSOVER_RETURNS_OK,
    MOVING_AVERAGE_CROSSOVER_RETURNS_RESPONSE,
)


class SpectrumEventFlowValidateTest(TestCase):
    def test_empty_flow_returns_001(self):
        spectrum_event_flow = SpectrumEventFlow({}, [])

        self.assertDictEqual(
            spectrum_event_flow.valid,
            {
                "isValid": False,
                "code": "VALIDATE-001",
                "description": "There are no tasks to be run",
            },
        )

    def test_single_node_data_field_empty_003(self):
        spectrum_event_flow = SpectrumEventFlow(
            SINGLE_NODE_DATA_FLOW_RETURNS_003["nodeList"],
            SINGLE_NODE_DATA_FLOW_RETURNS_003["edgeList"],
        )

        self.assertDictEqual(
            spectrum_event_flow.valid,
            {
                "isValid": False,
                "code": "VALIDATE-003",
                "description": "The value for key end_date in block id 1 is invalid / empty",
            },
        )

    def test_single_node_data_flow_returns_ok(self):
        spectrum_event_flow = SpectrumEventFlow(
            SINGLE_NODE_DATA_FLOW_RETURNS_OK["nodeList"],
            SINGLE_NODE_DATA_FLOW_RETURNS_OK["edgeList"],
        )

        self.assertDictEqual(
            spectrum_event_flow.valid,
            {"isValid": True, "code": "VALIDATE-OK", "description": ""},
        )

    def test_two_nodes_invalid_connection_returns_002(self):
        spectrum_event_flow = SpectrumEventFlow(
            TWO_NODE_INVALID_CONNECTION_RETURNS_002["nodeList"],
            TWO_NODE_INVALID_CONNECTION_RETURNS_002["edgeList"],
        )

        self.assertDictEqual(
            spectrum_event_flow.valid,
            {
                "isValid": False,
                "code": "VALIDATE-002",
                "description": f"Input into target block with block type DATA_BLOCK and block id 1",
            },
        )

    def test_two_nodes_not_connected_returns_004(self):
        spectrum_event_flow = SpectrumEventFlow(
            TWO_NODE_NOT_CONNECTED_RETURNS_004["nodeList"],
            TWO_NODE_NOT_CONNECTED_RETURNS_004["edgeList"],
        )

        self.assertDictEqual(
            spectrum_event_flow.valid,
            {
                "isValid": False,
                "code": "VALIDATE-004",
                "description": "The block of type COMPUTATIONAL_BLOCK and id 1. The required number of inputs is 1 but there were 0.",
            },
        )

    # TODO: Determine a case where this is valid
    def test_multiple_blocks_not_in_assembled_dependency_list_returns_005(self):
        spectrum_event_flow = SpectrumEventFlow(
            MULTIPLE_BLOCKS_NOT_IN_ASSEMBLED_DEPEDENCY_LIST_RETURNS_005["nodeList"],
            MULTIPLE_BLOCKS_NOT_IN_ASSEMBLED_DEPEDENCY_LIST_RETURNS_005["edgeList"],
        )

        pass

    # TODO: Determine a case where this is valid
    def test_todo_returns_006(self):
        pass

    def test_invalid_block_returns_007(self):
        spectrum_event_flow = SpectrumEventFlow(
            INVALID_BLOCK_RETURNS_007["nodeList"], INVALID_BLOCK_RETURNS_007["edgeList"]
        )

        self.assertDictEqual(
            spectrum_event_flow.valid,
            {
                "isValid": False,
                "code": "VALIDATE-007",
                "description": "The block with parameters block type INVALID_BLOCK and block ID 1 could not be found in the database",
            },
        )

    def test_moving_average_crossover_returns_ok(self):
        spectrum_event_flow = SpectrumEventFlow(
            MOVING_AVERAGE_CROSSOVER_RETURNS_OK["nodeList"],
            MOVING_AVERAGE_CROSSOVER_RETURNS_OK["edgeList"],
        )

        self.assertDictEqual(
            spectrum_event_flow.valid,
            {"isValid": True, "code": "VALIDATE-OK", "description": ""},
        )

        self.assertDictEqual(
            spectrum_event_flow.input_payloads,
            MOVING_AVERAGE_CROSSOVER_RETURNS_RESPONSE,
        )