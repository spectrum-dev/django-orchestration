FULL_TECHNICAL_ANALYSIS_FLOW_SINGLE_FLOW = {
    "strategyId": "69078f28-4747-4b28-9294-9da43fe37846",
    "nodeList": [
        {
            "id": "1",
            "type": "blockGenerator",
            "position": {
                "x": 580,
                "y": 140
            },
            "data": {
                "metadata": {
                    "header": "Raw Data",
                    "inputHandles": [],
                    "outputHandles": [
                        {
                            "fieldName": "",
                            "fieldVariableName": "",
                            "validConnections": []
                        }
                    ],
                    "dataInputs": [
                        {
                            "fieldName": "Equity Type",
                            "fieldVariableName": "equityType",
                            "fieldType": "dropdown",
                            "fieldData": {
                                "method": "GET",
                                "base": "/dataBlock/1/equityType"
                            }
                        },
                        {
                            "fieldName": "Region",
                            "fieldVariableName": "region",
                            "fieldType": "dropdown",
                            "fieldData": {
                                "method": "GET",
                                "base": "/dataBlock/1/equityRegion"
                            }
                        },
                        {
                            "fieldName": "Equity Name",
                            "fieldVariableName": "equityName",
                            "fieldType": "search",
                            "fieldData": {
                                "method": "GET",
                                "base": "/dataBlock/1/searchTicker"
                            }
                        },
                        {
                            "fieldName": "Start Date",
                            "fieldVariableName": "startDate",
                            "fieldType": "input"
                        },
                        {
                            "fieldName": "End Date",
                            "fieldVariableName": "endDate",
                            "fieldType": "input"
                        }
                    ],
                    "blockType": "DATA_BLOCK",
                    "blockId": 1
                },
                "input": {
                    "equity_name": "AAPL",
                    "data_type": "daily_adjusted",
                    "interval": "1min",
                    "outputsize": "full",
                    "start_date": "",
                    "end_date": "",
                },
                "output": {},
                "helpers": {}
            }
        },
        {
            "id": "2",
            "type": "blockGenerator",
            "position": {
                "x": 660,
                "y": 40
            },
            "data": {
                "metadata": {
                    "header": "Technical Analysis",
                    "inputHandles": [
                        {
                            "fieldName": "",
                            "fieldVariableName": "",
                            "validConnections": []
                        }
                    ],
                    "outputHandles": [
                        {
                            "fieldName": "",
                            "fieldVariableName": "",
                            "validConnections": []
                        }
                    ],
                    "dataInputs": [
                        {
                            "fieldName": "Indicator Name",
                            "fieldVariableName": "indicatorName",
                            "fieldType": "dropdown",
                            "fieldData": {
                                "method": "GET",
                                "base": "/computationBlock/1/indicatorNames",
                                "onChange": "/computationBlock/1/indicatorFields?indicatorName="
                            }
                        }
                    ],
                    "blockType": "COMPUTATIONAL_BLOCK",
                    "blockId": 1
                },
                "input": {
                    "short_name": "MA",
                    "indicator_name": "MA",
                    "lookback_period": "10",
                    "lookback_unit": "DATA_POINT"
                },
                "output": {},
                "helpers": {}
            }
        },
        {
            "id": "3",
            "type": "blockGenerator",
            "position": {
                "x": 900,
                "y": 380
            },
            "data": {
                "metadata": {
                    "header": "Technical Analysis",
                    "inputHandles": [
                        {
                            "fieldName": "",
                            "fieldVariableName": "",
                            "validConnections": []
                        }
                    ],
                    "outputHandles": [
                        {
                            "fieldName": "",
                            "fieldVariableName": "",
                            "validConnections": []
                        }
                    ],
                    "dataInputs": [
                        {
                            "fieldName": "Indicator Name",
                            "fieldVariableName": "indicatorName",
                            "fieldType": "dropdown",
                            "fieldData": {
                                "method": "GET",
                                "base": "/computationBlock/1/indicatorNames",
                                "onChange": "/computationBlock/1/indicatorFields?indicatorName="
                            }
                        }
                    ],
                    "blockType": "COMPUTATIONAL_BLOCK",
                    "blockId": 1
                },
                "input": {
                    "short_name": "MA",
                    "indicator_name": "MA",
                    "lookback_period": "12",
                    "lookback_unit": "DATA_POINT"
                },
                "output": {},
                "helpers": {}
            }
        },
        {
            "id": "4",
            "type": "blockGenerator",
            "position": {
                "x": 1260,
                "y": 220
            },
            "data": {
                "metadata": {
                    "header": "Event Block",
                    "inputHandles": [
                        {
                            "fieldName": "",
                            "fieldVariableName": "",
                            "validConnections": []
                        }
                    ],
                    "outputHandles": [
                        {
                            "fieldName": "",
                            "fieldVariableName": "",
                            "validConnections": []
                        }
                    ],
                    "dataInputs": [
                        {
                            "fieldName": "Event Type",
                            "fieldVariableName": "eventType",
                            "fieldType": "dropdown",
                            "fieldData": {
                                "method": "GET",
                                "base": "/signalBlock/1/eventTypes"
                            }
                        },
                        {
                            "fieldName": "Event Action",
                            "fieldVariableName": "eventAction",
                            "fieldType": "dropdown",
                            "fieldData": {
                                "method": "GET",
                                "base": "/signalBlock/1/eventActions"
                            }
                        }
                    ],
                    "blockType": "SIGNAL_BLOCK",
                    "blockId": 1
                },
                "input": {
                    "event_type": "INTERSECT",
                    "event_action": "BUY"
                },
                "output": {},
                "helpers": {}
            }
        },
        {
            "id": "5",
            "type": "blockGenerator",
            "position": {
                "x": 1640,
                "y": 120
            },
            "data": {
                "metadata": {
                    "header": "Backtest",
                    "inputHandles": [
                        {
                            "fieldName": "",
                            "fieldVariableName": "",
                            "validConnections": []
                        }
                    ],
                    "outputHandles": [],
                    "dataInputs": [
                        {
                            "fieldName": "Commission",
                            "fieldVariableName": "commission",
                            "fieldType": "input"
                        },
                        {
                            "fieldName": "Impact",
                            "fieldVariableName": "impact",
                            "fieldType": "input"
                        },
                        {
                            "fieldName": "Start Value",
                            "fieldVariableName": "startValue",
                            "fieldType": "input"
                        },
                        {
                            "fieldName": "Stop Loss",
                            "fieldVariableName": "stopLoss",
                            "fieldType": "input"
                        },
                        {
                            "fieldName": "Take Profit",
                            "fieldVariableName": "takeProfit",
                            "fieldType": "input"
                        },
                        {
                            "fieldName": "Trade Amount",
                            "fieldVariableName": "tradeAmount",
                            "fieldType": "input"
                        }
                    ],
                    "blockType": "STRATEGY_BLOCK",
                    "blockId": 1
                },
                "input": {
                    "start_value": 10000.00,
                    "commission": 4.95,
                    "impact": 0.01,
                    "stop_loss": 0.1,
                    "take_profit": 0.1,
                    "trade_amount_value": 10.00,
                    "trade_amount_unit": "PERCENTAGE"
                },
                "output": {},
                "helpers": {}
            }
        }
    ],
    "edgeList": [
        {
            "source": "1",
            "sourceHandle": "undefined_input_0",
            "target": "2",
            "targetHandle": "undefined_input_0",
            "id": "reactflow__edge-1undefined_input_0-2undefined_input_0"
        },
        {
            "source": "1",
            "sourceHandle": "undefined_input_0",
            "target": "3",
            "targetHandle": "undefined_input_0",
            "id": "reactflow__edge-1undefined_input_0-3undefined_input_0"
        },
        {
            "source": "2",
            "sourceHandle": "undefined_input_0",
            "target": "4",
            "targetHandle": "undefined_input_0",
            "id": "reactflow__edge-2undefined_input_0-4undefined_input_0"
        },
        {
            "source": "3",
            "sourceHandle": "undefined_input_0",
            "target": "4",
            "targetHandle": "undefined_input_0",
            "id": "reactflow__edge-3undefined_input_0-4undefined_input_0"
        },
        {
            "source": "4",
            "sourceHandle": "undefined_input_0",
            "target": "5",
            "targetHandle": "undefined_input_0",
            "id": "reactflow__edge-4undefined_input_0-5undefined_input_0"
        }
    ]
}

