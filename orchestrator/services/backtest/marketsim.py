import math

import numpy as np
import pandas as pd


def run(orders_df, price_df, start_val, commission, impact=0):
    # 1. Sort by dates in order file
    #    Creates a copy of the orders df to be stored later

    final_orders_df = orders_df.copy(deep=True)

    orders_df = orders_df.sort_values(["timestamp"], ascending=True)

    orders_df = orders_df.set_index("timestamp")

    # 2. Build data frame prices (prices should be adjusted close)
    price_df = _create_price_df(price_df, colname="close")

    # 3. Build data frame trades

    # Represents Changes
    trades_df = pd.DataFrame().reindex_like(price_df)
    trades_df[:] = 0

    # Instantiates New Fields in Orders DF
    final_orders_df["shares"] = 0
    final_orders_df["cash_value"] = 0

    shares = []
    cash_value = []
    # Iterator for final_orders_df
    i = 0
    for index, order in orders_df.iterrows():
        price = float(price_df.loc[index]["close"])
        order_type = order["order"]

        monetary_amount = int(order["monetary_amount"])

        share_amount = int(math.floor(monetary_amount / price))

        if order_type == "SELL":
            price *= 1 - impact
            trades_df["Cash"].loc[index] += price * share_amount - commission
            share_amount *= -1
        elif order_type == "BUY":
            price *= -1 * (1 + impact)
            trades_df["Cash"].loc[index] += price * share_amount - commission
        elif order_type == "SELL_CLOSE":
            share_amount = shares[i - 1]
            price *= 1 - impact
            trades_df["Cash"].loc[index] += price * share_amount - commission
            share_amount *= -1
        elif order_type == "BUY_CLOSE":
            share_amount = -1 * shares[i - 1]
            price *= -1 * (1 + impact)
            trades_df["Cash"].loc[index] += price * share_amount - commission

        trades_df[order["symbol"]].loc[index] = int(
            trades_df[order["symbol"]].loc[index]
        ) + int(share_amount)

        shares.append(share_amount)
        cash_value.append(abs(price) * share_amount)

        i += 1

    final_orders_df["shares"] = shares
    final_orders_df["cash_value"] = cash_value

    # 4. Creates holdings data frames

    holdings_df = trades_df.cumsum()
    holdings_df["Cash"] = holdings_df["Cash"] + start_val

    # Convert both DF's to float
    # TODO: Find the root cause of the type mismatch

    holdings_df["close"] = holdings_df["close"].astype(float)
    holdings_df["Cash"] = holdings_df["Cash"].astype(float)

    price_df["close"] = price_df["close"].astype(float)
    price_df["Cash"] = price_df["Cash"].astype(float)

    # 5. Creates dataframe values

    values_df = price_df * holdings_df

    # 6. Creates dataframe portvals

    portvals = values_df.sum(axis=1)

    # 7. Returns dataframe

    return portvals, final_orders_df


def _create_price_df(price_df, colname="adjusted_close"):
    price_df = price_df[colname].to_frame()

    price_df = price_df.fillna(method="bfill")
    price_df = price_df.fillna(method="ffill")

    # Creates a cash column and fills it with ones
    price_df["Cash"] = np.ones(len(price_df))

    return price_df
