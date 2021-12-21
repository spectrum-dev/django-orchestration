from datetime import datetime

from celery import current_app as app
from celery.result import allow_join_result

from orchestrator.exceptions import StrategyNotValidException
from orchestrator.services.flow.spectrum_flow import SpectrumFlow
from strategy.models import ScheduledStrategy


@app.task
def run_strategy(node_list, edge_list, log_trades=False):
    flow = SpectrumFlow(node_list, edge_list)
    if not flow.valid["isValid"]:
        raise StrategyNotValidException

    flow.run(log_trades=log_trades)

    return flow.outputs


@app.task
def run_screener(node_list, edge_list):
    flow = SpectrumFlow(node_list, edge_list)

    if not flow.valid["isValid"]:
        raise StrategyNotValidException

    # Retrieve the BULK_DATA_BLOCK
    block_id, bulk_data, payload = flow.get_bulk_data()

    queued_task = []
    inner_node_list = node_list
    for ticker, value in bulk_data.items():
        inner_node_list[block_id]["data"] = value
        task = app.send_task(
            "strategy.tasks.run_strategy",
            queue="backtest",
            routing_key="backtest_task",
            args=(inner_node_list, edge_list),
        )
        queued_task.append((ticker, task))

    result = []
    for ticker, task in queued_task:
        # Check the response to get all signals associated with the task
        # and check the event equal to the end_date in payload["inputs"]["end_date"]
        with allow_join_result():
            response = task.get()

            signal_key, signals = None, None
            for key in response.keys():
                if "SIGNAL_BLOCK" in key:
                    signals = response[key]
                    signal_key = key

            # target_date = payload["inputs"]["end_date"]

            for signal in signals:
                result.append({"timestamp": signal["timestamp"], "ticker": ticker})

    return {signal_key: result}


@app.task
def scheduled_run_strategy():
    scheduled_strategies = ScheduledStrategy.objects.filter(
        next_run_at__lt=datetime.utcnow()
    )
    for scheduled_strategy in scheduled_strategies:
        task = app.send_task(
            "strategy.tasks.run_strategy",
            queue="backtest",
            routing_key="backtest_task",
            args=(
                scheduled_strategy.input,
                scheduled_strategy.flow_metadata,
                True,
            ),  # Is this correct?
        )
        scheduled_strategy.save()
    return True
