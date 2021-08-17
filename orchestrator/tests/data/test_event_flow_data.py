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
