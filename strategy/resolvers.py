from ariadne import convert_kwargs_to_snake_case
from celery.result import AsyncResult

from strategy.tasks import run_strategy
from strategy.models import UserStrategy, Strategy

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


@convert_kwargs_to_snake_case
def get_task_status(*_, task_id):
    task = AsyncResult(task_id)
    return {"status": task.status}


# Mutations
def dispatch_run_strategy(
    _, info, strategyId, commitId, metadata, inputs, nodeList, edgeList
):
    task = run_strategy.delay(
        info.context["user"].id, strategyId, commitId, metadata, inputs, nodeList, edgeList
    )
    return {"status": True, "task_id": task.task_id}
