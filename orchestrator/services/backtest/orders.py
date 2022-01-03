import pandas as pd


class Orders:
    def __init__(self):
        self.trades_df = pd.DataFrame(
            columns=[
                "timestamp",
                "symbol",
                "order",
                "monetary_amount",
                "trade_id",
                "stop_loss",
                "take_profit",
            ]
        )

    def buy(self, timestamp, symbol, monetary_amount, trade_id, stop_loss, take_profit):
        """
        Processes a BUY Request

        Attributes
        ----------
        timestamp       :       Datetime New Trade is Placed
        symbol          :       Ticker of stock purchased
        amount          :       Number of Shares Purchased
        trade_id        :       Unique ID of Each Trade
        stop_loss       :       Stop Loss Buffer for User
        take_profit     :       Auto-Sell Price Level
        """

        self.trades_df = self.trades_df.append(
            {
                "timestamp": timestamp,
                "symbol": symbol,
                "order": "BUY",
                "monetary_amount": monetary_amount,
                "trade_id": trade_id,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
            },
            ignore_index=True,
        )

    def sell(
        self, timestamp, symbol, monetary_amount, trade_id, stop_loss, take_profit
    ):
        """
        Processes a SELL Request

        Attributes
        ----------
        timestamp       :       Datetime New Trade is Placed
        symbol          :       Ticker of stock purchased
        amount          :       Number of Shares Purchased
        trade_id        :       Unique ID of Each Trade
        stop_loss       :       Stop Loss Buffer for User
        take_profit     :       Auto-Sell Price Level
        """

        self.trades_df = self.trades_df.append(
            {
                "timestamp": timestamp,
                "symbol": symbol,
                "order": "SELL",
                "monetary_amount": monetary_amount,
                "trade_id": trade_id,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
            },
            ignore_index=True,
        )

    def buy_close(self, timestamp, symbol, trade_id, stop_loss, take_profit):
        """
        Processes a BUY CLOSE Request

        Attributes
        ----------
        timestamp       :       Datetime New Trade is Placed
        symbol          :       Ticker of stock purchased
        amount          :       Number of Shares Purchased
        trade_id        :       Unique ID of Each Trade
        stop_loss       :       Stop Loss Buffer for User
        take_profit     :       Auto-Sell Price Level
        """

        self.trades_df = self.trades_df.append(
            {
                "timestamp": timestamp,
                "symbol": symbol,
                "order": "BUY_CLOSE",
                "monetary_amount": 0,
                "trade_id": trade_id,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
            },
            ignore_index=True,
        )

    def sell_close(self, timestamp, symbol, trade_id, stop_loss, take_profit):
        """
        Processes a SELL Request

        Attributes
        ----------
        timestamp       :       Datetime New Trade is Placed
        symbol          :       Ticker of stock purchased
        amount          :       Number of Shares Purchased
        trade_id        :       Unique ID of Each Trade
        stop_loss       :       Stop Loss Buffer for User
        take_profit     :       Auto-Sell Price Level
        """

        self.trades_df = self.trades_df.append(
            {
                "timestamp": timestamp,
                "symbol": symbol,
                "order": "SELL_CLOSE",
                "monetary_amount": 0,
                "trade_id": trade_id,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
            },
            ignore_index=True,
        )
