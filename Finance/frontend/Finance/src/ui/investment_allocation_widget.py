import streamlit as st
import pandas as pd


def investment_allocation_widget(
    stocks_selected,
    investment_amount,
    moving_average=None,
    threshold=None,
    existing_allocations=None,
    strategy="Mean Reversion",
):

    if not stocks_selected:
        return None

    threshold_options = ["5%", "10%", "15%", "20%", "25%"]
    existing_map = {}

    if existing_allocations is not None and not existing_allocations.empty:
        existing_map = existing_allocations.set_index("Stock").to_dict("index")

    with st.container(border=True):
        st.markdown("### Investment Allocation")

        if strategy == "Dollar Cost Average":
            allocation_mode = st.radio(
                "Allocation Method",
                options=["Evenly Allocate", "Custom Allocation"],
                horizontal=True,
                label_visibility="collapsed"
            )

            if allocation_mode == "Evenly Allocate":
                allocation_pct = 100 / len(stocks_selected)
                allocation_df = pd.DataFrame({
                    "Stock": stocks_selected,
                    "Allocation %": [allocation_pct] * len(stocks_selected),
                })

                if existing_allocations is not None and not existing_allocations.empty:
                    for stock in stocks_selected:
                        row = existing_map.get(stock)
                        if row is not None:
                            allocation_df.loc[allocation_df["Stock"] == stock, "Allocation %"] = row.get("Allocation %", allocation_pct)

            else:
                allocations = {}
                for stock in stocks_selected:
                    row = existing_map.get(stock, {})
                    allocations[stock] = st.slider(
                        stock,
                        min_value=0,
                        max_value=100,
                        value=int(row.get("Allocation %", round(100 / len(stocks_selected)))),
                        step=1,
                        format="%d%%",
                        key=f"dca_allocation_{stock}"
                    )

                allocation_df = pd.DataFrame({
                    "Stock": list(allocations.keys()),
                    "Allocation %": list(allocations.values()),
                })

        else:
            allocation_mode = st.radio(
                "Allocation Method",
                options=["Evenly Allocate", "Custom Allocation"],
                horizontal=True,
                label_visibility="collapsed"
            )

            # ---------------------------------------------------------
            # EVENLY ALLOCATE
            # ---------------------------------------------------------

            if allocation_mode == "Evenly Allocate":

                allocation_pct = 100 / len(stocks_selected)
                base_moving_average = int(moving_average) if moving_average is not None else 200
                base_threshold = threshold if threshold in threshold_options else "10%"

                allocation_df = pd.DataFrame({
                    "Stock": stocks_selected,
                    "Allocation %": [allocation_pct] * len(stocks_selected),
                    "Moving Average": [base_moving_average] * len(stocks_selected),
                    "Threshold %": [base_threshold] * len(stocks_selected),
                })

                if existing_allocations is not None and not existing_allocations.empty:
                    for stock in stocks_selected:
                        row = existing_map.get(stock)
                        if row is not None:
                            allocation_df.loc[allocation_df["Stock"] == stock, "Allocation %"] = row.get("Allocation %", allocation_pct)
                            allocation_df.loc[allocation_df["Stock"] == stock, "Moving Average"] = row.get("Moving Average", base_moving_average)
                            allocation_df.loc[allocation_df["Stock"] == stock, "Threshold %"] = row.get("Threshold %", base_threshold)

            # ---------------------------------------------------------
            # CUSTOM ALLOCATION
            # ---------------------------------------------------------

            else:

                allocations = {}
                moving_averages = {}
                thresholds = {}

                for stock in stocks_selected:
                    col_stock, col_allocation, col_ma, col_threshold = st.columns([2.5, 2, 1.7, 2])
                    row = existing_map.get(stock, {})

                    with col_stock:
                        st.write(stock)

                    with col_allocation:
                        allocations[stock] = st.slider(
                            f"{stock} allocation",
                            min_value=0,
                            max_value=100,
                            value=int(row.get("Allocation %", round(100 / len(stocks_selected)))),
                            step=1,
                            format="%d%%",
                            key=f"allocation_{stock}"
                        )

                    with col_ma:
                        moving_averages[stock] = st.number_input(
                            f"{stock} MA",
                            min_value=1,
                            value=int(row.get("Moving Average", int(moving_average) if moving_average is not None else 200)),
                            step=1,
                            key=f"ma_{stock}",
                            label_visibility="collapsed"
                        )

                    with col_threshold:
                        default_threshold = row.get("Threshold %", threshold if threshold in threshold_options else "10%")
                        thresholds[stock] = st.selectbox(
                            f"{stock} threshold",
                            options=threshold_options,
                            index=threshold_options.index(default_threshold) if default_threshold in threshold_options else 2,
                            key=f"threshold_{stock}",
                            label_visibility="collapsed"
                        )

                allocation_df = pd.DataFrame({
                    "Stock": list(allocations.keys()),
                    "Allocation %": list(allocations.values()),
                    "Moving Average": [moving_averages[stock] for stock in allocations.keys()],
                    "Threshold %": [thresholds[stock] for stock in allocations.keys()],
                })

    # ---------------------------------------------------------
    # CALCULATE INVESTMENT AMOUNT
    # ---------------------------------------------------------

    allocation_df["Investment Amount"] = (
        investment_amount *
        allocation_df["Allocation %"] / 100
    )

    # ---------------------------------------------------------
    # TOTAL
    # ---------------------------------------------------------

    total_allocation = allocation_df["Allocation %"].sum()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Allocation",
            f"{total_allocation:.0f}%"
        )

    with col2:
        if total_allocation == 100:
            st.success("Fully allocated")
        elif total_allocation < 100:
            st.info(
                f"{100 - total_allocation:.0f}% unallocated"
            )
        else:
            st.warning(
                f"{total_allocation - 100:.0f}% over-allocated"
            )

    if strategy == "Mean Reversion":
        data_columns = {
            "Stock": st.column_config.TextColumn("Stock", disabled=True),
            "Allocation %": st.column_config.NumberColumn("Allocation %", disabled=True, format="%.0f%%"),
            "Moving Average": st.column_config.NumberColumn("Moving Average", disabled=True, format="%.0f"),
            "Threshold %": st.column_config.TextColumn("Threshold %", disabled=True),
            "Investment Amount": st.column_config.NumberColumn("Investment Amount", disabled=True, format="$%.2f")
        }
    else:
        data_columns = {
            "Stock": st.column_config.TextColumn("Stock", disabled=True),
            "Allocation %": st.column_config.NumberColumn("Allocation %", disabled=True, format="%.0f%%"),
            "Investment Amount": st.column_config.NumberColumn("Investment Amount", disabled=True, format="$%.2f")
        }

    st.data_editor(
        allocation_df,
        column_config=data_columns,
        hide_index=True,
        use_container_width=True
    )

    return allocation_df