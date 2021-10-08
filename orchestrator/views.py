import json
import requests
from os import environ

from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView

from authentication.decorators import SpectrumAuthentication, SpectrumIsAuthenticated

from orchestrator.models import BlockRegistry
from orchestrator.services.overlays.main import main
from orchestrator.services.flow.spectrum_flow import SpectrumFlow


class AllMetadataView(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def get(self, request):
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

        return JsonResponse({"response": response})


class MetadataView(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def get(self, request, block_type, block_id):
        try:
            block_registry = BlockRegistry.objects.get(
                block_type=block_type, block_id=block_id
            )

            metadata = {
                "blockName": block_registry.block_name,
                "blockType": block_registry.block_type,
                "blockId": block_registry.block_id,
                "inputs": block_registry.inputs,
                "validation": block_registry.validations,
                "outputInterface": block_registry.output_interface,
            }

            return JsonResponse(metadata)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Block Type - ID Pair does not exist"})
        except Exception as e:
            print(type(e))
            print(e)
            return JsonResponse({"error": "Unhandled error"})


class ProxyBlockActionView(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def get(self, request, block_type, block_id, action_name):
        try:
            # TODO: Make this more generic for all URL Parameters
            potential_url_param = request.GET.get("indicatorName", None)
            potential_url_param_two = request.GET.get("name", None)

            if potential_url_param:
                response = requests.get(
                    f"{environ['API_BASE_URL']}/{block_type}/{block_id}/{action_name}?indicatorName={potential_url_param}"
                )
            elif potential_url_param_two:
                response = requests.get(
                    f"{environ['API_BASE_URL']}/{block_type}/{block_id}/{action_name}?name={potential_url_param_two}"
                )
            else:
                response = requests.get(
                    f"{environ['API_BASE_URL']}/{block_type}/{block_id}/{action_name}"
                )

            return JsonResponse(response.json())
        except Exception as e:
            return JsonResponse({"error": "Unhandled error"})


class ValidateFlow(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def post(self, request):
        request_body = json.loads(request.body)

        if request_body["nodeList"] is not {} and request_body["edgeList"] is not []:
            flow = SpectrumFlow(request_body["nodeList"], request_body["edgeList"])

            response = {"valid": flow.is_valid, "edges": flow.edge_validation}
            if flow.is_valid_description:
                response["error"] = flow.is_valid_description
            return JsonResponse(response)
        else:
            return JsonResponse({"valid": False, "error": "The strategy is empty"})


class RunOverlay(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def post(self, request):
        request_body = json.loads(request.body)

        response = main(request_body)

        return JsonResponse({"response": response})
