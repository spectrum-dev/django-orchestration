# Generated by Django 3.2 on 2021-04-15 13:23

from django.db import migrations


def seed_blocks_into_registry(apps, schema_editor):
    BlockRegistry = apps.get_model("orchestrator", "BlockRegistry")

    BlockRegistry(
        block_type="DATA_BLOCK",
        block_id=1,
        block_name="US Stock Data",
        inputs=[
            {
                "fieldData": {
                    "base": "/equityName?name=",
                    "method": "GET",
                },
                "fieldName": "Equity Name",
                "fieldType": "search",
                "fieldVariableName": "equity_name",
            },
            {
                "fieldData": {
                    "data": [
                        "1min",
                        "5min",
                        "15min",
                        "30min",
                        "60min",
                        "1day",
                        "1week",
                        "1month",
                    ]
                },
                "fieldName": "Candlesticks",
                "fieldType": "dropdown",
                "fieldVariableName": "candlestick",
            },
            {
                "fieldName": "Date Range",
                "fieldType": "date_range",
                "fieldVariableNames": ["start_date", "end_date"],
            },
        ],
        validations={
            "input": {"required": [], "allowed_blocks": []},
            "output": [{"blockType": "DATA_BLOCK", "number": 1}],
        },
        output_interface={"interface": ["open", "high", "low", "close", "volume"]},
    ).save()

    BlockRegistry(
        block_type="DATA_BLOCK",
        block_id=2,
        block_name="Crypto Data",
        inputs=[
            {
                "fieldData": {
                    "base": "/cryptoName?name=",
                    "method": "GET",
                },
                "fieldName": "Crypto Name",
                "fieldType": "search",
                "fieldVariableName": "crypto_name",
            },
            {
                "fieldData": {
                    "data": [
                        "1min",
                        "5min",
                        "15min",
                        "30min",
                        "60min",
                        "1day",
                        "1week",
                        "1month",
                    ]
                },
                "fieldName": "Candlesticks",
                "fieldType": "dropdown",
                "fieldVariableName": "candlestick",
            },
            {
                "fieldName": "Date Range",
                "fieldType": "date_range",
                "fieldVariableNames": ["start_date", "end_date"],
            },
        ],
        validations={
            "input": {"required": [], "allowed_blocks": []},
            "output": [{"blockType": "DATA_BLOCK", "number": 1}],
        },
        output_interface={"interface": ["open", "high", "low", "close", "volume"]},
    ).save()

    BlockRegistry(
        block_type="BULK_DATA_BLOCK",
        block_id=1,
        block_name="Screener Data",
        inputs=[
            {
                "fieldData": {
                    "data": [
                        "US",
                        "KLSE",
                    ]
                },
                "fieldName": "Exchanges",
                "fieldType": "dropdown",
                "fieldVariableName": "exchange_name",
            },
            {
                "fieldData": {"data": ["1day"]},
                "fieldName": "Candlesticks",
                "fieldType": "dropdown",
                "fieldVariableName": "candlestick",
            },
            {
                "fieldName": "Date Range",
                "fieldType": "date_range",
                "fieldVariableNames": ["start_date", "end_date"],
            },
        ],
        validations={
            "input": {"required": [], "allowed_blocks": []},
            "output": [{"blockType": "BULK_DATA_BLOCK", "number": 1}],
        },
        output_interface={"interface": ["open", "high", "low", "close", "volume"]},
    ).save()

    BlockRegistry(
        block_type="COMPUTATIONAL_BLOCK",
        block_id=1,
        block_name="Technical Indicators",
        inputs=[
            {
                "fieldData": {
                    "base": "/indicator",
                    "method": "GET",
                    "onChange": "indicatorField?indicatorName=",
                },
                "fieldName": "Indicator Name",
                "fieldType": "dropdown",
                "fieldVariableName": "indicator_name",
            },
        ],
        validations={
            "input": {
                "required": [
                    {"blockType": ["DATA_BLOCK", "BULK_DATA_BLOCK"], "number": 1}
                ],
                "allowed_blocks": [
                    {"blockId": "1", "blockType": "DATA_BLOCK"},
                    {"blockId": "2", "blockType": "DATA_BLOCK"},
                    {"blockId": "1", "blockType": "BULK_DATA_BLOCK"},
                ],
            },
            "output": [{"blockType": "COMPUTATIONAL_BLOCK", "number": 1}],
        },
        output_interface={"interface": ["data"]},
    ).save()

    BlockRegistry(
        block_type="COMPUTATIONAL_BLOCK",
        block_id=2,
        block_name="Math Operation",
        inputs=[
            {
                "fieldName": "Incoming Data",
                "fieldVariableName": "data_field",
                "fieldType": "inputs_from_connection",
                "fieldDefaultValue": "close",
            },
            {
                "fieldData": {
                    "data": [
                        "+",
                        "-",
                        "*",
                        "/",
                        "^",
                    ]
                },
                "fieldName": "Operation Type",
                "fieldType": "dropdown",
                "fieldVariableName": "operation_type",
            },
            {
                "fieldName": "Operation Value",
                "fieldVariableName": "operation_value",
                "fieldType": "input",
            },
        ],
        validations={
            "input": {
                "required": [
                    {
                        "blockType": [
                            "DATA_BLOCK",
                            "BULK_DATA_BLOCK",
                            "COMPUTATIONAL_BLOCK",
                        ],
                        "number": 1,
                    }
                ],
                "allowed_blocks": [
                    {"blockId": "1", "blockType": "DATA_BLOCK"},
                    {"blockId": "2", "blockType": "DATA_BLOCK"},
                    {"blockId": "1", "blockType": "BULK_DATA_BLOCK"},
                    {"blockId": "1", "blockType": "COMPUTATIONAL_BLOCK"},
                ],
            },
            "output": [{"blockType": "COMPUTATIONAL_BLOCK", "number": 1}],
        },
        output_interface={"interface": ["data"]},
    ).save()

    BlockRegistry(
        block_type="SIGNAL_BLOCK",
        block_id=1,
        block_name="Intersect",
        inputs=[
            {
                "fieldData": {"data": ["BUY", "SELL"]},
                "fieldName": "Event Action",
                "fieldType": "dropdown",
                "fieldVariableName": "event_action",
            },
        ],
        validations={
            "input": {
                "required": [{"blockType": ["COMPUTATIONAL_BLOCK"], "number": 2}],
                "allowed_blocks": [
                    {"blockId": "1", "blockType": "COMPUTATIONAL_BLOCK"},
                    {"blockId": "2", "blockType": "COMPUTATIONAL_BLOCK"},
                ],
            },
            "output": [{"blockType": "SIGNAL_BLOCK", "number": 1}],
        },
        output_interface={"interface": ["timestamp", "order"]},
    ).save()

    BlockRegistry(
        block_type="SIGNAL_BLOCK",
        block_id=2,
        block_name="Saddle",
        inputs=[
            {
                "fieldName": "Incoming Data",
                "fieldVariableName": "incoming_data",
                "fieldType": "inputs_from_connection",
                "fieldDefaultValue": "close",
            },
            {
                "fieldData": {"data": ["DOWNWARD", "UPWARD"]},
                "fieldName": "Saddle Type",
                "fieldType": "dropdown",
                "fieldVariableName": "saddle_type",
            },
            {
                "fieldData": {"data": ["BUY", "SELL"]},
                "fieldName": "Event Action",
                "fieldType": "dropdown",
                "fieldVariableName": "event_action",
            },
            {
                "fieldName": "Consecutive Up",
                "fieldVariableName": "consecutive_up",
                "fieldType": "input",
            },
            {
                "fieldName": "Consecutive Down",
                "fieldVariableName": "consecutive_down",
                "fieldType": "input",
            },
        ],
        validations={
            "input": {
                "required": [
                    {
                        "blockType": [
                            "DATA_BLOCK",
                            "BULK_DATA_BLOCK",
                            "COMPUTATIONAL_BLOCK",
                        ],
                        "number": 1,
                    }
                ],
                "allowed_blocks": [
                    {"blockId": "1", "blockType": "DATA_BLOCK"},
                    {"blockId": "2", "blockType": "DATA_BLOCK"},
                    {"blockId": "1", "blockType": "BULK_DATA_BLOCK"},
                    {"blockId": "1", "blockType": "COMPUTATIONAL_BLOCK"},
                    {"blockId": "2", "blockType": "COMPUTATIONAL_BLOCK"},
                ],
            },
            "output": [{"blockType": "SIGNAL_BLOCK", "number": 2}],
        },
        output_interface={"interface": ["timestamp", "order"]},
    ).save()

    BlockRegistry(
        block_type="SIGNAL_BLOCK",
        block_id=3,
        block_name="And",
        inputs=[],
        validations={
            "input": {
                "required": [{"blockType": ["SIGNAL_BLOCK"], "number": 2}],
                "allowed_blocks": [
                    {"blockId": "1", "blockType": "SIGNAL_BLOCK"},
                    {"blockId": "2", "blockType": "SIGNAL_BLOCK"},
                    {"blockId": "4", "blockType": "SIGNAL_BLOCK"},
                    {"blockId": "6", "blockType": "SIGNAL_BLOCK"},
                    {"blockId": "7", "blockType": "SIGNAL_BLOCK"},
                ],
            },
            "output": [{"blockType": "SIGNAL_BLOCK", "number": 1}],
        },
        output_interface={"interface": ["timestamp", "order"]},
    ).save()

    BlockRegistry(
        block_type="SIGNAL_BLOCK",
        block_id=4,
        block_name="Crossover",
        inputs=[
            {
                "fieldName": "Incoming Data",
                "fieldVariableName": "incoming_data",
                "fieldType": "inputs_from_connection",
                "fieldDefaultValue": "close",
            },
            {
                "fieldData": {"data": ["ABOVE", "BELOW"]},
                "fieldName": "Event Type",
                "fieldType": "dropdown",
                "fieldVariableName": "event_type",
            },
            {
                "fieldName": "Event Value",
                "fieldVariableName": "event_value",
                "fieldType": "input",
            },
            {
                "fieldData": {"data": ["BUY", "SELL"]},
                "fieldName": "Event Action",
                "fieldType": "dropdown",
                "fieldVariableName": "event_action",
            },
        ],
        validations={
            "input": {
                "required": [{"blockType": ["COMPUTATIONAL_BLOCK"], "number": 1}],
                "allowed_blocks": [
                    {"blockId": "1", "blockType": "COMPUTATIONAL_BLOCK"},
                    {"blockId": "2", "blockType": "COMPUTATIONAL_BLOCK"},
                    {"blockId": "1", "blockType": "DATA_BLOCK"},
                    {"blockId": "2", "blockType": "DATA_BLOCK"},
                ],
            },
            "output": [{"blockType": "SIGNAL_BLOCK", "number": 1}],
        },
        output_interface={"interface": ["timestamp", "order"]},
    ).save()

    BlockRegistry(
        block_type="SIGNAL_BLOCK",
        block_id=5,
        block_name="Or",
        inputs=[],
        validations={
            "input": {
                "required": [{"blockType": ["SIGNAL_BLOCK"], "number": 2}],
                "allowed_blocks": [
                    {"blockId": "1", "blockType": "SIGNAL_BLOCK"},
                    {"blockId": "2", "blockType": "SIGNAL_BLOCK"},
                    {"blockId": "4", "blockType": "SIGNAL_BLOCK"},
                    {"blockId": "6", "blockType": "SIGNAL_BLOCK"},
                    {"blockId": "7", "blockType": "SIGNAL_BLOCK"},
                ],
            },
            "output": [{"blockType": "SIGNAL_BLOCK", "number": 1}],
        },
        output_interface={"interface": ["timestamp", "order"]},
    ).save()

    BlockRegistry(
        block_type="SIGNAL_BLOCK",
        block_id=6,
        block_name="Candle Close",
        inputs=[
            {
                "fieldData": {
                    "data": [
                        "CLOSE_ABOVE_OPEN",
                        "CLOSE_BELOW_OPEN",
                        "CLOSE_EQ_HIGH",
                        "CLOSE_BELOW_HIGH",
                        "CLOSE_ABOVE_LOW",
                        "CLOSE_EQ_LOW",
                    ]
                },
                "fieldName": "Candle Close Type",
                "fieldType": "dropdown",
                "fieldVariableName": "event_type",
            },
            {
                "fieldData": {"data": ["BUY", "SELL"]},
                "fieldName": "Event Action",
                "fieldType": "dropdown",
                "fieldVariableName": "event_action",
            },
        ],
        validations={
            "input": {
                "required": [
                    {"blockType": ["DATA_BLOCK", "BULK_DATA_BLOCK"], "number": 1}
                ],
                "allowed_blocks": [
                    {"blockId": "1", "blockType": "DATA_BLOCK"},
                    {"blockId": "2", "blockType": "DATA_BLOCK"},
                    {"blockId": "1", "blockType": "BULK_DATA_BLOCK"},
                ],
            },
            "output": [{"blockType": "SIGNAL_BLOCK", "number": 1}],
        },
        output_interface={"interface": ["timestamp", "order"]},
    ).save()

    BlockRegistry(
        block_type="SIGNAL_BLOCK",
        block_id=7,
        block_name="Comparison",
        inputs=[
            {
                "fieldName": "Block One Incoming Data",
                "fieldVariableName": "incoming_data_one",
                "fieldType": "inputs_from_connection",
                "fieldDefaultValue": "close",
            },
            {
                "fieldData": {
                    "data": [
                        "<",
                        "<=",
                        ">",
                        ">=",
                    ]
                },
                "fieldName": "Comparison Type",
                "fieldType": "dropdown",
                "fieldVariableName": "comparison_type",
            },
            {
                "fieldName": "Block Two Incoming Data",
                "fieldVariableName": "incoming_data_two",
                "fieldType": "inputs_from_connection",
                "fieldDefaultValue": "close",
            },
            {
                "fieldData": {"data": ["BUY", "SELL"]},
                "fieldName": "Event Action",
                "fieldType": "dropdown",
                "fieldVariableName": "event_action",
            },
        ],
        validations={
            "input": {
                "required": [
                    {
                        "blockType": [
                            "DATA_BLOCK",
                            "BULK_DATA_BLOCK",
                            "COMPUTATIONAL_BLOCK",
                        ],
                        "number": 2,
                    }
                ],
                "allowed_blocks": [
                    {"blockId": "1", "blockType": "COMPUTATIONAL_BLOCK"},
                    {"blockId": "2", "blockType": "COMPUTATIONAL_BLOCK"},
                    {"blockId": "1", "blockType": "DATA_BLOCK"},
                    {"blockId": "2", "blockType": "DATA_BLOCK"},
                    {"blockId": "1", "blockType": "BULK_DATA_BLOCK"},
                ],
            },
            "output": [{"blockType": "SIGNAL_BLOCK", "number": 1}],
        },
        output_interface={"interface": ["timestamp", "order"]},
    ).save()

    BlockRegistry(
        block_type="STRATEGY_BLOCK",
        block_id=1,
        block_name="Simple Backtest",
        inputs=[
            {
                "fieldName": "Commission ($)",
                "fieldVariableName": "commission",
                "fieldType": "input",
            },
            {
                "fieldName": "Start Value ($)",
                "fieldVariableName": "start_value",
                "fieldType": "input",
            },
            {
                "fieldName": "Trade Amount Value ($)",
                "fieldVariableName": "trade_amount_value",
                "fieldType": "input",
            },
        ],
        validations={
            "input": {
                "required": [
                    {"blockType": ["DATA_BLOCK"], "number": 1},
                    {"blockType": ["SIGNAL_BLOCK"], "number": 1},
                ],
                "allowed_blocks": [
                    {"blockId": "1", "blockType": "SIGNAL_BLOCK"},
                    {"blockId": "2", "blockType": "SIGNAL_BLOCK"},
                    {"blockId": "3", "blockType": "SIGNAL_BLOCK"},
                    {"blockId": "4", "blockType": "SIGNAL_BLOCK"},
                    {"blockId": "5", "blockType": "SIGNAL_BLOCK"},
                    {"blockId": "6", "blockType": "SIGNAL_BLOCK"},
                    {"blockId": "7", "blockType": "SIGNAL_BLOCK"},
                    {"blockId": "1", "blockType": "DATA_BLOCK"},
                    {"blockId": "2", "blockType": "DATA_BLOCK"},
                ],
            },
            "output": [{"blockType": "STRATEGY_BLOCK", "number": 1}],
        },
        output_interface={"interface": ["trades", "portVals"]},
    ).save()


def reverse_blocks_into_registry(apps, schema_editor):
    BlockRegistry = apps.get_model("orchestrator", "BlockRegistry")
    BlockRegistry.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("orchestrator", "0001_block_registry"),
    ]

    operations = [
        migrations.RunPython(
            seed_blocks_into_registry, reverse_code=reverse_blocks_into_registry
        )
    ]
