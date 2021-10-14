from django.test import TestCase

from strategy.tasks import run_screener

class SpectrumFlowRunScreener(TestCase):
    def test_debug(self):
        node_list = {
            1: {
                "blockId": 1,
                "blockType": "BULK_DATA_BLOCK",
                "candlestick": { "value": "1day", "options": [] },
                "start_date": { "value": "2021-08-26", "rawValue": "2021-09-26T22:58:13.000Z" },
                "end_date": { "value": "2021-10-05", "rawValue": "2021-10-05T22:58:13.842Z" },
                "exchange_name": { "value": "KLSE", "options": [] },
            },
            2: {
                "blockType": "COMPUTATIONAL_BLOCK",
                "blockId": 1,
                "indicator_name": {
                    "options": [],
                    "value": "MA",
                    "onChange": "indicatorField?indicatorName="
                },
                "incoming_data": {
                    "value": "close"
                },
                "lookback_period": {
                    "value": "3"
                }
            },
            3: {
                "blockType": "SIGNAL_BLOCK",
                "blockId": 2,
                "incoming_data": {
                    "inputFromConnectionValue": "",
                    "value": "data"
                },
                "saddle_type": {
                    "options": [],
                    "value": "UPWARD"
                },
                "event_action": {
                    "options": [],
                    "value": "BUY"
                },
                "consecutive_up": {
                    "value": "1"
                },
                "consecutive_down": {
                    "value": "1"
                }
            },
        }
        edge_list = [
            {
                "source": "1",
                "sourceHandle": "output_id888",
                "target": "2",
                "targetHandle": "input_id891",
                "type": "edge",
                "id": "reactflow__edge-1output_id888-2input_id891",
            },
            {
                "source": "2",
                "sourceHandle": "output_id1356",
                "target": "3",
                "targetHandle": "input_id1363",
                "type": "edge",
                "id": "reactflow__edge-2output_id1356-4input_id1363",
            }
        ]

        task = run_screener.delay(node_list, edge_list)
        assert False
    