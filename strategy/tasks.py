from celery import current_app as app

from strategy.models import Strategy, UserStrategy
from orchestrator.services.flow.spectrum_event_flow import SpectrumEventFlow

from orchestrator.exceptions import StrategyNotValidException, StrategyDoesNotExistException

@app.task
def run_strategy(user, strategy_id, commit_id, metadata, node_list, edge_list):
    try:
        flow = SpectrumEventFlow(node_list, edge_list)
        if not flow.valid["isValid"]:
            raise StrategyNotValidException
        
        # Runs Flow
        flow.run()
        
        user_strategy = UserStrategy.objects.get(strategy=strategy_id, user=user)

        Strategy.objects.update_or_create(
            strategy=user_strategy,
            commit_id=commit_id,
            flow_metadata=metadata,
            input=flow.input_payloads,
            output=flow.outputs
        )
    except UserStrategy.DoesNotExist:
        raise StrategyDoesNotExistException