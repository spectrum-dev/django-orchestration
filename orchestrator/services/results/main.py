
import empyrical
import pandas as pd


def main(payload):
    port_vals_df = _convert_port_vals_to_df(payload["portVals"])
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
        "cards": [
            {"label": "Max Drawdowns", "value": max_drawdowns},
            {
                "label": "Annual Return",
                "value": annual_return,
                "type": "PERCENTAGE",
            },
            {
                "label": "Annual Volatility",
                "value": annual_volatility,
                "type": "PERCENTAGE",
            },
            {
                "label": "Calmar Ratio",
                "value": calmar_ratio,
                "type": "FIXED",
            },
            {
                "label": "Omega Ratio",
                "value": omega_ratio,
                "type": "FIXED",
            },
            {
                "label": "Sharpe Ratio",
                "value": sharpe_ratio,
                "type": "FIXED",
            },
            {
                "label": "Sortino Ratio",
                "value": sortino_ratio,
                "type": "FIXED",
            },
            {
                "label": "Downside Risk",
                "value": downside_risk,
                "type": "FIXED",
            },
            {
                "label": "Stability of Time Series",
                "value": stability_of_timeseries,
                "type": "FIXED",
            },
            {
                "label": "Tail Ratio",
                "value": tail_ratio,
                "type": "FIXED",
            },
            {
                "label": "CAGR",
                "value": cagr,
                "type": "FIXED",
            },
        ],
        "graphs": [
            {"title": "Portfolio Values", "data": payload["portVals"]},
            {
                "title": "Portfolio Values Returns",
                "data": _convert_df_to_json(port_vals_returns),
            },
            {
                "title": "Cumulative Returns",
                "data": _convert_df_to_json(cum_returns),
            },
        ],
        "tables": [{"title": "Trades", "data": payload["trades"]}],
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
