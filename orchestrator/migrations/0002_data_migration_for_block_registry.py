# Generated by Django 3.2 on 2021-04-15 13:23

from django.db import migrations


def seed_blocks_into_registry(apps, schema_editor):
    BlockRegistry = apps.get_model("orchestrator", "BlockRegistry")

    BlockRegistry(
        block_type="DATA_BLOCK",
        block_id=1,
        block_name="Raw Data",
        inputs=[
            {
                "fieldData": {
                    "base": "/equityName?name=",
                    "method": "GET",
                },
                "fieldName": "Equity Name",
                "fieldType": "search",
                "fieldVariableName": "equity_name",
            },  # TODO: Change fieldType from dropdown to search
            {
                "fieldData": {"base": "/dataType", "method": "GET"},
                "fieldName": "Data Type",
                "fieldType": "dropdown",
                "fieldVariableName": "data_type",
            },
            {
                "fieldData": {"base": "/interval", "method": "GET"},
                "fieldName": "Interval",
                "fieldType": "dropdown",
                "fieldVariableName": "interval",
            },
            {
                "fieldData": {"base": "/outputSize", "method": "GET"},
                "fieldName": "Output Size",
                "fieldType": "dropdown",
                "fieldVariableName": "outputsize",
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
    ).save()

    BlockRegistry(
        block_type="COMPUTATIONAL_BLOCK",
        block_id=1,
        block_name="Technical Analysis",
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
                "required": [{"blockType": "DATA_BLOCK", "number": 1}],
                "allowed_blocks": [{"blockId": "1", "blockType": "DATA_BLOCK"}],
            },
            "output": [{"blockType": "COMPUTATIONAL_BLOCK", "number": 1}],
        },
    ).save()

    BlockRegistry(
        block_type="SIGNAL_BLOCK",
        block_id=1,
        block_name="Event",
        inputs=[
            {
                "fieldData": {"base": "/eventType", "method": "GET"},
                "fieldName": "Event Type",
                "fieldType": "dropdown",
                "fieldVariableName": "event_type",
            },
            {
                "fieldData": {"base": "/eventAction", "method": "GET"},
                "fieldName": "Event Action",
                "fieldType": "dropdown",
                "fieldVariableName": "event_action",
            },
        ],
        validations={
            "input": {
                "required": [{"blockType": "COMPUTATIONAL_BLOCK", "number": 2}],
                "allowed_blocks": [
                    {"blockId": "1", "blockType": "COMPUTATIONAL_BLOCK"}
                ],
            },
            "output": [{"blockType": "SIGNAL_BLOCK", "number": 1}],
        },
    ).save()

    BlockRegistry(
        block_type="SIGNAL_BLOCK",
        block_id=2,
        block_name="Saddle",
        inputs=[
            {
                "fieldData": {"base": "/saddleType", "method": "GET"},
                "fieldName": "Saddle Type",
                "fieldType": "dropdown",
                "fieldVariableName": "saddle_type",
            },
            {
                "fieldData": {"base": "/eventAction", "method": "GET"},
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
                "required": [{"blockType": "COMPUTATIONAL_BLOCK", "number": 1}],
                "allowed_blocks": [
                    {"blockId": "1", "blockType": "COMPUTATIONAL_BLOCK"}
                ],
            },
            "output": [{"blockType": "SIGNAL_BLOCK", "number": 2}],
        },
    ).save()

    BlockRegistry(
        block_type="STRATEGY_BLOCK",
        block_id=1,
        block_name="Backtest",
        inputs=[
            {
                "fieldName": "Commission",
                "fieldVariableName": "commission",
                "fieldType": "input",
            },
            {
                "fieldName": "Impact",
                "fieldVariableName": "impact",
                "fieldType": "input",
            },
            {
                "fieldName": "Start Value",
                "fieldVariableName": "start_value",
                "fieldType": "input",
            },
            {
                "fieldName": "Stop Loss",
                "fieldVariableName": "stop_loss",
                "fieldType": "input",
            },
            {
                "fieldName": "Take Profit",
                "fieldVariableName": "take_profit",
                "fieldType": "input",
            },
            {
                "fieldName": "Trade Amount",
                "fieldVariableName": "trade_amount_value",
                "fieldType": "input",
            },
        ],
        validations={
            "input": {
                "required": [
                    {"blockType": "DATA_BLOCK", "number": 1},
                    {"blockType": "SIGNAL_BLOCK", "number": 1},
                ],
                "allowed_blocks": [
                    {"blockId": "1", "blockType": "SIGNAL_BLOCK"},
                    {"blockId": "1", "blockType": "DATA_BLOCK"},
                ],
            },
            "output": [{"blockType": "STRATEGY_BLOCK", "number": 1}],
        },
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
