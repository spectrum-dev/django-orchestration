from unittest import mock

from django.test import TestCase

from authentication.factories import set_up_authentication
from orchestrator.exceptions import MultipleBacktestBlocksException
from orchestrator.services.flow.spectrum_flow import SpectrumFlow
from orchestrator.tests.data.fixture_mock import (
    MULTIPLE_STRATEGY_BLOCK_MOCK_RESPONSE,
    GenericCeleryMockClass,
)

# Test Data
from orchestrator.tests.data.test_flow_data import (
    AND_BLOCK_SELECTS_CORRECT_PAYLOAD_AND_RETURNS_OK,
    AND_BLOCK_SELECTS_CORRECT_PAYLOAD_AND_RETURNS_OK_RESPONSE,
    BLOCK_DNE_IN_ASSEMBLED_DEPENDENCY_LIST_BUT_IN_REQUIRED_FIELDS_RESPONSE,
    BLOCK_DNE_IN_ASSEMBLED_DEPENDENCY_LIST_BUT_IN_REQUIRED_FIELDS_RETURNS_OK,
    FLOW_WITH_SCREENER_BLOCK_RETURNS_OK,
    FLOW_WITHOUT_SCREENER_BLOCK_RETURNS_008,
    INVALID_BLOCK_RETURNS_007,
    MOVING_AVERAGE_CROSSOVER_RETURNS_OK,
    MOVING_AVERAGE_CROSSOVER_RETURNS_RESPONSE,
    MULTIPLE_INCOMING_BLOCKS_OF_DIFFERENT_TYPES_RETURNS_OK,
    MULTIPLE_INCOMING_BLOCKS_OF_DIFFERENT_TYPES_RETURNS_OK_RESPONSE,
    MULTIPLE_STRATEGY_BLOCKS_RAISE_EXCEPTION,
    SINGLE_BLOCK_ALLOWING_SINGLE_INPUT_ALLOWS_BLOCKS_OF_MULTIPLE_TYPES_RETURNS_OK,
    SINGLE_BLOCK_ALLOWING_SINGLE_INPUT_ALLOWS_BLOCKS_OF_MULTIPLE_TYPES_RETURNS_OK_RESPONSE,
    SINGLE_NODE_DATA_FLOW_RETURNS_003,
    SINGLE_NODE_DATA_FLOW_RETURNS_OK,
    TWO_NODE_INVALID_CONNECTION_RETURNS_002,
    TWO_NODE_NOT_CONNECTED_RETURNS_004,
)


