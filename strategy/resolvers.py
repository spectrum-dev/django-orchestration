from ariadne import convert_kwargs_to_snake_case

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


# Mutations
@convert_kwargs_to_snake_case
def run_strategy(*_, user, strategy_id, commit_id, metadata, node_list, edge_list):
    try:
        run_strategy.delay(user, strategy_id, commit_id, metadata, node_list, edge_list)
        return {"status": True}
    except:
        return {"status": False}
