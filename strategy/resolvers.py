from ariadne import convert_kwargs_to_snake_case
from celery import current_app
from celery.result import AsyncResult

from django.contrib.auth.models import User

from strategy.tasks import run_strategy
from strategy.models import UserStrategy, Strategy, StrategySharing

# Queries
@convert_kwargs_to_snake_case
def list_user_strategies(_, info):
    return [
        {
            "strategy_id": user_strategy.strategy,
            "strategy_name": user_strategy.strategy_name,
            "created_at": user_strategy.created_at,
            "updated_at": user_strategy.updated_at,
        }
        for user_strategy in UserStrategy.objects.filter(user=info.context["user"])
    ]


@convert_kwargs_to_snake_case
def list_strategies(_, info):
    return [
        {
            "strategy": strategy.strategy,
            "commit_id": strategy.commit,
            "flow_metadata": strategy.flow_metadata,
            "input": strategy.input,
            "output": strategy.output,
            "created_at": strategy.created_at,
            "updated_at": strategy.updated_at,
        }
        for strategy in Strategy.objects.filter(strategy__user=info.context["user"])
    ]


def get_task_result(*_, taskId):
    task = AsyncResult(taskId)
    if not task.status == "SUCCESS":
        return {
            "status": task.status,
            "output": None,
        }

    return {
        "status": task.status,
        "output": task.get(),
    }


# Mutations
def dispatch_run_strategy(*_, nodeList, edgeList, strategyType):
    if strategyType == "SCREENER":
        task = current_app.send_task(
            "strategy.tasks.run_screener",
            queue="screener",
            routing_key="screener_task",
            args=(nodeList, edgeList),
        )
        return {"status": True, "task_id": task.task_id}
    elif strategyType == "BACKTEST":
        task = current_app.send_task(
            "strategy.tasks.run_strategy",
            queue="backtest",
            routing_key="backtest_task",
            args=(nodeList, edgeList),
        )
        return {"status": True, "task_id": task.task_id}
    else:
        return {"status": False, "task_id": None}


@convert_kwargs_to_snake_case
def share_strategy(*_, strategy_id, email, permissions):
    user_strategy = UserStrategy.objects.get(strategy=strategy_id)
    user = User.objects.get(email=email)

    StrategySharing.objects.update_or_create(
        strategy=user_strategy, user=user, permissions=permissions
    )

    return {"shared": True}
