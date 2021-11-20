SINGLE_NODE_DATA_FLOW_RETURNS_OK = {
    "nodeList": {
        "1": {
            "blockType": "DATA_BLOCK",
            "blockId": 1,
            "equity_name": {"value": "AAPL", "options": []},
            "data_type": {
                "value": "intraday",
                "options": ["intraday", "daily_adjusted"],
            },
            "interval": {"value": "1min", "options": ["1min"]},
            "outputsize": {"value": "compact", "options": ["compact", "full"]},
            "start_date": {"value": "2021-06-21 19:58:00"},
            "end_date": {"value": "2021-06-21 20:00:00"},
        },
    },
    "edgeList": [],
}

SINGLE_NODE_DATA_FLOW_RETURNS_003 = {
    "nodeList": {
        "1": {
            "blockType": "DATA_BLOCK",
            "blockId": 1,
            "equity_name": {"value": "AAPL", "options": []},
            "data_type": {
                "value": "intraday",
                "options": ["intraday", "daily_adjusted"],
            },
            "interval": {"value": "1min", "options": ["1min"]},
            "outputsize": {"value": "compact", "options": ["compact", "full"]},
            "start_date": {"value": "2021-06-21 19:58:00"},
            "end_date": {"value": ""},
        },
    },
    "edgeList": [],
}

TWO_NODE_NOT_CONNECTED_RETURNS_004 = {
    "nodeList": {
        "1": {
            "blockType": "DATA_BLOCK",
            "blockId": 1,
            "equity_name": {"value": "AAPL", "options": []},
            "data_type": {
                "value": "intraday",
                "options": ["intraday", "daily_adjusted"],
            },
            "interval": {"value": "1min", "options": ["1min"]},
            "outputsize": {"value": "compact", "options": ["compact", "full"]},
            "start_date": {"value": "2021-06-21 19:58:00"},
            "end_date": {"value": "2021-06-21 20:00:00"},
        },
        "2": {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 1,
            "indicator_name": {"value": "MA", "options": []},
            "lookback_period": {"value": "2"},
            "lookback_unit": {"value": "DATA_POINT"},
        },
    },
    "edgeList": [],
}

TWO_NODE_INVALID_CONNECTION_RETURNS_002 = {
    "nodeList": {
        "1": {
            "blockType": "DATA_BLOCK",
            "blockId": 1,
            "equity_name": {"value": "AAPL", "options": []},
            "data_type": {
                "value": "intraday",
                "options": ["intraday", "daily_adjusted"],
            },
            "interval": {"value": "1min", "options": ["1min"]},
            "outputsize": {"value": "compact", "options": ["compact", "full"]},
            "start_date": {"value": "2021-06-21 19:58:00"},
            "end_date": {"value": "2021-06-21 20:00:00"},
        },
        "2": {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 1,
            "event_type": {"value": "INTERSECT"},
            "event_action": {"value": "BUY"},
        },
    },
    "edgeList": [
        {
            "source": "1",
            "sourceHandle": "output_id888",
            "target": "2",
            "targetHandle": "input_id891",
            "type": "edge",
            "id": "reactflow__edge-1output_id888-2input_id891",
        },
    ],
}

MULTIPLE_BLOCKS_NOT_IN_ASSEMBLED_DEPEDENCY_LIST_RETURNS_005 = {
    "nodeList": {},
    "edgeList": [],
}

INVALID_BLOCK_RETURNS_007 = {
    "nodeList": {
        "2": {
            "blockType": "INVALID_BLOCK",
            "blockId": 1,
            "event_type": {"value": "INTERSECT"},
            "event_action": {"value": "BUY"},
        },
    },
    "edgeList": [],
}

