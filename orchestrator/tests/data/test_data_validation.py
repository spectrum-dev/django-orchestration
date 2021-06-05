SINGLE_FULL_FLOW_INVALID = {
  "nodeList": {
    "1": {
      "blockType": "DATA_BLOCK",
      "blockId": 1,
      "equity_name": {
        "options": [
          "AAPL"
        ],
        "value": ""
      },
      "data_type": {
        "options": [
          "intraday",
          "daily_adjusted"
        ],
        "value": ""
      },
      "interval": {
        "options": [
          "1min"
        ],
        "value": ""
      },
      "outputsize": {
        "options": [
          "compact",
          "full"
        ],
        "value": ""
      },
      "start_date": {
        "value": ""
      },
      "end_date": {
        "value": ""
      }
    },
    "2": {
      "blockType": "COMPUTATIONAL_BLOCK",
      "blockId": 1,
      "indicator_name": {
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
          "RSI"
        ],
        "value": ""
      }
    },
    "3": {
      "blockType": "SIGNAL_BLOCK",
      "blockId": 1,
      "event_type": {
        "options": [
          "INTERSECT"
        ],
        "value": ""
      },
      "event_action": {
        "options": [
          "BUY",
          "SELL"
        ],
        "value": ""
      }
    },
    "4": {
      "blockType": "SIGNAL_BLOCK",
      "blockId": 1,
      "event_type": {
        "options": [
          "INTERSECT"
        ],
        "value": ""
      },
      "event_action": {
        "options": [
          "BUY",
          "SELL"
        ],
        "value": ""
      }
    }
  },
  "edgeList": [
    {
      "source": "1",
      "sourceHandle": "output_id502",
      "target": "4",
      "targetHandle": "input_id589",
      "type": "edge",
      "id": "reactflow__edge-1output_id502-4input_id589"
    },
    {
      "source": "4",
      "sourceHandle": "output_id986",
      "target": "2",
      "targetHandle": "input_id1089",
      "type": "edge",
      "id": "reactflow__edge-4output_id986-2input_id1089"
    },
    {
      "source": "4",
      "sourceHandle": "output_id1230",
      "target": "3",
      "targetHandle": "input_id1417",
      "type": "edge",
      "id": "reactflow__edge-4output_id1230-3input_id1417"
    }
  ]
}


SINGLE_FULL_FLOW_VALID = {
  "nodeList": {
    "1": {
      "blockType": "DATA_BLOCK",
      "blockId": 1,
      "equity_name": {
        "options": [
          "AAPL"
        ],
        "value": "AAPL"
      },
      "data_type": {
        "options": [
          "intraday",
          "daily_adjusted"
        ],
        "value": "intraday"
      },
      "interval": {
        "options": [
          "1min"
        ],
        "value": "1min"
      },
      "outputsize": {
        "options": [
          "compact",
          "full"
        ],
        "value": "compact"
      },
      "start_date": {
        "value": "2020-01-01"
      },
      "end_date": {
        "value": "2021-01-01"
      }
    },
    "2": {
      "blockType": "COMPUTATIONAL_BLOCK",
      "blockId": 1,
      "indicator_name": {
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
          "RSI"
        ],
        "value": "MA"
      }
    },
    "3": {
      "blockType": "COMPUTATIONAL_BLOCK",
      "blockId": 1,
      "indicator_name": {
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
          "RSI"
        ],
        "value": "MA"
      }
    },
    "4": {
      "blockType": "SIGNAL_BLOCK",
      "blockId": 1,
      "event_type": {
        "options": [
          "INTERSECT"
        ],
        "value": "INTERSECT"
      },
      "event_action": {
        "options": [
          "BUY",
          "SELL"
        ],
        "value": "BUY"
      }
    },
    "5": {
      "blockType": "STRATEGY_BLOCK",
      "blockId": 1,
      "commission": {
        "value": "4.95"
      },
      "impact": {
        "value": "0.0"
      },
      "start_value": {
        "value": "10000.00"
      },
      "stop_loss": {
        "value": "0.00"
      },
      "take_profit": {
        "value": "0.00"
      },
      "trade_amount_value": {
        "value": "1000.00"
      }
    }
  },
  "edgeList": [
    {
      "source": "1",
      "sourceHandle": "output_id888",
      "target": "2",
      "targetHandle": "input_id891",
      "type": "edge",
      "id": "reactflow__edge-1output_id888-2input_id891"
    },
    {
      "source": "1",
      "sourceHandle": "output_id1136",
      "target": "3",
      "targetHandle": "input_id1143",
      "type": "edge",
      "id": "reactflow__edge-1output_id1136-3input_id1143"
    },
    {
      "source": "2",
      "sourceHandle": "output_id1356",
      "target": "4",
      "targetHandle": "input_id1363",
      "type": "edge",
      "id": "reactflow__edge-2output_id1356-4input_id1363"
    },
    {
      "source": "3",
      "sourceHandle": "output_id1576",
      "target": "4",
      "targetHandle": "input_id1579",
      "type": "edge",
      "id": "reactflow__edge-3output_id1576-4input_id1579"
    },
    {
      "source": "4",
      "sourceHandle": "output_id1796",
      "target": "5",
      "targetHandle": "input_id1799",
      "type": "edge",
      "id": "reactflow__edge-4output_id1796-5input_id1799"
    }
  ]
}