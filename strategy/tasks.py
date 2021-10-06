from celery import current_app as app

from strategy.models import Strategy, UserStrategy
from orchestrator.services.flow.spectrum_event_flow import SpectrumEventFlow

from orchestrator.exceptions import (
    StrategyNotValidException,
    StrategyDoesNotExistException,
)


@app.task
def run_screener(node_list, edge_list):
    flow = SpectrumEventFlow(node_list, edge_list)
    if not flow.valid["isValid"]:
        raise StrategyNotValidException

    # TODO: Need to determine how to swap the BULK_DATA_BLOCK with a normal "DATA_BLOCK" that
    #       has pre-filled data in it, then just run the run_strategy below. Batch the tasks so that you can have async behaviour
    block_id, bulk_data = flow.run_screener()
    
    print ('Block ID: ', block_id)

    results = []
    inner_node_list = node_list
    i = 0
    print ()
    print ("Starting Loop")
    print ()
    for ticker, value in bulk_data.items():
        if (i == 1):
            break
        
        inner_node_list[block_id]['data'] = value
        print ("Node List")
        print (inner_node_list)
        print ()
        task = run_strategy.delay(inner_node_list, edge_list)
        results.append(task)

        i += 1

    # queued_results = []
    # inner_node_list = node_list
    # for ticker, value in bulk_data.items():
    #     print ('Ticker: ', ticker)
    #     print ('Value: ', value)
    #     print ()
    #     output_key = ticker
    #     inner_node_list[block_id]['data'] = value
    #     task = run_strategy.delay(inner_node_list, edge_list)
    #     queued_results.append(task)
    #     # TODO: Remake the node_list with just the data
    #     # TODO: Run the run_strategy below, keeping track of all the instances running
    
    # TODO: Retrieve results and aggregate
    return {}

@app.task
def run_strategy(node_list, edge_list):
    flow = SpectrumEventFlow(node_list, edge_list)
    if not flow.valid["isValid"]:
        raise StrategyNotValidException

    flow.run()

    return flow.outputs
