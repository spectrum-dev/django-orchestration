import json
from django.test import TestCase, Client

from orchestrator.services.flow.spectrum_flow_v2 import DependencyGraph, SpectrumFlow

# Test Data
from orchestrator.data.test_data_validation import SINGLE_FULL_FLOW


class DependencyGraphTest(TestCase):
    def test_full_single_flow(self):
        graph = DependencyGraph(SINGLE_FULL_FLOW["nodeList"], SINGLE_FULL_FLOW["edgeList"])

        assert (graph.graph.adjacency_list == {'1': {'2', '3'}, '2': {'4'}, '3': {'4'}, '4': {'5'}, '5': set()})
        assert (graph.dependency_graph.adjacency_list == {'1': set(), '2': {'1'}, '3': {'1'}, '4': {'2', '3'},
                                                          '5': {'4'}})
        assert (graph.batched_tasks == [{'1'}, {'2', '3'}, {'4'}, {'5'}])


class SpectrumFlowValidateTest(TestCase):
    def test_full_single_flow(self):
        flow = SpectrumFlow(SINGLE_FULL_FLOW["nodeList"], SINGLE_FULL_FLOW["edgeList"])

        assert flow.is_valid is True


class SpectrumFlowRunTest(TestCase):
    def test_full_single_flow(self):
        pass
