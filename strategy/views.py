import uuid
import json

from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.views import APIView

from authentication.decorators import SpectrumAuthentication, SpectrumIsAuthenticated
from strategy.models import UserStrategy, Strategy

# Create your views here.


class StrategyIdView(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def get(self, request):
        strategy_id = uuid.uuid4()

        strategy_exists = UserStrategy.objects.filter(strategy=strategy_id).exists()
        if not strategy_exists:
            return JsonResponse({"strategy_id": strategy_id})
        else:
            return JsonResponse({"error": "Strategy does not exist"}, status=404)


class StrategyView(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def get(self, request, strategy_id):
        """
        Gets the latest saves strategy data
        """
        try:
            user = request.user

            user_strategy = UserStrategy.objects.filter(strategy=strategy_id, user=user)

            if user_strategy.exists():
                strategy = Strategy.objects.filter(
                    strategy=user_strategy[0],
                ).order_by("-updated_at")

                if len(strategy) > 0:
                    strategy = strategy[0]

                    response = {
                        "elements": strategy.flow_metadata,
                        "inputs": strategy.input,
                        "outputs": strategy.output,
                    }
                else:
                    response = {"elements": [], "inputs": {}, "outputs": {}}

                return JsonResponse(response)
            else:
                return JsonResponse(
                    {"error": "You are not authorized to view this strategy"},
                    status=401,
                )
        except Exception as e:
            return JsonResponse(
                {"error": "There was an unhandled error with the response"}, status=500
            )


class CommitIdView(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def get(self, request, strategy_id):
        user = request.user
        user_strategy = UserStrategy.objects.filter(strategy=strategy_id, user=user)

        if not user_strategy.exists():
            return JsonResponse({"error": "Strategy does not exist"})

        commit_id = uuid.uuid4()
        strategy_commit_pair_exist = Strategy.objects.filter(
            strategy=user_strategy[0], commit=commit_id
        ).exists()

        if not strategy_commit_pair_exist:
            return JsonResponse({"strategyId": strategy_id, "commitId": commit_id})
        else:
            return JsonResponse({"error": "Commit ID already exists"})


class StrategyCommitView(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def get(self, request, strategy_id, commit_id):
        try:
            user = request.user

            user_strategy = UserStrategy.objects.filter(strategy=strategy_id, user=user)

            if user_strategy.exists():
                strategy = Strategy.objects.get(
                    strategy=user_strategy[0],
                    commit=commit_id,
                )

                response = {
                    "elements": strategy.flow_metadata,
                    "inputs": strategy.input,
                    "outputs": strategy.output,
                }

                return JsonResponse(response)
            else:
                return JsonResponse(
                    {"error": "You are not authorized to view this strategy"},
                    status=401,
                )
        except ValidationError as e:
            return JsonResponse({"validation_error": "There was a validation error"})
        except ObjectDoesNotExist as e:
            return JsonResponse({"error": "ID does not exist"})
        except Exception as e:
            return JsonResponse(
                {"error": "There was an unhandled error with the response"}, status=500
            )

    def post(self, request, strategy_id, commit_id):
        try:
            user = request.user
            request_body = json.loads(request.body)

            user_strategy = UserStrategy.objects.filter(strategy=strategy_id, user=user)

            if not user_strategy.exists():
                user_strategy = UserStrategy.objects.create(
                    user=user, strategy=strategy_id
                )
            else:
                user_strategy = user_strategy[0]

            Strategy.objects.update_or_create(
                strategy=user_strategy,
                commit=commit_id,
                flow_metadata=request_body["metadata"],
                input=request_body["inputs"],
                output=request_body["outputs"],
            )
            return JsonResponse({"message": "Successfully saved strategy "})

        except IntegrityError:
            return JsonResponse({"error": "The strategy-commit pair already exist"})
        except ValidationError:
            return JsonResponse({"error": "There was a validation error"})
        except Exception as e:
            print(type(e))
            print(e)
            return JsonResponse({"error": "There was an error saving the strategy"})
