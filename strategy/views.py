import uuid
import json

from django.http import JsonResponse
from rest_framework.views import APIView

from authentication.decorators import SpectrumAuthentication, SpectrumIsAuthenticated
from strategy.models import Strategy

# Create your views here.


class StrategyIdView(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def get(self, request):
        strategy_id = uuid.uuid4()

        strategy_exists = Strategy.objects.filter(strategy_id=strategy_id).exists()
        if not strategy_exists:
            return JsonResponse({"strategy_id": strategy_id})
        else:
            return JsonResponse({"error": "Strategy does not exist"})


class CommitIdView(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def get(self, request, strategy_id):
        # strategy_exists = Strategy.objects.filter(strategy_id=strategy_id).exists()

        # if not strategy_exists:
        #     return JsonResponse({"error": "Strategy does not exist"})

        commit_id = uuid.uuid4()

        strategy_commit_pair_exist = Strategy.objects.filter(
            strategy_id=strategy_id, commit_id=commit_id
        )

        if not strategy_commit_pair_exist:
            return JsonResponse({"strategy_id": strategy_id, "commit_id": commit_id})
        else:
            return JsonResponse({"error": "Commit ID already exists"})


class SaveStrategyView(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def post(self, request, strategy_id, commit_id):
        try:
            user = request.user
            request_body = json.loads(request.body)

            Strategy.objects.create(
                strategy_id=strategy_id,
                commit_id=commit_id,
                user=user,
                flow_metadata=request_body["metadata"],
                input={},
                output=request_body["outputs"],
            )
            return JsonResponse({"message": "Successfully saved strategy "})
        except Exception:
            return JsonResponse({"error": "There was an error saving the strategy"})