MOVING_AVERAGE_CROSSOVER_RETURNS_OK = {
    "nodeList": {
        "1": {
            "blockType": "DATA_BLOCK",
            "blockId": 1,
            "equity_name": {"value": "AAPL", "options": []},
            "candlestick": {"value": "1month", "options": ["1min", "1month"]},
            "start_date": {"value": "2021-05-28 00:00:00"},
            "end_date": {"value": "2021-07-30 00:00:00"},
        },
        "2": {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 1,
            "indicator_name": {"value": "MA", "options": []},
            "lookback_period": {"value": "2"},
            "lookback_unit": {"value": "DATA_POINT"},
        },
        "3": {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 1,
            "indicator_name": {"value": "MA"},
            "lookback_period": {"value": "1"},
            "lookback_unit": {"value": "DATA_POINT"},
        },
        "4": {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 1,
            "event_action": {"value": "BUY"},
        },
        "5": {
            "blockType": "STRATEGY_BLOCK",
            "blockId": 1,
            "start_value": {"value": 10000.00},
            "commission": {"value": 4.95},
            "impact": {"value": 0.01},
            "stop_loss": {"value": 0.1},
            "take_profit": {"value": 0.1},
            "trade_amount_value": {"value": 10.00},
            "trade_amount_unit": {"value": "PERCENTAGE"},
        },
    },
    "edgeList": [
        {
            "source": "1",
            "sourceHandle": "output_id888",
            "target": "2",
            "targetHandle": "input_id891",
            "type": "edge",
            "id": "reactflow__edge-1output_id888-2input_id891",
        },
        {
            "source": "1",
            "sourceHandle": "output_id1136",
            "target": "3",
            "targetHandle": "input_id1143",
            "type": "edge",
            "id": "reactflow__edge-1output_id1136-3input_id1143",
        },
        {
            "source": "2",
            "sourceHandle": "output_id1356",
            "target": "4",
            "targetHandle": "input_id1363",
            "type": "edge",
            "id": "reactflow__edge-2output_id1356-4input_id1363",
        },
        {
            "source": "3",
            "sourceHandle": "output_id1576",
            "target": "4",
            "targetHandle": "input_id1579",
            "type": "edge",
            "id": "reactflow__edge-3output_id1576-4input_id1579",
        },
        {
            "source": "4",
            "sourceHandle": "output_id1796",
            "target": "5",
            "targetHandle": "input_id1799",
            "type": "edge",
            "id": "reactflow__edge-4output_id1796-5input_id1799",
        },
    ],
}

MOVING_AVERAGE_CROSSOVER_RETURNS_RESPONSE = {
    "1": {
        "inputs": {
            "equity_name": "AAPL",
            "candlestick": "1month",
            "start_date": "2021-05-28 00:00:00",
            "end_date": "2021-07-30 00:00:00",
        },
        "outputs": {"ref": set()},
        "blockType": "DATA_BLOCK",
        "blockId": 1,
    },
    "3": {
        "inputs": {
            "indicator_name": "MA",
            "lookback_period": "1",
            "lookback_unit": "DATA_POINT",
        },
        "outputs": {"ref": {"1"}},
        "blockType": "COMPUTATIONAL_BLOCK",
        "blockId": 1,
    },
    "2": {
        "inputs": {
            "indicator_name": "MA",
            "lookback_period": "2",
            "lookback_unit": "DATA_POINT",
        },
        "outputs": {"ref": {"1"}},
        "blockType": "COMPUTATIONAL_BLOCK",
        "blockId": 1,
    },
    "4": {
        "inputs": {"event_action": "BUY"},
        "outputs": {"ref": {"3", "2"}},
        "blockType": "SIGNAL_BLOCK",
        "blockId": 1,
    },
    "5": {
        "inputs": {
            "start_value": 10000.0,
            "commission": 4.95,
            "impact": 0.01,
            "stop_loss": 0.1,
            "take_profit": 0.1,
            "trade_amount_value": 10.0,
            "trade_amount_unit": "PERCENTAGE",
        },
        "outputs": {"ref": {"1", "4"}},
        "blockType": "STRATEGY_BLOCK",
        "blockId": 1,
    },
}

