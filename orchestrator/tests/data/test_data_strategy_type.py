BACKTEST_FLOW_OK = {
    "nodeList": {
        "1": {
            "blockType": "DATA_BLOCK",
            "blockId": 1,
            "equity_name": {"options": ["AAPL"], "value": ""},
            "data_type": {"options": ["intraday", "daily_adjusted"], "value": ""},
            "interval": {"options": ["1min"], "value": ""},
            "outputsize": {"options": ["compact", "full"], "value": ""},
            "start_date": {"value": ""},
            "end_date": {"value": ""},
        },
    },
    "edgeList": [],
}

SCREENER_FLOW_OK = {
    "nodeList": {
        "1": {
            "blockType": "BULK_DATA_BLOCK",
            "blockId": 1,
            "equity_name": {"options": ["AAPL"], "value": ""},
            "data_type": {"options": ["intraday", "daily_adjusted"], "value": ""},
            "interval": {"options": ["1min"], "value": ""},
            "outputsize": {"options": ["compact", "full"], "value": ""},
            "start_date": {"value": ""},
            "end_date": {"value": ""},
        },
    },
    "edgeList": [],
}
