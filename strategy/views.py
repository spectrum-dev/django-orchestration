import json
import uuid

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import IntegrityError
from django.http import JsonResponse
from rest_framework.views import APIView

from authentication.decorators import SpectrumAuthentication, SpectrumIsAuthenticated
from strategy.models import Strategy, StrategySharing, UserStrategy

# Create your views here.


class StrategyDetailView(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def get(self, request, strategy_id):
        try:
            strategy = UserStrategy.objects.get(strategy=strategy_id)
            return JsonResponse(
                {"strategy_id": strategy_id, "strategy_name": strategy.strategy_name}
            )
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Strategy does not exist"}, status=404)


class DeleteStrategyView(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def post(self, request, strategy_id):
        try:
            user = request.user
            UserStrategy.objects.get(user=user, strategy=strategy_id).delete()
            return JsonResponse({"status": "true"})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Strategy ID does not exist"}, status=404)
        except Exception as e:
            print("Exception: ", e)
            return JsonResponse({"error": "Unhandled Error"}, status=400)


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
            strategy_sharing = StrategySharing.objects.filter(
                strategy__strategy=strategy_id, user=user
            )

            if user_strategy.exists() or strategy_sharing.exists():
                strategy = Strategy.objects.filter(
                    strategy__strategy=strategy_id,
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
        except Exception:
            return JsonResponse(
                {"error": "There was an unhandled error with the response"}, status=500
            )


class CommitIdView(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def get(self, request, strategy_id):
        user = request.user

        user_strategy = UserStrategy.objects.filter(strategy=strategy_id, user=user)
        sharing_strategy = StrategySharing.objects.filter(
            strategy__strategy=strategy_id, user=user
        )

        if not user_strategy.exists() and not sharing_strategy.exists():
            return JsonResponse({"error": "Strategy does not exist"}, status=404)

        commit_id = uuid.uuid4()
        strategy_commit_pair_exist = Strategy.objects.filter(
            strategy__strategy=strategy_id, commit=commit_id
        ).exists()

        if not strategy_commit_pair_exist:
            return JsonResponse({"strategyId": strategy_id, "commitId": commit_id})
        else:
            return JsonResponse({"error": "Commit ID already exists"}, status=400)


class StrategyCommitView(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    # TODO: This needs to be updated to support sharing
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
        except ValidationError:
            return JsonResponse({"validation_error": "There was a validation error"})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "ID does not exist"})
        except Exception:
            return JsonResponse(
                {"error": "There was an unhandled error with the response"}, status=500
            )

    def post(self, request, strategy_id, commit_id):
        try:
            user = request.user
            request_body = json.loads(request.body)

            user_strategy = UserStrategy.objects.filter(strategy=strategy_id, user=user)
            strategy_sharing = StrategySharing.objects.filter(
                strategy__strategy=strategy_id, user=user
            )

            if not user_strategy.exists() and not strategy_sharing.exists():
                return JsonResponse(
                    {"error": "This strategy does not exist"}, status=401
                )

            strategy = None
            if user_strategy.exists():
                strategy = user_strategy.first()

            if strategy_sharing.exists():
                if strategy_sharing.first().permissions == 1:
                    return JsonResponse(
                        {"error": "You only have read permissions on this strategy"}
                    )

                strategy = strategy_sharing.first().strategy

            Strategy.objects.update_or_create(
                strategy=strategy,
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