AND_BLOCK_SELECTS_CORRECT_PAYLOAD_AND_RETURNS_OK = {
    "nodeList": {
        "1": {
            "blockType": "DATA_BLOCK",
            "blockId": 1,
            "equity_name": {"value": "AAPL", "options": []},
            "candlestick": {"value": "1month", "options": ["1min", "1month"]},
            "start_date": {"value": "2021-05-28 00:00:00"},
            "end_date": {"value": "2021-07-30 00:00:00"},
        },
        "2": {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 1,
            "indicator_name": {"value": "MA", "options": []},
            "lookback_period": {"value": "2"},
            "lookback_unit": {"value": "DATA_POINT"},
        },
        "3": {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 1,
            "indicator_name": {"value": "MA"},
            "lookback_period": {"value": "1"},
            "lookback_unit": {"value": "DATA_POINT"},
        },
        "4": {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 1,
            "event_action": {"value": "BUY"},
        },
        "5": {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 2,
            "saddle_type": {"value": "DOWNWARD", "options": []},
            "event_action": {"value": "BUY", "options": []},
            "consecutive_up": {"value": "2"},
            "consecutive_down": {"value": "2"},
        },
        "6": {"blockId": 3, "blockType": "SIGNAL_BLOCK"},
        "7": {
            "blockType": "STRATEGY_BLOCK",
            "blockId": 1,
            "start_value": {"value": 10000.00},
            "commission": {"value": 4.95},
            "impact": {"value": 0.01},
            "stop_loss": {"value": 0.1},
            "take_profit": {"value": 0.1},
            "trade_amount_value": {"value": 10.00},
            "trade_amount_unit": {"value": "PERCENTAGE"},
        },
    },
    "edgeList": [
        {
            "source": "1",
            "sourceHandle": "output_id888",
            "target": "2",
            "targetHandle": "input_id891",
            "type": "edge",
            "id": "reactflow__edge-1output_id888-2input_id891",
        },
        {
            "source": "1",
            "sourceHandle": "output_id1136",
            "target": "3",
            "targetHandle": "input_id1143",
            "type": "edge",
            "id": "reactflow__edge-1output_id1136-3input_id1143",
        },
        {
            "source": "2",
            "sourceHandle": "output_id1356",
            "target": "4",
            "targetHandle": "input_id1363",
            "type": "edge",
            "id": "reactflow__edge-2output_id1356-4input_id1363",
        },
        {
            "source": "3",
            "sourceHandle": "output_id1576",
            "target": "4",
            "targetHandle": "input_id1579",
            "type": "edge",
            "id": "reactflow__edge-3output_id1576-4input_id1579",
        },
        {
            "source": "2",
            "sourceHandle": "output_id1576",
            "target": "5",
            "targetHandle": "input_id1579",
            "type": "edge",
            "id": "reactflow__edge-3output_id1576-4input_id1579",
        },
        {
            "source": "4",
            "sourceHandle": "output_id1576",
            "target": "6",
            "targetHandle": "input_id1579",
            "type": "edge",
            "id": "reactflow__edge-3output_id1576-4input_id1579",
        },
        {
            "source": "5",
            "sourceHandle": "output_id1576",
            "target": "6",
            "targetHandle": "input_id1579",
            "type": "edge",
            "id": "reactflow__edge-3output_id1576-4input_id1579",
        },
        {
            "source": "6",
            "sourceHandle": "output_id1796",
            "target": "7",
            "targetHandle": "input_id1799",
            "type": "edge",
            "id": "reactflow__edge-4output_id1796-5input_id1799",
        },
    ],
}

