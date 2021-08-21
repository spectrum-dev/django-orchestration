from ariadne import convert_kwargs_to_snake_case
from strategy.models import UserStrategy, Strategy

@convert_kwargs_to_snake_case
def list_user_strategies(*_):
    return [
        {
            "strategy_id": user_strategy.strategy,
            "strategy_name": user_strategy.strategy_name,
            "created_at": user_strategy.created_at,
            "updated_at": user_strategy.updated_at
        } for user_strategy in UserStrategy.objects.all()
    ]
    