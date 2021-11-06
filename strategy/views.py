from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import JsonResponse
from rest_framework.views import APIView

from authentication.decorators import SpectrumAuthentication, SpectrumIsAuthenticated
from strategy.models import Strategy, StrategySharing, UserStrategy

# Create your views here.


# Gets the strategy if no commit ID is provided by the latest saved version of the strategy
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