AND_BLOCK_SELECTS_CORRECT_PAYLOAD_AND_RETURNS_OK_RESPONSE = {
    "1": {
        "inputs": {
            "equity_name": "AAPL",
            "candlestick": "1month",
            "start_date": "2021-05-28 00:00:00",
            "end_date": "2021-07-30 00:00:00",
        },
        "outputs": {"ref": set()},
        "blockType": "DATA_BLOCK",
        "blockId": 1,
    },
    "3": {
        "inputs": {
            "indicator_name": "MA",
            "lookback_period": "1",
            "lookback_unit": "DATA_POINT",
        },
        "outputs": {"ref": {"1"}},
        "blockType": "COMPUTATIONAL_BLOCK",
        "blockId": 1,
    },
    "2": {
        "inputs": {
            "indicator_name": "MA",
            "lookback_period": "2",
            "lookback_unit": "DATA_POINT",
        },
        "outputs": {"ref": {"1"}},
        "blockType": "COMPUTATIONAL_BLOCK",
        "blockId": 1,
    },
    "4": {
        "inputs": {"event_action": "BUY"},
        "outputs": {"ref": {"3", "2"}},
        "blockType": "SIGNAL_BLOCK",
        "blockId": 1,
    },
    "5": {
        "inputs": {
            "saddle_type": "DOWNWARD",
            "event_action": "BUY",
            "consecutive_up": "2",
            "consecutive_down": "2",
        },
        "outputs": {"ref": {"2"}},
        "blockType": "SIGNAL_BLOCK",
        "blockId": 2,
    },
    "6": {
        "inputs": {},
        "outputs": {"ref": {"4", "5"}},
        "blockType": "SIGNAL_BLOCK",
        "blockId": 3,
    },
    "7": {
        "inputs": {
            "start_value": 10000.0,
            "commission": 4.95,
            "impact": 0.01,
            "stop_loss": 0.1,
            "take_profit": 0.1,
            "trade_amount_value": 10.0,
            "trade_amount_unit": "PERCENTAGE",
        },
        "outputs": {"ref": {"6", "1"}},
        "blockType": "STRATEGY_BLOCK",
        "blockId": 1,
    },
}

SINGLE_BLOCK_ALLOWING_SINGLE_INPUT_ALLOWS_BLOCKS_OF_MULTIPLE_TYPES_RETURNS_OK = {
    "nodeList": {
        "1": {
            "inputs": {
                "equity_name": "AAPL",
                "candlestick": "1month",
                "start_date": "2021-05-28 00:00:00",
                "end_date": "2021-07-30 00:00:00",
            },
            "outputs": {"ref": set()},
            "blockType": "DATA_BLOCK",
            "blockId": 1,
        },
        "2": {
            "inputs": {
                "data_field": "close",
                "operation_type": "*",
                "operation_value": "3",
            },
            "outputs": {"ref": set()},
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
        },
    },
    "edgeList": [
        {
            "source": "1",
            "sourceHandle": "output_id888",
            "target": "2",
            "targetHandle": "input_id891",
            "type": "edge",
            "id": "reactflow__edge-1output_id888-2input_id891",
        },
    ],
}

SINGLE_BLOCK_ALLOWING_SINGLE_INPUT_ALLOWS_BLOCKS_OF_MULTIPLE_TYPES_RETURNS_OK_RESPONSE = {
    "1": {
        "inputs": {},
        "outputs": {"ref": set()},
        "blockType": "DATA_BLOCK",
        "blockId": 1,
    },
    "2": {
        "inputs": {},
        "outputs": {"ref": {"1"}},
        "blockType": "COMPUTATIONAL_BLOCK",
        "blockId": 2,
    },
}

