from celery import current_app as app

from orchestrator.exceptions import StrategyNotValidException
from orchestrator.services.flow.spectrum_flow import SpectrumEventFlow


@app.task
def run_strategy(node_list, edge_list):
    flow = SpectrumEventFlow(node_list, edge_list)
    if not flow.valid["isValid"]:
        raise StrategyNotValidException

    flow.run()

    return flow.outputs
