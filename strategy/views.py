import uuid
import json
from django.http import (
    JsonResponse
)

from strategy.models import Strategy

# Create your views here.

def get_strategy_id(request):
    strategy_id = uuid.uuid4()

    strategy_exists = Strategy.objects.filter(strategy_id=strategy_id).exists()
    if not strategy_exists:
        return JsonResponse({"strategy_id": strategy_id})
    else:
        return JsonResponse({"error": "Strategy does not exist"})


def get_commit_id(request, strategy_id):
    strategy_exists = Strategy.objects.filter(strategy_id=strategy_id).exists()

    # if not strategy_exists:
    #     return JsonResponse({"error": "Strategy does not exist"})

    commit_id = uuid.uuid4()
    strategy_commit_pair_exist = Strategy.objects.filter(
        strategy_id=strategy_id,
        commit_id=commit_id
    )

    if not strategy_commit_pair_exist:
        return JsonResponse({
            "strategy_id": strategy_id,
            "commit_id": commit_id
        })
    else:
        return JsonResponse({"error": "Commit ID already exists"})


def save_strategy(request, strategy_id, commit_id):
    request_body = json.loads(request.body)

    try:
        Strategy.objects.create(
            strategy_id=strategy_id,
            commit_id=commit_id,
            flow_metadata=request_body["metadata"],
            input={},
            output=request_body["outputs"]
        )
        return JsonResponse({ "message": "Successfully saved strategy "})
    except:
        return JsonResponse({"error": "There was an error saving the strategy"})