MULTIPLE_INCOMING_BLOCKS_OF_DIFFERENT_TYPES_RETURNS_OK = {
    "nodeList": {
        "1": {
            "inputs": {
                "equity_name": "AAPL",
                "candlestick": "1month",
                "start_date": "2021-05-28 00:00:00",
                "end_date": "2021-07-30 00:00:00",
            },
            "outputs": {"ref": set()},
            "blockType": "DATA_BLOCK",
            "blockId": 1,
        },
        "2": {
            "inputs": {
                "data_field": "close",
                "operation_type": "*",
                "operation_value": "3",
            },
            "outputs": {"ref": set()},
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 2,
        },
        "3": {
            "inputs": {
                "incoming_data_one": "1-close",
                "incoming_data_two": "2-data",
                "comparison_type": "<=",
                "event_action": "BUY",
            },
            "outputs": {"ref": set()},
            "blockType": "SIGNAL_BLOCK",
            "blockId": 7,
        },
    },
    "edgeList": [
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
            "sourceHandle": "output_id888",
            "target": "3",
            "targetHandle": "input_id891",
            "type": "edge",
            "id": "reactflow__edge-1output_id888-2input_id891",
        },
        {
            "source": "1",
            "sourceHandle": "output_id888",
            "target": "3",
            "targetHandle": "input_id891",
            "type": "edge",
            "id": "reactflow__edge-1output_id888-2input_id891",
        },
    ],
}

MULTIPLE_INCOMING_BLOCKS_OF_DIFFERENT_TYPES_RETURNS_OK_RESPONSE = {
    "1": {
        "inputs": {},
        "outputs": {"ref": set()},
        "blockType": "DATA_BLOCK",
        "blockId": 1,
    },
    "2": {
        "inputs": {},
        "outputs": {"ref": {"1"}},
        "blockType": "COMPUTATIONAL_BLOCK",
        "blockId": 2,
    },
    "3": {
        "inputs": {},
        "outputs": {"ref": {"1", "2"}},
        "blockType": "SIGNAL_BLOCK",
        "blockId": 7,
    },
}


