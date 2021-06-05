import json
import requests

from django.shortcuts import render
from django.http import JsonResponse

from orchestration.settings import env
from orchestrator.models import BlockRegistry
from orchestrator.services.flow.run import run
from orchestrator.services.flow.spectrum_flow_v2 import SpectrumFlow


def get_all_metadata(request):
    all_blocks_from_registry = BlockRegistry.objects.all()

    response = {}
    for block_registry in all_blocks_from_registry:
        response = {
            **response,
            block_registry.block_type: {
                block_registry.block_id: {
                    "blockName": block_registry.block_name,
                    "blockMetadata": f"/orchestration/${block_registry.block_type}/${block_registry.block_id}/",
                }
            },
        }

    return JsonResponse({"response": response})


def get_metadata(request, block_type, block_id):
    block_registry = (
        BlockRegistry.objects.all()
        .filter(block_type=block_type)
        .filter(block_id=block_id)[0]
    )

    metadata = {
        "blockName": block_registry.block_name,
        "blockType": block_registry.block_type,
        "blockId": block_registry.block_id,
        "inputs": block_registry.inputs,
        "validation": block_registry.validations,
    }

    return JsonResponse(metadata)


def proxy_block_action(request, block_type, block_id, action_name):
    # TODO: Make this more generic for all URL Parameters
    potential_url_param = request.GET.get("indicatorName", None)
    potential_url_param_two = request.GET.get("name", None)

    if potential_url_param:
        response = requests.get(
            f"{env('API_BASE_URL')}/{block_type}/{block_id}/{action_name}?indicatorName={potential_url_param}"
        )
    elif potential_url_param_two:
        response = requests.get(
            f"{env('API_BASE_URL')}/{block_type}/{block_id}/{action_name}?name={potential_url_param_two}"
        )
    else:
        print(
            "Request URL: ",
            f"{env('API_BASE_URL')}/{block_type}/{block_id}/{action_name}",
        )
        response = requests.get(
            f"{env('API_BASE_URL')}/{block_type}/{block_id}/{action_name}"
        )

    return JsonResponse(response.json())


def validate_flow(request):
    request_body = json.loads(request.body)

    flow = SpectrumFlow(request_body["nodeList"], request_body["edgeList"])

    return JsonResponse({"valid": flow.is_valid})


def post_flow(request):
    request_body = json.loads(request.body)

    flow = SpectrumFlow(request_body["nodeList"], request_body["edgeList"])

    response = flow.run(mode="RUN")

    return JsonResponse({"response": response})
