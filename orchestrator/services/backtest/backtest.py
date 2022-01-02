import pandas as pd
from pydantic import BaseModel
from utils.utils import retrieve_block_data, validate_payload

from .exceptions import StrategyBlockOneInvalidInputPayloadException
from .marketsim import run as run_marketsim
from .orders import Orders


class InputPayload(BaseModel):
    start_value: float
    commission: float
    trade_amount_value: float


def run(input: dict, output: dict) -> dict:
    """
    Simple Backtest Block: Completes the flow and runs the backtest

    Args:
        input (dict): Input payload from flow
        output (dict): Data payload from flow

    Returns:
        dict: Dictionary of portfolio values and trades placed at different time points
    """
    input = validate_payload(
        InputPayload, input, StrategyBlockOneInvalidInputPayloadException
    )
    selectable_data = {
        "data_block": ["DATA_BLOCK", "BULK_DATA_BLOCK"],
        "signal_block": ["SIGNAL_BLOCK"],
    }
    block_data = retrieve_block_data(selectable_data, output)

    if len(block_data["data_block"]) <= 0 or len(block_data["signal_block"]) <= 0:
        return {"response": {"portVals": [], "trades": []}}

    data_block_df = _generate_data_block_df(block_data["data_block"])
    signal_block_df = _generate_signal_block_df(block_data["signal_block"])
    trades_df = _generate_trades_df(input, signal_block_df)

    # TODO: Implement the marketsim
    port_vals, trades_df = run_marketsim(
        trades_df,
        data_block_df,
        input.start_value,
        input.commission,
    )

    # Generates Responses
    port_vals = _generate_port_vals_response(port_vals)
    trades = _generate_trades_df_response(trades_df)

    return {"response": {"portVals": port_vals, "trades": trades}}


def _generate_data_block_df(data_block):
    """
    Generates a Data Block DF

    Attributes
    ----------

    data_block: Incoming Data Block DF
    """
    data_block_df = pd.DataFrame(data_block)
    data_block_df = data_block_df.sort_values(by="timestamp")
    data_block_df = data_block_df.set_index("timestamp")

    return data_block_df


def _generate_signal_block_df(signal_block):
    """
    Generates a dataframe for the signals

    Attributes
    ----------
    signal_block: Incoming Signal Block JSON
    """
    signal_block_df = pd.DataFrame(
        columns=["timestamp", "buy", "sell", "buy_close", "sell_close"],
    )
    signal_block_df = signal_block_df.set_index("timestamp")

    for i in range(0, len(signal_block)):
        # Returns boolean of whether should BUY or SELL
        buy = signal_block[i]["order"] == "BUY"
        sell = signal_block[i]["order"] == "SELL"

        not_purchased = True
        if i >= 1:
            if buy and signal_block[i - 1]["order"] == "SELL":
                signal_block_df = signal_block_df.append(
                    {
                        "timestamp": signal_block[i]["timestamp"],
                        "buy": False,
                        "sell": False,
                        "sell_close": False,
                        "buy_close": True,
                    },
                    ignore_index=True,
                )
                not_purchased = False
            elif sell and signal_block[i - 1]["order"] == "BUY":
                signal_block_df = signal_block_df.append(
                    {
                        "timestamp": signal_block[i]["timestamp"],
                        "buy": False,
                        "sell": False,
                        "sell_close": True,
                        "buy_close": False,
                    },
                    ignore_index=True,
                )
                not_purchased = False

        if not_purchased:
            signal_block_df = signal_block_df.append(
                {
                    "timestamp": signal_block[i]["timestamp"],
                    "buy": buy,
                    "sell": sell,
                    "sell_close": False,
                    "buy_close": False,
                },
                ignore_index=True,
            )

    signal_block_df = signal_block_df.set_index("timestamp")
    return signal_block_df


def _generate_trades_df(input, signal_block_df):
    """
    Generates the trades dataframe

    Attributes
    ----------
    input: Form Input
    signal_block_df: The DataFrame of signals generated earlier
    """
    orders = Orders()

    trade_amount = input.trade_amount_value

    for index, row in signal_block_df.iterrows():
        if row["buy"]:
            orders.buy(index, "close", trade_amount, "", "", "")
        elif row["sell"]:
            orders.sell(index, "close", trade_amount, "", "", "")
        elif row["buy_close"]:
            orders.buy_close(index, "close", "", "", "")
        elif row["sell_close"]:
            orders.sell_close(index, "close", "", "", "")

    return orders.trades_df


def _generate_port_vals_response(port_vals):
    """
    Generates JSON response from port_vals

    Attributes
    ----------
    port_vals: List of Portfolio Values
    """
    port_vals_df = port_vals.to_frame()
    port_vals_df = port_vals_df.rename(columns={0: "value"})
    port_vals_df["timestamp"] = port_vals_df.index

    port_vals = port_vals_df.to_dict(orient="records")

    return port_vals


def _generate_trades_df_response(trades_df):
    """
    Generates JSON response from trades

    Attributes
    ----------
    trades_df: DataFrame of Trades
    """
    trades_df = trades_df.drop(
        columns=["symbol", "trade_id", "stop_loss", "take_profit"]
    )

    trades_df = trades_df.rename(
        columns={
            "cash_value": "amount_invested",
            "monetary_amount": "cash_allocated",
        }
    )

    trades_df = trades_df.round(2)
    trades = trades_df.to_dict(orient="records")

    return trades