BLOCK_DNE_IN_ASSEMBLED_DEPENDENCY_LIST_BUT_IN_REQUIRED_FIELDS_RETURNS_OK = {
    "nodeList": {
        "1": {
            "blockId": 1,
            "end_date": {"value": "2021-06-30", "rawValue": "2021-06-30T09:19:32.000Z"},
            "blockType": "DATA_BLOCK",
            "start_date": {
                "value": "2019-01-01",
                "rawValue": "2019-01-01T10:19:32.000Z",
            },
            "candlestick": {
                "value": "1day",
                "options": [
                    "1min",
                    "5min",
                    "15min",
                    "30min",
                    "60min",
                    "1day",
                    "1week",
                    "1month",
                ],
            },
            "equity_name": {
                "value": "AEHR",
                "options": ["AEHL", "AEHR", "AEHAU", "AEHDX"],
            },
        },
        "2": {
            "blockId": 1,
            "blockType": "COMPUTATIONAL_BLOCK",
            "incoming_data": {"value": "volume"},
            "indicator_name": {
                "value": "MA",
                "options": [
                    "MA",
                    "EMA",
                    "MACD",
                    "ADX",
                    "ADXR",
                    "APO",
                    "AROONOSC",
                    "BOP",
                    "CCI",
                    "CMO",
                    "DX",
                    "RSI",
                    "BB",
                    "DB",
                    "KAMA",
                    "KC",
                    "MI",
                    "STOCH_OSCI",
                    "TRIX",
                    "TSI",
                    "OR",
                ],
                "onChange": "indicatorField?indicatorName=",
            },
            "lookback_period": {"value": "30"},
        },
        "3": {
            "blockId": 2,
            "blockType": "COMPUTATIONAL_BLOCK",
            "data_field": {"value": "data", "inputFromConnectionValue": ""},
            "operation_type": {"value": "*", "options": ["+", "-", "*", "/", "^"]},
            "operation_value": {"value": "5"},
        },
        "4": {
            "blockId": 6,
            "blockType": "SIGNAL_BLOCK",
            "event_type": {
                "value": "CLOSE_ABOVE_OPEN",
                "options": [
                    "CLOSE_ABOVE_OPEN",
                    "CLOSE_BELOW_OPEN",
                    "CLOSE_EQ_HIGH",
                    "CLOSE_BELOW_HIGH",
                    "CLOSE_ABOVE_LOW",
                    "CLOSE_EQ_LOW",
                ],
            },
            "event_action": {"value": "BUY", "options": ["BUY", "SELL"]},
        },
        "6": {
            "blockId": 1,
            "blockType": "COMPUTATIONAL_BLOCK",
            "incoming_data": {"value": "volume"},
            "indicator_name": {
                "value": "MA",
                "options": [
                    "MA",
                    "EMA",
                    "MACD",
                    "ADX",
                    "ADXR",
                    "APO",
                    "AROONOSC",
                    "BOP",
                    "CCI",
                    "CMO",
                    "DX",
                    "RSI",
                    "BB",
                    "DB",
                    "KAMA",
                    "KC",
                    "MI",
                    "STOCH_OSCI",
                    "TRIX",
                    "TSI",
                    "OR",
                ],
                "onChange": "indicatorField?indicatorName=",
            },
            "lookback_period": {"value": "1"},
        },
        "7": {
            "blockId": 7,
            "blockType": "SIGNAL_BLOCK",
            "event_action": {"value": "BUY", "options": ["BUY", "SELL"]},
            "comparison_type": {"value": ">", "options": ["<", "<=", ">", ">="]},
            "incoming_data_one": {"value": "data", "inputFromConnectionValue": "6"},
            "incoming_data_two": {"value": "data", "inputFromConnectionValue": "3"},
        },
        "8": {"blockId": 3, "blockType": "SIGNAL_BLOCK"},
        "9": {
            "blockId": 1,
            "blockType": "STRATEGY_BLOCK",
            "commission": {"value": "0"},
            "start_value": {"value": "100000"},
            "trade_amount_value": {"value": "5000"},
        },
    },
    "edgeList": [
        {
            "id": "reactflow__edge-1output_1-2input_2",
            "type": "flowEdge",
            "source": "1",
            "target": "2",
            "sourceHandle": "output_1",
            "targetHandle": "input_2",
        },
        {
            "id": "reactflow__edge-2output_2-3input_3",
            "type": "flowEdge",
            "source": "2",
            "target": "3",
            "sourceHandle": "output_2",
            "targetHandle": "input_3",
        },
        {
            "id": "reactflow__edge-1output_1-4input_4",
            "type": "flowEdge",
            "source": "1",
            "target": "4",
            "sourceHandle": "output_1",
            "targetHandle": "input_4",
        },
        {
            "id": "reactflow__edge-1output_1-6input_6",
            "type": "flowEdge",
            "source": "1",
            "target": "6",
            "sourceHandle": "output_1",
            "targetHandle": "input_6",
        },
        {
            "id": "reactflow__edge-6output_6-7input_7",
            "type": "flowEdge",
            "source": "6",
            "target": "7",
            "sourceHandle": "output_6",
            "targetHandle": "input_7",
        },
        {
            "id": "reactflow__edge-3output_3-7input_7",
            "type": "flowEdge",
            "source": "3",
            "target": "7",
            "sourceHandle": "output_3",
            "targetHandle": "input_7",
        },
        {
            "id": "reactflow__edge-4output_4-8input_8",
            "type": "flowEdge",
            "source": "4",
            "target": "8",
            "sourceHandle": "output_4",
            "targetHandle": "input_8",
        },
        {
            "id": "reactflow__edge-7output_7-8input_8",
            "type": "flowEdge",
            "source": "7",
            "target": "8",
            "sourceHandle": "output_7",
            "targetHandle": "input_8",
        },
        {
            "id": "reactflow__edge-8output_8-9input_9",
            "type": "flowEdge",
            "source": "8",
            "target": "9",
            "sourceHandle": "output_8",
            "targetHandle": "input_9",
        },
    ],
}

