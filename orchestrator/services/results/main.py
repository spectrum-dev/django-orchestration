import pandas as pd
import empyrical


def main(payload):
    port_vals_df = _convert_port_vals_to_df(payload["response"]["portVals"])
    # Calculates per data point returns
    port_vals_returns = port_vals_df["value"].pct_change()

    cum_returns = empyrical.cum_returns(port_vals_returns, starting_value=0)
    # aggregate_returns = empyrical.aggregate_returns(port_vals_returns, convert_to='weekly')
    max_drawdowns = empyrical.max_drawdown(port_vals_returns)
    annual_return = empyrical.annual_return(
        port_vals_returns, period="daily", annualization=None
    )
    annual_volatility = empyrical.annual_volatility(
        port_vals_returns, period="daily", alpha=2.0, annualization=None
    )
    calmar_ratio = empyrical.calmar_ratio(
        port_vals_returns, period="daily", annualization=None
    )
    omega_ratio = empyrical.omega_ratio(
        port_vals_returns, risk_free=0.0, required_return=0.0, annualization=1
    )
    sharpe_ratio = empyrical.sharpe_ratio(
        port_vals_returns, risk_free=0, period="daily", annualization=None
    )
    sortino_ratio = empyrical.sortino_ratio(
        port_vals_returns,
        required_return=0,
        period="daily",
        annualization=None,
        _downside_risk=None,
    )
    downside_risk = empyrical.downside_risk(
        port_vals_returns, required_return=0, period="daily", annualization=None
    )
    stability_of_timeseries = empyrical.stability_of_timeseries(port_vals_returns)
    tail_ratio = empyrical.tail_ratio(port_vals_returns)
    cagr = empyrical.cagr(port_vals_returns, period="daily", annualization=None)

    # TODO: These are for benchmarking against stocks and indexes
    # information_ratio = empyrical.information_ratio(port_vals_returns, 0.3)
    # alpha_beta = empyrical.alpha_beta(port_vals_returns, factor_returns, risk_free=0.0, period='daily', annualization=None)
    # alpha = empyrical.alpha(port_vals_returns, factor_returns, risk_free=0.0, period='daily', annualization=None, _beta=None)
    # beta = empyrical.beta(port_vals_returns, factor_returns, risk_free=0.0)

    return {
        "response": {
            "port_vals": payload["response"]["portVals"],
            "port_vals_returns": _convert_df_to_json(port_vals_returns),
            "trades": payload["response"]["trades"],
            "cum_returns": _convert_df_to_json(cum_returns),
            "max_drawdowns": max_drawdowns,
            "annual_return": annual_return,
            "annual_volatility": annual_volatility,
            "calmar_ratio": calmar_ratio,
            "omega_ratio": omega_ratio,
            "sharpe_ratio": sharpe_ratio,
            "sortino_ratio": sortino_ratio,
            "downside_risk": downside_risk,
            "stability_of_timeseries": stability_of_timeseries,
            "tail_ratio": tail_ratio,
            "cagr": cagr,
        }
    }


def _convert_port_vals_to_df(port_vals):
    df = pd.DataFrame.from_dict(port_vals, orient="columns")
    df = df.set_index("timestamp")
    return df


def _convert_df_to_json(series):
    df = series.to_frame(name="value")
    df["timestamp"] = df.index
    df = df.dropna()
    response = df.to_dict(orient="records")

    return response


# TODO: Remove Later
def main_debug():
    data = [["2015-12-1", 0.0], ["2015-12-2", 0.5], ["2015-12-3", -0.2]]

    stock_rets = pd.DataFrame(data, columns=["date", "close"])
    stock_rets["new_date"] = pd.to_datetime(stock_rets["date"], format="%Y-%m-%d")

    stock_rets = stock_rets.set_index("new_date")
    stock_rets = stock_rets.drop(["date"], axis=1)

    print(stock_rets["close"])

    # TODO: Figure out how to get returns array
    stock_rets_np = np.array([0.01, 0.02, 0.03, -0.4, -0.06, -0.02])

    # response = empyrical.cum_returns(stock_rets['close'], starting_value=0)
    response = empyrical.max_drawdown(stock_rets_np)
    # response = empyrical.sharpe_ratio(stock_rets['close'])
    # response = empyrical.annual_return(stock_rets['close'])
    print(response)

    return None
