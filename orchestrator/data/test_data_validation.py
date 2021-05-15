SINGLE_FULL_FLOW = {
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
    },
    "5": {
      "blockType": "STRATEGY_BLOCK",
      "blockId": 1,
      "commission": {
        "value": ""
      },
      "impact": {
        "value": ""
      },
      "start_value": {
        "value": ""
      },
      "stop_loss": {
        "value": ""
      },
      "take_profit": {
        "value": ""
      },
      "trade_amount_value": {
        "value": ""
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