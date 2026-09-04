import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.lakehouse import sql_query, get_tickers

def mean_reversion(stock:str, ma:int, threshold:str):

    threshold = int(threshold[0].replace("%",""))/100

    query =f""" 
    WITH price_data AS (

                SELECT 
                dd.date_value,
                fa.adj_close,
                dc.company_stock_symbol,
                AVG(fa.adj_close) OVER (partition by dc.company_stock_symbol ORDER BY dd.date_value ROWS BETWEEN {int(ma)-1} PRECEDING AND CURRENT ROW) AS moving_avg
                FROM operations.finance.fact_price_daily fa
                LEFT JOIN operations.finance.dim_company dc ON dc.company_bigint_key = fa.company_bigint_key
                LEFT JOIN operations.finance.dim_date dd ON dd.date_key = fa.date_key
                WHERE dc.company_stock_symbol = '{stock}'
            ),

            indicators AS (

                SELECT
                    *,
                    ((adj_close - moving_avg) / moving_avg) * 100 AS pct_from_ma,
                    LAG(adj_close) OVER (partition by company_stock_symbol ORDER BY date_value) AS previous_price
                FROM price_data
            )

            SELECT
                date_value,
                company_stock_symbol,
                adj_close,
                moving_avg,
                pct_from_ma,
                previous_price,

                CASE
                when adj_close < moving_avg * (1-{threshold}) AND adj_close > previous_price THEN 'BUY'
                when adj_close > moving_avg * (1+{threshold}) AND adj_close < previous_price THEN 'SELL'
                ELSE 'HOLD'
                END AS signal

            FROM indicators

            ORDER BY date_value, company_stock_symbol;
            """
    
    df = sql_query(sql_query=query)

    df["date_value"] = pd.to_datetime(df["date_value"])
    df["adj_close"] = pd.to_numeric(df["adj_close"], errors="coerce")
    df['moving_avg'] = pd.to_numeric(df['moving_avg'], errors="coerce")

    # =========================================================
    # Create Figure
    # =========================================================

    fig = go.Figure()

    # =========================================================
    # Price
    # =========================================================

    fig.add_trace(
        go.Scatter(
            x=df["date_value"],
            y=df["adj_close"],
            mode="lines",
            name=stock,
        )
    )

    # =========================================================
    # Moving Average
    # =========================================================

    fig.add_trace(
        go.Scatter(
            x=df["date_value"],
            y=df["moving_avg"],
            mode="lines",
            name=f"{stock} {int(ma)}-Day MA",
            line=dict(
                dash="dash"
            ),
            opacity=0.6
        )
    )

    # =========================================================
    # BUY markers
    # =========================================================

    buy_df = df[df["signal"] == "BUY"]

    fig.add_trace(
        go.Scatter(
            x=buy_df["date_value"],
            y=buy_df["adj_close"],
            mode="markers",
            name="BUY",
            marker=dict(
                color="green",
                size=10,
                symbol="triangle-up"
            )
        )
    )

    # =========================================================
    # SELL markers
    # =========================================================

    sell_df = df[df["signal"] == "SELL"]

    fig.add_trace(
        go.Scatter(
            x=sell_df["date_value"],
            y=sell_df["adj_close"],
            mode="markers",
            name="SELL",
            marker=dict(
                color="red",
                size=10,
                symbol="triangle-down"
            )
        )
    )

    # =========================================================
    # Axis formatting
    # =========================================================

    y_min = df["adj_close"].min()
    y_max = df["adj_close"].max()

    padding = (y_max - y_min) * 0.01

    fig.update_yaxes(
        range=[
            y_min - padding,
            y_max + padding
        ],
        title="Adjusted Close Price"
    )

    fig.update_xaxes(
        title="Date"
    )

    fig.update_layout(
        title=f"{stock} Mean Reversion Strategy",
        hovermode="x unified",
        legend_title="Indicator"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )