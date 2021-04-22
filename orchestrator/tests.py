import json
from django.test import TestCase, Client

from orchestrator.services.flow.run import run
from orchestrator.data.test_data import FULL_TECHNICAL_ANALYSIS_FLOW_SINGLE_FLOW

# Create your tests here.
class SpectrumFlow(TestCase):
    def test_instantiate_class(self):
        spectrum_flow = run(
            FULL_TECHNICAL_ANALYSIS_FLOW_SINGLE_FLOW["nodeList"],
            FULL_TECHNICAL_ANALYSIS_FLOW_SINGLE_FLOW["edgeList"]
        )
        
        print ("Adjacency List")
        print (spectrum_flow.graph.adjacency_list)

        print()

        print ("Dependency Graph")
        print (spectrum_flow.dependency_graph.adjacency_list)

        print()

        print ("Batches")
        print (spectrum_flow.batched_tasks)

        print()

        outputs = spectrum_flow.run_batched_tasks_v3()

        # TODO: Remove once done debugging
        with open("flow-outputs.json", "w") as outfile:
            json.dump(outputs, outfile)

        assert False

    def test_run_batched_tasks(self):
        pass