BLOCK_DNE_IN_ASSEMBLED_DEPENDENCY_LIST_BUT_IN_REQUIRED_FIELDS_RESPONSE = {
    "1": {
        "inputs": {
            "end_date": "2021-06-30",
            "start_date": "2019-01-01",
            "candlestick": "1day",
            "equity_name": "AEHR",
        },
        "outputs": {"ref": set()},
        "blockType": "DATA_BLOCK",
        "blockId": 1,
    },
    "4": {
        "inputs": {"event_type": "CLOSE_ABOVE_OPEN", "event_action": "BUY"},
        "outputs": {"ref": {"1"}},
        "blockType": "SIGNAL_BLOCK",
        "blockId": 6,
    },
    "6": {
        "inputs": {
            "incoming_data": "volume",
            "indicator_name": "MA",
            "lookback_period": "1",
        },
        "outputs": {"ref": {"1"}},
        "blockType": "COMPUTATIONAL_BLOCK",
        "blockId": 1,
    },
    "2": {
        "inputs": {
            "incoming_data": "volume",
            "indicator_name": "MA",
            "lookback_period": "30",
        },
        "outputs": {"ref": {"1"}},
        "blockType": "COMPUTATIONAL_BLOCK",
        "blockId": 1,
    },
    "3": {
        "inputs": {"data_field": "data", "operation_type": "*", "operation_value": "5"},
        "outputs": {"ref": {"2"}},
        "blockType": "COMPUTATIONAL_BLOCK",
        "blockId": 2,
    },
    "7": {
        "inputs": {
            "event_action": "BUY",
            "comparison_type": ">",
            "incoming_data_one": "6-data",
            "incoming_data_two": "3-data",
        },
        "outputs": {"ref": {"6", "3"}},
        "blockType": "SIGNAL_BLOCK",
        "blockId": 7,
    },
    "8": {
        "inputs": {},
        "outputs": {"ref": {"4", "7"}},
        "blockType": "SIGNAL_BLOCK",
        "blockId": 3,
    },
    "9": {
        "inputs": {
            "commission": "0",
            "start_value": "100000",
            "trade_amount_value": "5000",
        },
        "outputs": {"ref": {"8", "1"}},
        "blockType": "STRATEGY_BLOCK",
        "blockId": 1,
    },
}

FLOW_WITHOUT_SCREENER_BLOCK_RETURNS_008 = {
    "nodeList": {
        "1": {
            "blockType": "BULK_DATA_BLOCK",
            "blockId": 1,
            "equity_name": {"value": "AAPL", "options": []},
            "data_type": {
                "value": "intraday",
                "options": ["intraday", "daily_adjusted"],
            },
            "interval": {"value": "1min", "options": ["1min"]},
            "outputsize": {"value": "compact", "options": ["compact", "full"]},
            "start_date": {"value": "2021-06-21 19:58:00"},
            "end_date": {"value": "2021-06-21 19:58:00"},
        },
    },
    "edgeList": [],
}

FLOW_WITH_SCREENER_BLOCK_RETURNS_OK = {
    "nodeList": {
        "1": {
            "blockType": "BULK_DATA_BLOCK",
            "blockId": 1,
            "equity_name": {"value": "AAPL", "options": []},
            "data_type": {
                "value": "intraday",
                "options": ["intraday", "daily_adjusted"],
            },
            "interval": {"value": "1min", "options": ["1min"]},
            "outputsize": {"value": "compact", "options": ["compact", "full"]},
            "start_date": {"value": "2021-06-21 19:58:00"},
            "end_date": {"value": "2021-06-21 19:58:00"},
        },
        "2": {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 1,
            "indicator_name": {"value": "MA", "options": []},
            "lookback_period": {"value": "2"},
            "lookback_unit": {"value": "DATA_POINT"},
        },
        "3": {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 1,
            "indicator_name": {"value": "MA"},
            "lookback_period": {"value": "1"},
            "lookback_unit": {"value": "DATA_POINT"},
        },
        "4": {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 1,
            "event_action": {"value": "BUY"},
        },
    },
    "edgeList": [
        {
            "source": "1",
            "sourceHandle": "output_id888",
            "target": "2",
            "targetHandle": "input_id891",
            "type": "edge",
            "id": "reactflow__edge-1output_id888-2input_id891",
        },
        {
            "source": "1",
            "sourceHandle": "output_id1136",
            "target": "3",
            "targetHandle": "input_id1143",
            "type": "edge",
            "id": "reactflow__edge-1output_id1136-3input_id1143",
        },
        {
            "source": "2",
            "sourceHandle": "output_id1356",
            "target": "4",
            "targetHandle": "input_id1363",
            "type": "edge",
            "id": "reactflow__edge-2output_id1356-4input_id1363",
        },
        {
            "source": "3",
            "sourceHandle": "output_id1576",
            "target": "4",
            "targetHandle": "input_id1579",
            "type": "edge",
            "id": "reactflow__edge-3output_id1576-4input_id1579",
        },
    ],
}

