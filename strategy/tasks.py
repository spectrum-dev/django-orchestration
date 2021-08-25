from celery import current_app as app

from strategy.models import Strategy, UserStrategy
from orchestrator.services.flow.spectrum_event_flow import SpectrumEventFlow

from orchestrator.exceptions import (
    StrategyNotValidException,
    StrategyDoesNotExistException,
)


@app.task
def run_strategy(node_list, edge_list):
    flow = SpectrumEventFlow(node_list, edge_list)
    if not flow.valid["isValid"]:
        raise StrategyNotValidException

    flow.run()

    return flow.outputs
