from orchestrator.interface import (
    get_input_dependency_graph as get_input_dependency_graph_interface,
)


# Queries
def get_input_dependency_graph(*_, nodeList, edgeList):
    response = get_input_dependency_graph_interface(nodeList, edgeList)
    return response
