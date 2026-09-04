import streamlit as st
import pandas as pd
from ui.session_manager import create_session
from data.lakehouse import sql_query
from ui.investment_allocation_widget import investment_allocation_widget
from pages.strategy_mean_reversion import mean_reversion

@st.dialog("Create Session",width="large")
def create_session_dialog(edit_session_id: str | None = None):
    st.write("Build a trading strategy")

    existing_session = None
    if edit_session_id:
        from ui.session_manager import get_session
        existing_session = get_session(edit_session_id)

    session_name = st.text_input(
        "Session Name",
        placeholder="Enter a name...",
        value=existing_session["session_name"] if existing_session else ""
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        asset_type_options = ['Stocks', 'ETF', 'Index']
        asset_type = st.selectbox(
            "Asset Type",
            options=asset_type_options,
            index=asset_type_options.index(existing_session["asset_type"]) if existing_session else 0
        )
    with col2:
        if asset_type == 'Stocks':

            stocks = """select distinct dc.company_stock_symbol from operations.finance.fact_price_daily fa
            left join operations.finance.dim_company dc on dc.company_bigint_key = fa.company_bigint_key
            where fa.asset_type = 'Stock'
            order by company_stock_symbol asc"""

            stocks_list = sql_query(stocks).iloc[:,0].tolist()
            selected_stocks = []
            if existing_session and existing_session.get("allocations") is not None:
                selected_stocks = list(pd.DataFrame(existing_session["allocations"])["Stock"].tolist())
            stocks_selected = st.multiselect(
                label='Stocks',
                options=stocks_list,
                default=selected_stocks,
                placeholder='Select a stocks'
            )

        if asset_type == 'Index':

            index =  """select distinct dc.company_stock_symbol from operations.finance.fact_price_daily fa
            left join operations.finance.dim_company dc on dc.company_bigint_key = fa.company_bigint_key
            where fa.asset_type = 'Index'
            order by company_stock_symbol asc"""
            
            index_list = sql_query(index).iloc[:,0].tolist()
            st.multiselect(label='Index List', options = index_list, placeholder = 'Select a index...')

    with col3:
        strategy_options = ['Dollar Cost Average', 'Mean Reversion']
        strategy = st.selectbox(
            "Strategy",
            options=strategy_options,
            index=strategy_options.index(existing_session["strategy"]) if existing_session else None,
            placeholder='Select a strategy...'
        )

    #################################dollar cost average strategy#################################  
    if strategy == "Dollar Cost Average":

        col1, col2, col3 = st.columns(3)
        
        with col1:
            investment_amount = st.number_input(
                "Investment Amount",
                min_value = 0.0,
                step=100.0,
                value=float(existing_session["investment_amount"]) if existing_session else 1000.0
            )
        with col2: 
            frequency = st.selectbox(
                "Investment Frequency",
                options=['Daily',"Weekly","Bi-Weekly","Monthly"],
                index=['Daily',"Weekly","Bi-Weekly","Monthly"].index(existing_session["frequency"]) if existing_session and existing_session.get("frequency") in ['Daily','Weekly','Bi-Weekly','Monthly'] else 0
            )
        
        with col3:
            if frequency == 'Daily':
                pass

            elif frequency == "Weekly":
                day_options = ['Monday',"Tuesday","Wednesday",'Thursday','Friday']
                day_of_week = st.selectbox(
                    "Day of Week",
                    options=day_options,
                    index=day_options.index(existing_session["day_of_week"]) if existing_session and existing_session.get("day_of_week") in day_options else 0
                )
            elif frequency == "Bi-Weekly":
                day_options = ['Monday',"Tuesday","Wednesday",'Thursday','Friday']
                day_of_week = st.selectbox(
                    "Day of Week",
                    options=day_options,
                    index=day_options.index(existing_session["day_of_week"]) if existing_session and existing_session.get("day_of_week") in day_options else 0
                )
            elif frequency == "Monthly":
                month_options = ['First Trading day of Month', 'Last Trading day of Month']
                day_of_week = st.selectbox(
                    "Beginning/End of Month",
                    options = month_options,
                    index=month_options.index(existing_session["day_of_week"]) if existing_session and existing_session.get("day_of_week") in month_options else 0
                )
        
        col4, col5 = st.columns(2)

        with col4:
            allocation_df = investment_allocation_widget(
                stocks_selected,
                investment_amount,
                moving_average=moving_average if 'moving_average' in locals() else None,
                threshold=threshold if 'threshold' in locals() else None,
                existing_allocations=pd.DataFrame(existing_session["allocations"]) if existing_session and existing_session.get("allocations") is not None else None,
                strategy="Dollar Cost Average",
            )

            allocation_values = ", ".join(
            f"('{row['Stock']}', {row['Allocation %']}, {row['Investment Amount']})"
            for _, row in allocation_df.iterrows()
            )

    #################################mean reversion strategy#################################       
    elif strategy == 'Mean Reversion':

        col1, col2, col3 = st.columns(3)

        with col1: 
            investment_amount = st.number_input(
                "Investment Amount",
                min_value = 0.0,
                step=100.0,
                value=float(existing_session["investment_amount"]) if existing_session else 1000.0
            )

        with col2:
            default_ma = existing_session.get("moving_average") if existing_session and isinstance(existing_session.get("moving_average"), int) else 200
            moving_average = st.number_input(
                "Moving Average",
                min_value=1,
                value=default_ma
            )
        
        with col3:
            threshold_options = ['5%','10%','15%','20%','25%']
            default_threshold = None
            if existing_session:
                existing_threshold = existing_session.get("threshold")
                if isinstance(existing_threshold, dict):
                    default_threshold = existing_threshold.get(stocks_selected[0], threshold_options[2]) if stocks_selected else threshold_options[2]
                elif isinstance(existing_threshold, str) and existing_threshold in threshold_options:
                    default_threshold = existing_threshold
            threshold = st.selectbox(
                "Buy/Sell % Threshold",
                options=threshold_options,
                index=threshold_options.index(default_threshold) if default_threshold in threshold_options else 2
            )
        
        col4, col5 = st.columns(2)

        with col4:
            allocation_df = investment_allocation_widget(
                stocks_selected,
                investment_amount,
                moving_average=moving_average,
                threshold=threshold,
                existing_allocations=pd.DataFrame(existing_session["allocations"]) if existing_session and existing_session.get("allocations") is not None else None,
                strategy="Mean Reversion",
            )

            allocation_values = ", ".join(
            f"('{row['Stock']}', {row['Allocation %']}, {row['Investment Amount']})"
            for _, row in allocation_df.iterrows()
            )

#################################Section for brief view of how strategy looks in selected time period#################################
    if st.button("Quick Test", type='primary',use_container_width=None):

        if strategy == "Dollar Cost Average":

            col1, col2 = st.columns(2)

            with col1:

                stocks_selected_list = ", ".join(f"'{t}'" for t in stocks_selected)

                if frequency == "Daily":
                    window_days = 30
                    schedule_sql = "1 = 1"
                    final_select_sql = "select * from strategy_output order by date_value asc, company_stock_symbol asc"
                elif frequency == "Weekly":
                    window_days = 70
                    schedule_sql = f"date_format(dd.date_value, 'EEEE') = '{day_of_week}'"
                    final_select_sql = "select * from strategy_output order by date_value asc, company_stock_symbol asc"
                elif frequency == "Bi-Weekly":
                    window_days = 140
                    schedule_sql = f"date_format(dd.date_value, 'EEEE') = '{day_of_week}' and mod(cast(datediff(dd.date_value, date '2000-01-03') / 7 as int), 2) = 0"
                    final_select_sql = """
                        select *
                        from (
                            select *,
                                row_number() over (partition by company_stock_symbol order by gain_by_trade desc) as rn
                            from strategy_output
                        )
                        where rn <= 10
                        order by company_stock_symbol asc, gain_by_trade desc
                    """
                elif frequency == "Monthly":
                    window_days = 180
                    if day_of_week == "First Trading day of Month":
                        month_filter = "first_rank = 1"
                    else:
                        month_filter = "last_rank = 1"
                    final_select_sql = "select * from strategy_output order by date_value asc, company_stock_symbol asc"
                else:
                    window_days = 70
                    schedule_sql = "1 = 1"
                    final_select_sql = "select * from strategy_output order by date_value asc, company_stock_symbol asc"

                if frequency == "Monthly":
                    query = f"""
                        with allocation as (
                            select *
                            from values
                            {allocation_values}
                            as allocation(company_stock_symbol, allocation_pct, investment_amount)
                        )
                        ,month_ranked as (
                            select
                                dd.date_value,
                                dc.company_stock_symbol,
                                fa.adj_close as adjusted_close,
                                row_number() over (
                                    partition by dc.company_stock_symbol, date_trunc('month', dd.date_value)
                                    order by dd.date_value asc
                                ) as first_rank,
                                row_number() over (
                                    partition by dc.company_stock_symbol, date_trunc('month', dd.date_value)
                                    order by dd.date_value desc
                                ) as last_rank
                            from operations.finance.fact_price_daily fa
                            left join operations.finance.dim_date dd on dd.date_key = fa.date_key
                            left join operations.finance.dim_company dc on dc.company_bigint_key = fa.company_bigint_key
                            where dc.company_stock_symbol in ({stocks_selected_list})
                            and dd.date_value >= date_add(current_date(), -{window_days})
                        )
                        ,selected_dates as (
                            select date_value, company_stock_symbol, adjusted_close
                            from month_ranked
                            where {month_filter}
                        )
                        ,price_latest as (
                            select company_stock_symbol, adjusted_close
                            from (
                                select
                                    dc.company_stock_symbol,
                                    fa.adj_close as adjusted_close,
                                    row_number() over (
                                        partition by dc.company_stock_symbol
                                        order by dd.date_value desc
                                    ) as rn
                                from operations.finance.fact_price_daily fa
                                left join operations.finance.dim_date dd on dd.date_key = fa.date_key
                                left join operations.finance.dim_company dc on dc.company_bigint_key = fa.company_bigint_key
                                where dc.company_stock_symbol in ({stocks_selected_list})
                            )
                            where rn = 1
                        )
                        ,strategy_output as (
                            select
                                selected_dates.date_value,
                                selected_dates.company_stock_symbol,
                                allocation.allocation_pct,
                                allocation.investment_amount,
                                round(selected_dates.adjusted_close, 2) as adjusted_close,
                                round(price_latest.adjusted_close, 2) as adjusted_close_latest,
                                round(allocation.investment_amount / selected_dates.adjusted_close, 4) as shares_purchased,
                                round((allocation.investment_amount / selected_dates.adjusted_close) * (price_latest.adjusted_close - selected_dates.adjusted_close), 2) as gain_by_trade
                            from selected_dates
                            left join price_latest on selected_dates.company_stock_symbol = price_latest.company_stock_symbol
                            left join allocation on selected_dates.company_stock_symbol = allocation.company_stock_symbol
                        )
                        select *
                        from strategy_output
                        order by date_value asc, company_stock_symbol asc
                    """
                else:
                    query = f"""
                        with allocation as (
                            select *
                            from values
                            {allocation_values}
                            as allocation(company_stock_symbol, allocation_pct, investment_amount)
                        )
                        ,selected_dates as (
                            select
                                dd.date_value,
                                dc.company_stock_symbol,
                                fa.adj_close as adjusted_close
                            from operations.finance.fact_price_daily fa
                            left join operations.finance.dim_date dd on dd.date_key = fa.date_key
                            left join operations.finance.dim_company dc on dc.company_bigint_key = fa.company_bigint_key
                            where dc.company_stock_symbol in ({stocks_selected_list})
                            and dd.date_value >= date_add(current_date(), -{window_days})
                            and {schedule_sql}
                        )
                        ,price_latest as (
                            select company_stock_symbol, adjusted_close
                            from (
                                select
                                    dc.company_stock_symbol,
                                    fa.adj_close as adjusted_close,
                                    row_number() over (
                                        partition by dc.company_stock_symbol
                                        order by dd.date_value desc
                                    ) as rn
                                from operations.finance.fact_price_daily fa
                                left join operations.finance.dim_date dd on dd.date_key = fa.date_key
                                left join operations.finance.dim_company dc on dc.company_bigint_key = fa.company_bigint_key
                                where dc.company_stock_symbol in ({stocks_selected_list})
                            )
                            where rn = 1
                        )
                        ,strategy_output as (
                            select
                                selected_dates.date_value,
                                selected_dates.company_stock_symbol,
                                allocation.allocation_pct,
                                allocation.investment_amount,
                                round(selected_dates.adjusted_close, 2) as adjusted_close,
                                round(price_latest.adjusted_close, 2) as adjusted_close_latest,
                                round(allocation.investment_amount / selected_dates.adjusted_close, 4) as shares_purchased,
                                round((allocation.investment_amount / selected_dates.adjusted_close) * (price_latest.adjusted_close - selected_dates.adjusted_close), 2) as gain_by_trade
                            from selected_dates
                            left join price_latest on selected_dates.company_stock_symbol = price_latest.company_stock_symbol
                            left join allocation on selected_dates.company_stock_symbol = allocation.company_stock_symbol
                        )
                        {final_select_sql}
                    """

                dca_strategy_output = sql_query(query)

                st.data_editor(dca_strategy_output, column_config={
                    "date_value": "Date",
                    "company_stock_symbol": "Stock",
                    "adjusted_close": "Price",
                    "adjusted_close_latest": "Price Today",
                    "gain_by_trade": "Gain"
                })


    if strategy == "Mean Reversion":

        #stocks_selected_list = ", ".join(f"'{t}'" for t in stocks_selected)

        single_stock = st.selectbox(label="Stock...", options=stocks_selected, key='mean_reversion_stock')

        if allocation_df is not None and "Moving Average" in allocation_df.columns and "Threshold %" in allocation_df.columns:
            selected_row = allocation_df[allocation_df["Stock"] == single_stock].iloc[0]
            quick_ma = int(selected_row["Moving Average"])
            quick_threshold = selected_row["Threshold %"]
        else:
            quick_ma = moving_average
            quick_threshold = threshold

        mean_reversion(stock=single_stock, ma=quick_ma, threshold=quick_threshold)
        
    if st.button("Update Session" if edit_session_id else "Create Session", type='primary',use_container_width=True):
        if not session_name:
            st.error("Please enter a session name")
            return

        if edit_session_id:
            from ui.session_manager import update_session
            update_session(
                session_id=edit_session_id,
                session_name=session_name,
                asset_type=asset_type,
                strategy=strategy,
                investment_amount=investment_amount,
                allocation_df=allocation_df,
                frequency=frequency if strategy == 'Dollar Cost Average' else None,
                day_of_week=day_of_week if strategy == 'Dollar Cost Average' else None,
                moving_average=moving_average if strategy == 'Mean Reversion' else None,
                threshold=threshold if strategy == 'Mean Reversion' else None,
            )
            st.session_state.pop("editing_session_id", None)
            st.success(f"Session '{session_name}' updated")
            st.rerun()
        else:
            if strategy == 'Dollar Cost Average':
                create_session(
                    session_name=session_name,
                    asset_type=asset_type,
                    strategy=strategy,
                    investment_amount=investment_amount,
                    allocation_df=allocation_df,
                    frequency=frequency,
                    day_of_week=day_of_week
                )
                st.success(f"Session '{session_name}' created")
                st.rerun()

            elif strategy == "Mean Reversion":
                create_session(
                    session_name=session_name,
                    asset_type=asset_type,
                    strategy=strategy,
                    investment_amount=investment_amount,
                    allocation_df=allocation_df,
                    moving_average=moving_average,
                    threshold=threshold
                )
                st.success(f"Session '{session_name}' created")
                st.rerun()

class CreateSession:
    def __init__(self):


        # Load Google Material Symbols
        st.markdown(
            """
            <link
                href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded"
                rel="stylesheet"
            >
            """,
            unsafe_allow_html=True,
        )


        # Create three columns and use the middle one
        left, center, right = st.columns([1, 2, 1])

        with center:

            # Large Material Icon
            st.markdown(
                """
                <div style="text-align: center;">
                    <span
                        class="material-symbols-rounded"
                        style="
                            font-size: 120px;
                            line-height: 1;
                        "
                    >
                        finance_mode
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div style="text-align: center;">
                    <h1>Welcome</h1>
                    <p>Create a session to get started.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Center the button
            button_left, button_center, button_right = st.columns([1, 1, 1])

            with button_center:
                if st.button("Create Session",use_container_width=True,):
                    create_session_dialog()