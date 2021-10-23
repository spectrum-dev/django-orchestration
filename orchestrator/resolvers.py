from orchestrator.interface import (
    get_input_dependency_graph as get_input_dependency_graph_interface,
)
from orchestrator.models import BlockRegistry


# Queries
def get_input_dependency_graph(*_, nodeList, edgeList):
    response = get_input_dependency_graph_interface(nodeList, edgeList)
    return response


def get_all_metadata(*_):
    all_blocks_from_registry = BlockRegistry.objects.all()
    response = {}
    for block_registry in all_blocks_from_registry:
        if block_registry.block_type not in response:
            response[block_registry.block_type] = {}

        if block_registry.block_id not in response[block_registry.block_type]:
            response[block_registry.block_type][block_registry.block_id] = {
                "blockName": block_registry.block_name,
                "blockMetadata": f"/orchestration/{block_registry.block_type}/{block_registry.block_id}/",
            }
    return response