class SpectrumFlowValidateTest(TestCase):
    def setUp(self):
        self.auth = set_up_authentication()

    def test_empty_flow_returns_001(self):
        spectrum_event_flow = SpectrumFlow({}, [])

        self.assertDictEqual(
            spectrum_event_flow.valid,
            {
                "isValid": False,
                "code": "VALIDATE-001",
                "description": "There are no tasks to be run",
            },
        )

    def test_single_node_data_field_empty_003(self):
        spectrum_event_flow = SpectrumFlow(
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
        spectrum_event_flow = SpectrumFlow(
            SINGLE_NODE_DATA_FLOW_RETURNS_OK["nodeList"],
            SINGLE_NODE_DATA_FLOW_RETURNS_OK["edgeList"],
        )

        self.assertDictEqual(
            spectrum_event_flow.valid,
            {"isValid": True, "code": "VALIDATE-OK", "description": ""},
        )

    def test_two_nodes_invalid_connection_returns_002(self):
        spectrum_event_flow = SpectrumFlow(
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
        spectrum_event_flow = SpectrumFlow(
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

    # # TODO: Determine a case where this is valid
    # def test_multiple_blocks_not_in_assembled_dependency_list_returns_005(self):
    #     spectrum_event_flow = SpectrumFlow(
    #         MULTIPLE_BLOCKS_NOT_IN_ASSEMBLED_DEPEDENCY_LIST_RETURNS_005["nodeList"],
    #         MULTIPLE_BLOCKS_NOT_IN_ASSEMBLED_DEPEDENCY_LIST_RETURNS_005["edgeList"],
    #     )

    #     pass

    # # TODO: Determine a case where this is valid
    # def test_todo_returns_006(self):
    #     pass

    def test_invalid_block_returns_007(self):
        spectrum_event_flow = SpectrumFlow(
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
        spectrum_event_flow = SpectrumFlow(
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

    def test_using_and_block_selects_correct_payload_and_returns_ok(self):
        spectrum_event_flow = SpectrumFlow(
            AND_BLOCK_SELECTS_CORRECT_PAYLOAD_AND_RETURNS_OK["nodeList"],
            AND_BLOCK_SELECTS_CORRECT_PAYLOAD_AND_RETURNS_OK["edgeList"],
        )

        self.assertDictEqual(
            spectrum_event_flow.valid,
            {"isValid": True, "code": "VALIDATE-OK", "description": ""},
        )

        self.assertDictEqual(
            spectrum_event_flow.input_payloads,
            AND_BLOCK_SELECTS_CORRECT_PAYLOAD_AND_RETURNS_OK_RESPONSE,
        )

    def test_single_block_allowing_single_input_allows_blocks_of_multiple_types_returns_ok(
        self,
    ):
        spectrum_event_flow = SpectrumFlow(
            SINGLE_BLOCK_ALLOWING_SINGLE_INPUT_ALLOWS_BLOCKS_OF_MULTIPLE_TYPES_RETURNS_OK[
                "nodeList"
            ],
            SINGLE_BLOCK_ALLOWING_SINGLE_INPUT_ALLOWS_BLOCKS_OF_MULTIPLE_TYPES_RETURNS_OK[
                "edgeList"
            ],
        )

        self.assertDictEqual(
            spectrum_event_flow.valid,
            {"isValid": True, "code": "VALIDATE-OK", "description": ""},
        )

        self.assertDictEqual(
            spectrum_event_flow.input_payloads,
            SINGLE_BLOCK_ALLOWING_SINGLE_INPUT_ALLOWS_BLOCKS_OF_MULTIPLE_TYPES_RETURNS_OK_RESPONSE,
        )

    def test_multiple_incoming_blocks_of_different_types_returns_ok(self):
        spectrum_event_flow = SpectrumFlow(
            MULTIPLE_INCOMING_BLOCKS_OF_DIFFERENT_TYPES_RETURNS_OK["nodeList"],
            MULTIPLE_INCOMING_BLOCKS_OF_DIFFERENT_TYPES_RETURNS_OK["edgeList"],
        )

        self.assertDictEqual(
            spectrum_event_flow.valid,
            {"isValid": True, "code": "VALIDATE-OK", "description": ""},
        )

        self.assertDictEqual(
            spectrum_event_flow.input_payloads,
            MULTIPLE_INCOMING_BLOCKS_OF_DIFFERENT_TYPES_RETURNS_OK_RESPONSE,
        )

    def test_block_dne_in_assembled_dependency_list_but_in_required_fields_returns_ok(
        self,
    ):
        spectrum_event_flow = SpectrumFlow(
            BLOCK_DNE_IN_ASSEMBLED_DEPENDENCY_LIST_BUT_IN_REQUIRED_FIELDS_RETURNS_OK[
                "nodeList"
            ],
            BLOCK_DNE_IN_ASSEMBLED_DEPENDENCY_LIST_BUT_IN_REQUIRED_FIELDS_RETURNS_OK[
                "edgeList"
            ],
        )

        self.assertDictEqual(
            spectrum_event_flow.valid,
            {"isValid": True, "code": "VALIDATE-OK", "description": ""},
        )

        self.assertDictEqual(
            spectrum_event_flow.input_payloads,
            BLOCK_DNE_IN_ASSEMBLED_DEPENDENCY_LIST_BUT_IN_REQUIRED_FIELDS_RESPONSE,
        )

    def test_screener_flow_incomplete_returns_error(self):
        spectrum_event_flow = SpectrumFlow(
            FLOW_WITHOUT_SCREENER_BLOCK_RETURNS_008["nodeList"],
            FLOW_WITHOUT_SCREENER_BLOCK_RETURNS_008["edgeList"],
        )

        self.assertDictEqual(
            spectrum_event_flow.valid,
            {
                "isValid": False,
                "code": "VALIDATE-008",
                "description": "The screener being run is not complete",
            },
        )

    def test_screener_flow_complete_returns_ok(self):
        spectrum_event_flow = SpectrumFlow(
            FLOW_WITH_SCREENER_BLOCK_RETURNS_OK["nodeList"],
            FLOW_WITH_SCREENER_BLOCK_RETURNS_OK["edgeList"],
        )

        self.assertDictEqual(
            spectrum_event_flow.valid,
            {"isValid": True, "code": "VALIDATE-OK", "description": ""},
        )


class SpectrumFlowRunTest(TestCase):
    def setUp(self):
        self.auth = set_up_authentication()

    @mock.patch(
        "orchestrator.services.flow.spectrum_flow.SpectrumFlow.celery_send_helper"
    )
    def test_monitor_all(self, mock_spectrum_flow):
        mock_spectrum_flow.return_value = (
            "FOO_BLOCK-99-1",
            GenericCeleryMockClass(),
            None,
        )
        spectrum_event_flow = SpectrumFlow(
            FLOW_WITH_SCREENER_BLOCK_RETURNS_OK["nodeList"],
            FLOW_WITH_SCREENER_BLOCK_RETURNS_OK["edgeList"],
        )
        self.assertEqual(
            spectrum_event_flow.run(),
            True,
        )

    @mock.patch(
        "orchestrator.services.flow.spectrum_flow.SpectrumFlow.celery_send_helper",
        side_effect=MULTIPLE_STRATEGY_BLOCK_MOCK_RESPONSE,
    )
    def test_failure_multiple_strategy_blocks(self, mock_spectrum_flow):
        with self.assertRaises(MultipleBacktestBlocksException):
            spectrum_event_flow = SpectrumFlow(
                MULTIPLE_STRATEGY_BLOCKS_RAISE_EXCEPTION["nodeList"],
                MULTIPLE_STRATEGY_BLOCKS_RAISE_EXCEPTION["edgeList"],
            )
            spectrum_event_flow.run()
