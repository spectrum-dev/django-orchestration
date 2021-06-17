import uuid
import json

from django.http import JsonResponse
from rest_framework.views import APIView

from authentication.decorators import SpectrumAuthentication, SpectrumIsAuthenticated
from strategy.models import UserStrategy, Strategy

# Create your views here.


class StrategyIdView(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def get(self, request):
        strategy_id = uuid.uuid4()
        user = request.user

        strategy_exists = UserStrategy.objects.filter(strategy=strategy_id, user=user).exists()
        if not strategy_exists:
            return JsonResponse({"strategy_id": strategy_id})
        else:
            return JsonResponse({"error": "Strategy does not exist"})

class StrategyView(APIView):
    authentication_classes = [SpectrumAuthentication]
    permission_classes = [SpectrumIsAuthenticated]

    def get(self, request, strategy_id):
        try:
          user = request.user

          user_strategy = UserStrategy.objects.filter(strategy=strategy_id, user=user)
        
          print ('User Strategy: ', user_strategy)
          if (user_strategy.exists()):
              print ('User strategy exists')
              strategy = Strategy.objects.filter(
                strategy=user_strategy[0],
              ).order_by('-updated_at')

              if len(strategy) > 0:
                strategy = strategy[0]
                print ('Strategy: ', strategy)

                response = {
                  'elements': strategy.flow_metadata,
                  'inputs': strategy.input,
                  'outputs': strategy.output,
                }
              else:
                print ('User strategy DNE')
                response = {
                    'elements': [],
                    'inputs': {},
                    'outputs': {}
                }

              return JsonResponse(response)
          else:
            return JsonResponse({'error': 'You are not authorized to view this strategy'}, status=401)
        except Exception as e:
          return JsonResponse({ 'error': 'There was an unhandled error with the response'}, status=500)


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
          
          if (user_strategy.exists()):
              strategy = Strategy.objects.get(
                strategy=user_strategy[0],
                commit=commit_id,
              )

              response = {
                'elements': strategy.flow_metadata,
                'inputs': strategy.input,
                'outputs': strategy.output,
              }

              return JsonResponse(response)
          else:
            return JsonResponse({'error': 'You are not authorized to view this strategy'}, status=401)
        except Exception as e:
          return JsonResponse({ 'error': 'There was an unhandled error with the response'}, status=500)

    def post(self, request, strategy_id, commit_id):
        try:
            user = request.user
            request_body = json.loads(request.body)

            user_strategy = UserStrategy.objects.filter(strategy=strategy_id, user=user)
            
            if (not user_strategy.exists()):
                user_strategy = UserStrategy.objects.create(
                    user=user,
                    strategy=strategy_id
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
        except Exception as e:
            print (e)
            return JsonResponse({"error": "There was an error saving the strategy"})
