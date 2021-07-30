from django.test import TestCase

from orchestrator.services.results.main import main


class ResultsTest(TestCase):
    def test_ok(self):
        payload = {
            "portVals": [
                {"value": 10000.0, "timestamp": "01/01/2020"},
                {"value": 10000.0, "timestamp": "01/02/2020"},
                {"value": 9910.0, "timestamp": "01/03/2020"},
                {"value": 9820.0, "timestamp": "01/04/2020"},
                {"value": 9820.0, "timestamp": "01/05/2020"},
            ],
            "trades": [
                {
                    "date": "01/02/2020",
                    "symbol": "close",
                    "order": "SELL",
                    "monetary_amount": 1000.0,
                    "trade_id": "",
                    "stop_loss": "",
                    "take_profit": "",
                    "shares": -90,
                    "cash_value": -990.0,
                },
                {
                    "date": "01/04/2020",
                    "symbol": "close",
                    "order": "BUY_CLOSE",
                    "monetary_amount": 0.0,
                    "trade_id": "",
                    "stop_loss": "",
                    "take_profit": "",
                    "shares": 90,
                    "cash_value": 1170.0,
                },
            ],
        }

        response = main(payload)

        self.assertDictEqual(
            response,
            {
                "cards": [
                    {"label": "Max Drawdowns", "value": -0.01799999999999997},
                    {"label": "Annual Return", "value": -0.599669218408968},
                    {"label": "Annual Volatility", "value": 0.08286261529783986},
                    {"label": "Calmar Ratio", "value": -33.31495657827605},
                    {"label": "Omega Ratio", "value": 0.0},
                    {"label": "Sharpe Ratio", "value": -13.747446179466248},
                    {"label": "Sortino Ratio", "value": -11.224857479414535},
                    {"label": "Downside Risk", "value": 0.10148452630120035},
                    {
                        "label": "Stability of Time Series",
                        "value": 0.891324427920153,
                    },
                    {"label": "Tail Ratio", "value": 0.0},
                    {"label": "CAGR", "value": -0.599669218408968},
                ],
                "graphs": [
                    {
                        "title": "Portfolio Values",
                        "data": [
                            {"value": 10000.0, "timestamp": "01/01/2020"},
                            {"value": 10000.0, "timestamp": "01/02/2020"},
                            {"value": 9910.0, "timestamp": "01/03/2020"},
                            {"value": 9820.0, "timestamp": "01/04/2020"},
                            {"value": 9820.0, "timestamp": "01/05/2020"},
                        ],
                    },
                    {
                        "title": "Portfolio Values Returns",
                        "data": [
                            {"value": 0.0, "timestamp": "01/02/2020"},
                            {
                                "value": -0.009000000000000008,
                                "timestamp": "01/03/2020",
                            },
                            {
                                "value": -0.00908173562058523,
                                "timestamp": "01/04/2020",
                            },
                            {"value": 0.0, "timestamp": "01/05/2020"},
                        ],
                    },
                    {
                        "title": "Cumulative Returns",
                        "data": [
                            {"value": 0.0, "timestamp": "01/01/2020"},
                            {"value": 0.0, "timestamp": "01/02/2020"},
                            {
                                "value": -0.009000000000000008,
                                "timestamp": "01/03/2020",
                            },
                            {
                                "value": -0.018000000000000016,
                                "timestamp": "01/04/2020",
                            },
                            {
                                "value": -0.018000000000000016,
                                "timestamp": "01/05/2020",
                            },
                        ],
                    },
                ],
                "tables": [
                    {
                        "title": "Trades",
                        "data": [
                            {
                                "date": "01/02/2020",
                                "symbol": "close",
                                "order": "SELL",
                                "monetary_amount": 1000.0,
                                "trade_id": "",
                                "stop_loss": "",
                                "take_profit": "",
                                "shares": -90,
                                "cash_value": -990.0,
                            },
                            {
                                "date": "01/04/2020",
                                "symbol": "close",
                                "order": "BUY_CLOSE",
                                "monetary_amount": 0.0,
                                "trade_id": "",
                                "stop_loss": "",
                                "take_profit": "",
                                "shares": 90,
                                "cash_value": 1170.0,
                            },
                        ],
                    }
                ],
            },
        )
