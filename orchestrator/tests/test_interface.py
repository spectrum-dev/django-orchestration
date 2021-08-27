from django.test import TestCase
from orchestrator.interface import get_input_dependency_graph

from orchestrator.tests.data.test_event_flow_data import (
    MOVING_AVERAGE_CROSSOVER_RETURNS_OK,
)


class ResultsTest(TestCase):
    def test_valid_flow(self):
        response = get_input_dependency_graph(
            MOVING_AVERAGE_CROSSOVER_RETURNS_OK["nodeList"],
            MOVING_AVERAGE_CROSSOVER_RETURNS_OK["edgeList"],
        )

        self.assertDictEqual(
            response,
            {
                "1": [],
                "2": ["open", "high", "low", "close", "volume"],
                "3": ["open", "high", "low", "close", "volume"],
                "4": ["open", "high", "low", "close", "volume"],
                "5": ["timestamp", "order"],
            },
        )
