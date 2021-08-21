from ariadne import convert_kwargs_to_snake_case
from strategy.models import UserStrategy, Strategy

@convert_kwargs_to_snake_case
def list_user_strategies(*_):
    return [
        {
            "strategy": user_strategy.strategy,
            "strategy_name": user_strategy.strategy_name,
            "created_at": user_strategy.created_at,
            "updated_at": user_strategy.updated_at
        } for user_strategy in UserStrategy.objects.all()
    ]
    
def list_strategies(*_):
    return [
        {
            "strategy": strategy.strategy,
            "commit": strategy.commit,
            "flow_metadata": strategy.flow_metadata,
            "input": strategy.input,
            "output": strategy.output,
            "created_at": strategy.created_at,
            "updated_at": strategy.updated_at
        } for strategy in Strategy.objects.all()
    ]