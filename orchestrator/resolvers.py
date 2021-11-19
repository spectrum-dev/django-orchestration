from ariadne import convert_kwargs_to_snake_case
from django.db.models import Max

from orchestrator.interface import (
    get_input_dependency_graph as get_input_dependency_graph_interface,
)
from orchestrator.models import BlockRegistry
from orchestrator.services.flow.spectrum_flow import SpectrumFlow


# Queries
def get_input_dependency_graph(*_, nodeList, edgeList):
    response = get_input_dependency_graph_interface(nodeList, edgeList)
    return response


def get_block_metadata(*_, blockType, blockId):
    try:
        block_registry = BlockRegistry.objects.get(
            block_type=blockType, block_id=blockId
        )

        return {
            "block_name": block_registry.block_name,
            "block_type": block_registry.block_type,
            "block_id": block_registry.block_id,
            "inputs": block_registry.inputs,
            "validation": block_registry.validations,
            "output_interface": block_registry.output_interface,
        }

    except BlockRegistry.DoesNotExist:
        return Exception("Block Type - ID Pair does not exist")
    except Exception:
        return Exception("There was an unhandled error retrieving the block metadata")


@convert_kwargs_to_snake_case
def get_all_metadata(*_, strategy_type):
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

    if strategy_type == "SCREENER":
        del response["STRATEGY_BLOCK"]

    return response


@convert_kwargs_to_snake_case
def create_block_metadata(
    *_, block_type, block_name, inputs, validations, output_interface
):
    block_id = BlockRegistry.objects.filter(block_type=block_type).aggregate(
        max_block_id=Max("block_id")
    )["max_block_id"]
    # block_id will be None if corresponding block_type DNE yet, in which case we want to start ID at 1
    block_id = (block_id or 0) + 1

    block_registry = BlockRegistry.objects.create(
        block_type=block_type,
        block_id=block_id,
        block_name=block_name,
        inputs=inputs,
        validations=validations,
        output_interface=output_interface,
    )
    return {
        "unique_block_id": block_registry.id,
        "block_id": block_registry.block_id,
        "status": True,
    }


def get_validate_flow(*_, nodeList, edgeList):
    if nodeList is not {} and edgeList is not []:
        flow = SpectrumFlow(nodeList, edgeList)
        return {"valid": flow.valid["isValid"], "edges": flow.edge_validation}
    else:
        return {"valid": False}
