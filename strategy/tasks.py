from celery import current_app as app

from strategy.models import Strategy, UserStrategy
from orchestrator.services.flow.spectrum_event_flow import SpectrumEventFlow

from orchestrator.exceptions import (
    StrategyNotValidException,
    StrategyDoesNotExistException,
)


@app.task
def run_strategy(
    user_id, strategy_id, commit_id, metadata, inputs, node_list, edge_list
):
    try:
        flow = SpectrumEventFlow(node_list, edge_list)
        if not flow.valid["isValid"]:
            raise StrategyNotValidException

        # Runs Flow
        flow.run()

        user_strategy = UserStrategy.objects.get(strategy=strategy_id, user_id=user_id)

        strategy = Strategy.objects.get(strategy=user_strategy, commit=commit_id)

        # Updates the existing object
        strategy.flow_metadata = metadata
        strategy.input = inputs
        strategy.output = flow.outputs
        strategy.save()

    except UserStrategy.DoesNotExist:
        raise StrategyDoesNotExistException
    except Strategy.DoesNotExist:
        Strategy.objects.create(
            strategy=user_strategy,
            commit=commit_id,
            flow_metadata=metadata,
            input=inputs,
            output=flow.outputs,
        )