SINGLE_RAW_DATA_BLOCK_FLOW = {
  "nodeList": [
    {
      "id": "1",
      "type": "blockGenerator",
      "position": {
        "x": 540,
        "y": 140
      },
      "data": {
        "metadata": {
          "header": "Raw Data",
          "inputHandles": [],
          "outputHandles": [
            {
              "number": 1,
              "blockType": "DATA_BLOCK"
            }
          ],
          "dataInputs": [
            {
              "fieldData": {
                "base": "/equityName",
                "method": "GET"
              },
              "fieldName": "Equity Name",
              "fieldType": "dropdown",
              "fieldVariableName": "equity_name"
            },
            {
              "fieldData": {
                "base": "/dataType",
                "method": "GET"
              },
              "fieldName": "Data Type",
              "fieldType": "dropdown",
              "fieldVariableName": "data_type"
            },
            {
              "fieldData": {
                "base": "/interval",
                "method": "GET"
              },
              "fieldName": "Interval",
              "fieldType": "dropdown",
              "fieldVariableName": "interval"
            },
            {
              "fieldData": {
                "base": "/outputSize",
                "method": "GET"
              },
              "fieldName": "Output Size",
              "fieldType": "dropdown",
              "fieldVariableName": "outputsize"
            },
            {
              "fieldName": "Start Date",
              "fieldType": "input",
              "fieldVariableName": "start_date"
            },
            {
              "fieldName": "End Date",
              "fieldType": "input",
              "fieldVariableName": "end_date"
            }
          ],
          "blockType": "DATA_BLOCK",
          "blockId": 1
        },
        "input": {
          "equity_name": "AAPL",
          "data_type": "full",
          "interval": "1min",
          "outputsize": "full",
          "start_date": "2020-01-01",
          "end_date": "2021-01-0"
        },
        "output": {},
        "helpers": {}
      }
    }
  ],
  "edgeList": []
}