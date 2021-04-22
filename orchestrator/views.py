import json
from django.shortcuts import render

from django.http import (
    JsonResponse
)

from orchestrator.models import BlockRegistry

# Create your views here.

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

def post_flow(request):
    request_body = json.loads(request.body)

    return JsonResponse({})