MULTIPLE_STRATEGY_BLOCKS_RAISE_EXCEPTION = {
    "nodeList": {
        "1": {
            "blockType": "DATA_BLOCK",
            "blockId": 1,
            "equity_name": {"value": "AAPL", "options": []},
            "candlestick": {"value": "1month", "options": ["1min", "1month"]},
            "start_date": {"value": "2021-05-28 00:00:00"},
            "end_date": {"value": "2021-07-30 00:00:00"},
        },
        "2": {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 1,
            "indicator_name": {"value": "MA", "options": []},
            "lookback_period": {"value": "2"},
            "lookback_unit": {"value": "DATA_POINT"},
        },
        "3": {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 1,
            "indicator_name": {"value": "MA"},
            "lookback_period": {"value": "1"},
            "lookback_unit": {"value": "DATA_POINT"},
        },
        "4": {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 1,
            "event_action": {"value": "BUY"},
        },
        "5": {
            "blockType": "STRATEGY_BLOCK",
            "blockId": 1,
            "start_value": {"value": 10000.00},
            "commission": {"value": 4.95},
            "impact": {"value": 0.01},
            "stop_loss": {"value": 0.1},
            "take_profit": {"value": 0.1},
            "trade_amount_value": {"value": 10.00},
            "trade_amount_unit": {"value": "PERCENTAGE"},
        },
        "6": {
            "blockType": "STRATEGY_BLOCK",
            "blockId": 1,
            "start_value": {"value": 10000.00},
            "commission": {"value": 4.95},
            "impact": {"value": 0.01},
            "stop_loss": {"value": 0.1},
            "take_profit": {"value": 0.1},
            "trade_amount_value": {"value": 10.00},
            "trade_amount_unit": {"value": "PERCENTAGE"},
        },
    },
    "edgeList": [
        {
            "source": "1",
            "sourceHandle": "output_id888",
            "target": "2",
            "targetHandle": "input_id891",
            "type": "edge",
            "id": "reactflow__edge-1output_id888-2input_id891",
        },
        {
            "source": "1",
            "sourceHandle": "output_id1136",
            "target": "3",
            "targetHandle": "input_id1143",
            "type": "edge",
            "id": "reactflow__edge-1output_id1136-3input_id1143",
        },
        {
            "source": "2",
            "sourceHandle": "output_id1356",
            "target": "4",
            "targetHandle": "input_id1363",
            "type": "edge",
            "id": "reactflow__edge-2output_id1356-4input_id1363",
        },
        {
            "source": "3",
            "sourceHandle": "output_id1576",
            "target": "4",
            "targetHandle": "input_id1579",
            "type": "edge",
            "id": "reactflow__edge-3output_id1576-4input_id1579",
        },
        {
            "source": "4",
            "sourceHandle": "output_id1796",
            "target": "5",
            "targetHandle": "input_id1799",
            "type": "edge",
            "id": "reactflow__edge-4output_id1796-5input_id1799",
        },
        {
            "source": "4",
            "sourceHandle": "output_id1796",
            "target": "6",
            "targetHandle": "input_id1800",
            "type": "edge",
            "id": "reactflow__edge-4output_id1796-5input_id1800",
        },
    ],
}
