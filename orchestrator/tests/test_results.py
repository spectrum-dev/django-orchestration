from django.test import TestCase

from orchestrator.services.results.main import main


class ResultsTest(TestCase):
    def test_ok(self):
        payload = {
            "response": {
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
        }

        response = main(payload)

        self.assertDictEqual(
            response,
            {
                "response": {
                    "port_vals": [
                        {"value": 10000.0, "timestamp": "01/01/2020"},
                        {"value": 10000.0, "timestamp": "01/02/2020"},
                        {"value": 9910.0, "timestamp": "01/03/2020"},
                        {"value": 9820.0, "timestamp": "01/04/2020"},
                        {"value": 9820.0, "timestamp": "01/05/2020"},
                    ],
                    "port_vals_returns": [
                        {"value": 0.0, "timestamp": "01/02/2020"},
                        {"value": -0.009000000000000008, "timestamp": "01/03/2020"},
                        {"value": -0.00908173562058523, "timestamp": "01/04/2020"},
                        {"value": 0.0, "timestamp": "01/05/2020"},
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
                    "cum_returns": [
                        {"value": 0.0, "timestamp": "01/01/2020"},
                        {"value": 0.0, "timestamp": "01/02/2020"},
                        {"value": -0.009000000000000008, "timestamp": "01/03/2020"},
                        {"value": -0.018000000000000016, "timestamp": "01/04/2020"},
                        {"value": -0.018000000000000016, "timestamp": "01/05/2020"},
                    ],
                    "max_drawdowns": -0.01799999999999997,
                    "annual_return": -0.599669218408968,
                    "annual_volatility": 0.08286261529783986,
                    "calmar_ratio": -33.31495657827605,
                    "omega_ratio": 0.0,
                    "sharpe_ratio": -13.747446179466248,
                    "sortino_ratio": -11.224857479414535,
                    "downside_risk": 0.10148452630120035,
                    "stability_of_timeseries": 0.891324427920153,
                    "tail_ratio": 0.0,
                    "cagr": -0.599669218408968,
                }
            },
        )
