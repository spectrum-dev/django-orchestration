from django.test import TestCase
from unittest.mock import patch

from strategy.tasks import run_screener

def demo_function():
    return "TEST"

class TestRunScreener(TestCase):
    @patch('strategy.tasks.run_screener', demo_function)
    def test_debug(self):
        node_list = {
            1: {
                "blockId": 1,
                "blockType": "BULK_DATA_BLOCK",
                "candlestick": { "value": "1day", "options": [] },
                "start_date": { "value": "2021-09-26", "rawValue": "2021-09-26T22:58:13.000Z" },
                "end_date": { "value": "2021-10-05", "rawValue": "2021-10-05T22:58:13.842Z" },
                "exchange_name": { "value": "KLSE", "options": [] },
            }
        }
        edge_list = []

        task = run_screener.delay(node_list, edge_list)
        print (task.name)
        print (task.status)
        print (task.get())

        assert False