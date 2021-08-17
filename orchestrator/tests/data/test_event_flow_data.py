SINGLE_NODE_DATA_FLOW_RETURNS_OK = {
    "nodeList": {
        "1": {
            "blockType": "DATA_BLOCK",
            "blockId": 1,
            "equity_name": {"value": "AAPL", "options": []},
            "data_type": {"value": "intraday", "options": ["intraday", "daily_adjusted"]},
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
            "data_type": {"value": "intraday", "options": ["intraday", "daily_adjusted"]},
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
        "3": {
            "blockType": "COMPUTATIONAL_BLOCK",
            "blockId": 1,
            "indicator_name": {"value": "MA"},
            "lookback_period": {"value": "5"},
            "lookback_unit": {"value": "DATA_POINT"},
        },
        "4": {
            "blockType": "SIGNAL_BLOCK",
            "blockId": 1,
            "event_type": {"value": "INTERSECT"},
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
