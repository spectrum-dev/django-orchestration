import json
from os import environ

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.views import APIView

from authentication.decorators import SpectrumAuthentication, SpectrumIsAuthenticated
from orchestrator.models import BlockRegistry
from orchestrator.services.overlays.main import main


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
        except Exception:
            return JsonResponse({"error": "Unhandled error"})


class RunOverlay(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def post(self, request):
        request_body = json.loads(request.body)

        response = main(request_body)

        return JsonResponse({"response": response})
