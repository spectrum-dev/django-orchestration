from celery import current_app as app
from celery.result import allow_join_result

from orchestrator.exceptions import StrategyNotValidException
from orchestrator.services.flow.spectrum_flow import SpectrumFlow


@app.task
def run_strategy(node_list, edge_list):
    flow = SpectrumFlow(node_list, edge_list)
    if not flow.valid["isValid"]:
        raise StrategyNotValidException

    flow.run()

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

            target_date = payload["inputs"]["end_date"]

            for signal in signals:
                if signal["timestamp"] == f"{target_date} 00:00:00":
                    result.append({"ticker": ticker})
                    break

    return {signal_key: result}
