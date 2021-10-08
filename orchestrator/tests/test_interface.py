from django.test import TestCase
from orchestrator.interface import get_input_dependency_graph

from orchestrator.tests.data.test_flow_data import (
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
                "2": {
                    "1": {
                        "name": "US Stock Data",
                        "outputInterface": ["open", "high", "low", "close", "volume"],
                    }
                },
                "3": {
                    "1": {
                        "name": "US Stock Data",
                        "outputInterface": ["open", "high", "low", "close", "volume"],
                    }
                },
                "4": {
                    "3": {"name": "Technical Indicators", "outputInterface": ["data"]},
                    "2": {"name": "Technical Indicators", "outputInterface": ["data"]},
                },
                "5": {
                    "4": {
                        "name": "Intersect",
                        "outputInterface": ["timestamp", "order"],
                    }
                },
            },
        )
