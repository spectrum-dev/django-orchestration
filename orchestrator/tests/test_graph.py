from django.test import TestCase

from orchestrator.services.flow.graph import DependencyGraph, Graph
from orchestrator.tests.data.test_data_validation import SINGLE_FULL_FLOW_VALID


class GraphTest(TestCase):
    def test_insert_when_value_not_in_adjacency_list(self):
        graph = Graph()
        graph.insert("1", "2")
        self.assertDictEqual(graph.adjacency_list, {"1": {"2"}})


class DependencyGraphTest(TestCase):
    @staticmethod
    def test_full_single_flow():
        graph = DependencyGraph(
            SINGLE_FULL_FLOW_VALID["nodeList"], SINGLE_FULL_FLOW_VALID["edgeList"]
        )

        assert graph.graph.adjacency_list == {
            "1": {"2", "3"},
            "2": {"4"},
            "3": {"4"},
            "4": {"5"},
            "5": set(),
        }
        assert graph.dependency_graph.adjacency_list == {
            "1": set(),
            "2": {"1"},
            "3": {"1"},
            "4": {"2", "3"},
            "5": {"4"},
        }
        assert graph.batched_tasks == [{"1"}, {"2", "3"}, {"4"}, {"5"}]
