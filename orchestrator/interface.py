from orchestrator.models import BlockRegistry
from orchestrator.exceptions import BlockDoesNotExist
from orchestrator.services.flow.spectrum_event_flow import SpectrumEventFlow


def get_input_dependency_graph(node_list, edge_list):
    """
    Forms a dependency graph and maps every block to the inputs it has access to
    
    Inputs
    ---
    node_list: Dict[block_id_in_flow(string), block_data(json)]
    edge_list: List[edge pairing]

    Outputs
    ---
    {
        [block_id_in_flow]: [list of available input fields]
    }
    """
    flow = SpectrumEventFlow(node_list, edge_list)

    input_dependency_graph = {}
    for key, dependencies in flow.dependency_graph.items():
        if not dependencies:
            input_dependency_graph[key] = []

        for dependency_block_id in list(dependencies):
            try:
                block = flow.get_block_in_flow_by_id(dependency_block_id)
                block_metadata = BlockRegistry.objects.get(
                    block_id=block["blockId"], block_type=block["blockType"]
                )
                input_dependency_graph[key] = block_metadata.output_interface[
                    "interface"
                ]
            except BlockRegistry.DoesNotExist:
                raise BlockDoesNotExist

    return input_dependency_graph
