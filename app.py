"""
==========================================================
APL Logistics Dashboard
Delivery Performance, Delay Risk and Logistics Efficiency
==========================================================
"""

import streamlit as st
import pandas as pd

# Local Modules
from config import configure_page
from analysis import preprocess_dataset, calculate_kpis
from utils import (
    load_css,
    sidebar_filters,
    filter_dataframe,
    metric_card,
    dashboard_footer
)

from charts import (
    delivery_performance_chart,
    delivery_gap_histogram,
    late_delivery_risk_chart,
    delivery_status_chart,
    shipping_mode_chart,
    shipping_delay_chart,
    shipping_sales_chart,
    shipping_profit_chart
)

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

configure_page()

# ==========================================================
# LOAD CSS
# ==========================================================

load_css("assets/style.css")

# ==========================================================
# DASHBOARD TITLE
# ==========================================================

st.markdown(
    """
    <div class='dashboard-title'>
        🚚 Delivery Performance Dashboard
    </div>

    <div class='dashboard-subtitle'>
        Delay Risk & Logistics Efficiency Analysis
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# LOAD DATA
# ==========================================================

DATA_PATH = "data/APL_Logistics.csv"

try:

    df = preprocess_dataset(DATA_PATH)

except Exception as e:

    st.error(f"Error Loading Dataset : {e}")

    st.stop()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.image(
    "https://img.icons8.com/color/96/truck.png",
    width=90
)

st.sidebar.title("Dashboard Filters")

shipping_mode, region, market, customer_segment = sidebar_filters(df)

filtered_df = filter_dataframe(

    df,

    shipping_mode,

    region,

    market,

    customer_segment

)

# ==========================================================
# KPI SECTION
# ==========================================================

kpis = calculate_kpis(filtered_df)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:

    metric_card(

        "Total Orders",

        f"{kpis['Total Orders']:,}"

    )

with col2:

    metric_card(

        "On-Time Delivery",

        f"{kpis['On-Time Delivery %']}%"

    )

with col3:

    metric_card(

        "Delayed Delivery",

        f"{kpis['Delayed Delivery %']}%"

    )

with col4:

    metric_card(

        "Average Delay",

        f"{kpis['Average Delay']} Days"

    )

st.markdown("")

col5, col6, col7, col8 = st.columns(4)

with col5:

    metric_card(

        "Late Delivery Risk",

        f"{kpis['Late Delivery Risk %']}%"

    )

with col6:

    metric_card(

        "Average Sales",

        f"${kpis['Average Sales']:,.2f}"

    )

with col7:

    metric_card(

        "Average Profit",

        f"${kpis['Average Profit']:,.2f}"

    )

with col8:

    metric_card(
    "Records",
    f"{len(filtered_df):,}"
)
st.markdown("---")

# ==========================================================
# OVERVIEW
# ==========================================================

st.header("📊 Delivery Performance Overview")

left, right = st.columns(2)

with left:

    st.plotly_chart(

        delivery_performance_chart(filtered_df),

        use_container_width=True

    )

with right:

    st.plotly_chart(

        delivery_gap_histogram(filtered_df),

        use_container_width=True

    )

st.markdown("---")
# ==========================================================
# DELAY RISK ANALYSIS
# ==========================================================

st.header("⚠️ Delay Risk Analysis")

col1, col2 = st.columns(2)

with col1:

    st.plotly_chart(
        late_delivery_risk_chart(filtered_df),
        use_container_width=True
    )

with col2:

    st.plotly_chart(
        delivery_status_chart(filtered_df),
        use_container_width=True
    )

st.markdown("---")


# ==========================================================
# SHIPPING MODE ANALYSIS
# ==========================================================

st.header("🚚 Shipping Mode Analysis")

col1, col2 = st.columns(2)

with col1:

    st.plotly_chart(
        shipping_mode_chart(filtered_df),
        use_container_width=True
    )

with col2:

    st.plotly_chart(
        shipping_delay_chart(filtered_df),
        use_container_width=True
    )

st.markdown("")

col3, col4 = st.columns(2)

with col3:

    st.plotly_chart(
        shipping_sales_chart(filtered_df),
        use_container_width=True
    )

with col4:

    st.plotly_chart(
        shipping_profit_chart(filtered_df),
        use_container_width=True
    )

st.markdown("---")


# ==========================================================
# IMPORT REMAINING CHART FUNCTIONS
# ==========================================================

from charts import (

    regional_delay_chart,

    market_delay_chart,

    customer_segment_chart,

    sales_vs_delay,

    profit_vs_delay,

    region_market_heatmap,

    country_delay_chart,

    delivery_gap_boxplot,

    sales_distribution,

    profit_distribution,

    on_time_gauge

)


# ==========================================================
# REGIONAL ANALYSIS
# ==========================================================

st.header("🌍 Regional Logistics Analysis")

col1, col2 = st.columns(2)

with col1:

    st.plotly_chart(
        regional_delay_chart(filtered_df),
        use_container_width=True
    )

with col2:

    st.plotly_chart(
        country_delay_chart(filtered_df),
        use_container_width=True
    )

st.markdown("---")


# ==========================================================
# MARKET ANALYSIS
# ==========================================================

st.header("🌐 Market Analysis")

col1, col2 = st.columns(2)

with col1:

    st.plotly_chart(
        market_delay_chart(filtered_df),
        use_container_width=True
    )

with col2:

    st.plotly_chart(
        region_market_heatmap(filtered_df),
        use_container_width=True
    )

st.markdown("---")


# ==========================================================
# CUSTOMER SEGMENT ANALYSIS
# ==========================================================

st.header("👥 Customer Segment Analysis")

st.plotly_chart(

    customer_segment_chart(filtered_df),

    use_container_width=True

)

st.markdown("---")


# ==========================================================
# SALES & PROFIT ANALYSIS
# ==========================================================

st.header("💰 Sales and Profit Analysis")

col1, col2 = st.columns(2)

with col1:

    st.plotly_chart(
        sales_vs_delay(filtered_df),
        use_container_width=True
    )

with col2:

    st.plotly_chart(
        profit_vs_delay(filtered_df),
        use_container_width=True
    )

st.markdown("")

col3, col4 = st.columns(2)

with col3:

    st.plotly_chart(
        sales_distribution(filtered_df),
        use_container_width=True
    )

with col4:

    st.plotly_chart(
        profit_distribution(filtered_df),
        use_container_width=True
    )

st.markdown("---")


# ==========================================================
# DELIVERY GAP ANALYSIS
# ==========================================================

st.header("📦 Delivery Gap Analysis")

col1, col2 = st.columns(2)

with col1:

    st.plotly_chart(
        delivery_gap_boxplot(filtered_df),
        use_container_width=True
    )

with col2:

    st.plotly_chart(
        on_time_gauge(
            kpis["On-Time Delivery %"]
        ),
        use_container_width=True
    )

st.markdown("---")
# ==========================================================
# DATA PREVIEW
# ==========================================================

st.header("📄 Dataset Preview")

st.dataframe(

    filtered_df,

    use_container_width=True,

    height=400

)

st.markdown("---")


# ==========================================================
# SUMMARY TABLES
# ==========================================================

st.header("📊 Summary Tables")

tab1, tab2, tab3, tab4 = st.tabs(

    [

        "Shipping",

        "Region",

        "Market",

        "Customer"

    ]

)

with tab1:

    shipping_summary = (

        filtered_df

        .groupby("Shipping Mode")

        .agg(

            Orders=("Shipping Mode", "count"),

            Average_Delay=("Delivery Gap", "mean"),

            Average_Sales=("Sales", "mean"),

            Average_Profit=("Order Profit Per Order", "mean")

        )

        .round(2)

    )

    st.dataframe(

        shipping_summary,

        use_container_width=True

    )


with tab2:

    regional_summary = (

        filtered_df

        .groupby("Order Region")

        .agg(

            Orders=("Order Region", "count"),

            Average_Delay=("Delivery Gap", "mean"),

            Sales=("Sales", "sum"),

            Profit=("Order Profit Per Order", "sum")

        )

        .round(2)

    )

    st.dataframe(

        regional_summary,

        use_container_width=True

    )


with tab3:

    market_summary = (

        filtered_df

        .groupby("Market")

        .agg(

            Orders=("Market", "count"),

            Average_Delay=("Delivery Gap", "mean"),

            Sales=("Sales", "sum"),

            Profit=("Order Profit Per Order", "sum")

        )

        .round(2)

    )

    st.dataframe(

        market_summary,

        use_container_width=True

    )


with tab4:

    customer_summary = (

        filtered_df

        .groupby("Customer Segment")

        .agg(

            Orders=("Customer Segment", "count"),

            Average_Delay=("Delivery Gap", "mean"),

            Sales=("Sales", "sum"),

            Profit=("Order Profit Per Order", "sum")

        )

        .round(2)

    )

    st.dataframe(

        customer_summary,

        use_container_width=True

    )


st.markdown("---")


# ==========================================================
# DOWNLOAD SECTION
# ==========================================================

st.header("📥 Download Processed Dataset")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(

    label="⬇ Download Cleaned Dataset",

    data=csv,

    file_name="APL_Logistics_Cleaned_Data.csv",

    mime="text/csv"

)


st.markdown("---")


# ==========================================================
# PROJECT INFORMATION
# ==========================================================

with st.expander("📘 Project Information"):

    st.markdown("""

### Project Title

**Delivery Performance, Delay Risk, and Logistics Efficiency Analysis in Global Supply Chain Operations**

### Organization

APL Logistics (KWE Group)

### Objectives

- Analyze delivery performance.
- Identify late delivery risk.
- Compare shipping modes.
- Evaluate regional logistics performance.
- Monitor SLA compliance.
- Generate operational KPIs.

### Technologies

- Python
- Streamlit
- Pandas
- Plotly
- NumPy

""")


# ==========================================================
# FOOTER
# ==========================================================

dashboard_footer()