import json
import requests

from django.shortcuts import render

from django.http import (
    JsonResponse
)

from orchestration.settings import env

from orchestrator.models import BlockRegistry

from orchestrator.services.flow.run import run
# Create your views here.


def get_all_metadata(request):
    all_blocks_from_registry = BlockRegistry.objects.all()

    response = []
    for block_registry in all_blocks_from_registry:
        metadata = {
            "blockName": block_registry.block_name,
            "blockType": block_registry.block_type,
            "blockId": block_registry.block_id,
            "inputs": block_registry.inputs,
            "validation": block_registry.validations
        }

        response.append(metadata)

    return JsonResponse({"response": response})


def get_metadata(request, block_type, block_id):
    block_registry = BlockRegistry.objects.all().filter(block_type=block_type).filter(block_id=block_id)[0]

    metadata = {
        "blockName": block_registry.block_name,
        "blockType": block_registry.block_type,
        "blockId": block_registry.block_id,
        "inputs": block_registry.inputs,
        "validation": block_registry.validations
    }
    
    return JsonResponse(metadata)


def proxy_block_action(request, block_type, block_id, action_name):
    # TODO: Make this more generic for all URL Parameters
    potential_url_param = request.GET.get("indicatorName", None)

    if potential_url_param:
        response = requests.get(f"{env('API_BASE_URL')}/{block_type}/{block_id}/{action_name}?indicatorName={potential_url_param}")
    else:
        response = requests.get(f"{env('API_BASE_URL')}/{block_type}/{block_id}/{action_name}")

    return JsonResponse(response.json())

def post_flow(request):
    request_body = json.loads(request.body)
    spectrum_flow = run(
        request_body["nodeList"],
        request_body["edgeList"]
    )

    response = spectrum_flow.run_batched_tasks_v3()

    return JsonResponse(response)


