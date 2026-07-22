"""
==========================================================
APL Logistics Dashboard
Utility Functions (Part 1)
==========================================================
"""

import os
import pandas as pd
import numpy as np
import streamlit as st


# ==========================================================
# Load Dataset
# ==========================================================

@st.cache_data
def load_data(file_path):
    """
    Load logistics dataset.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"File not found : {file_path}"
        )

    df = pd.read_csv(file_path, encoding="latin1")

    return df


# ==========================================================
# Validate Dataset
# ==========================================================

def validate_dataset(df):
    """
    Validate required dataset columns.
    """

    required_columns = [

        "Days for shipping (real)",
        "Days for shipment (scheduled)",
        "Late_delivery_risk",
        "Delivery Status",
        "Shipping Mode",
        "Order Region",
        "Order Country",
        "Market",
        "Customer Segment",
        "Sales",
        "Order Profit Per Order",
        "Benefit per order"

    ]

    missing_columns = []

    for column in required_columns:

        if column not in df.columns:

            missing_columns.append(column)

    if len(missing_columns) > 0:

        raise ValueError(

            f"Missing Columns : {missing_columns}"

        )

    return True


# ==========================================================
# Clean Dataset
# ==========================================================

def clean_data(df):
    """
    Clean logistics dataset.
    """

    df = df.copy()

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Remove missing shipping values
    df.dropna(

        subset=[

            "Days for shipping (real)",

            "Days for shipment (scheduled)"

        ],

        inplace=True

    )

    # Remove invalid values
    df = df[

        (df["Days for shipping (real)"] >= 0)

        &

        (df["Days for shipment (scheduled)"] >= 0)

    ]

    # Fill categorical values
    categorical_columns = [

        "Shipping Mode",

        "Delivery Status",

        "Order Region",

        "Order Country",

        "Market",

        "Customer Segment"

    ]

    for column in categorical_columns:

        df[column] = (

            df[column]

            .fillna("Unknown")

            .astype(str)

            .str.strip()

            .str.title()

        )

    # Fill numeric values

    numeric_columns = [

        "Sales",

        "Order Profit Per Order",

        "Benefit per order"

    ]

    for column in numeric_columns:

        df[column] = df[column].fillna(

            df[column].median()

        )

    return df.reset_index(drop=True)


# ==========================================================
# Delivery Gap
# ==========================================================

def calculate_delivery_gap(df):
    """
    Calculate delivery delay gap.
    """

    df = df.copy()

    df["Delivery Gap"] = (

        df["Days for shipping (real)"]

        -

        df["Days for shipment (scheduled)"]

    )

    return df


# ==========================================================
# Delivery Classification
# ==========================================================

def classify_delivery(df):
    """
    Classify deliveries.
    """

    conditions = [

        df["Delivery Gap"] < 0,

        df["Delivery Gap"] == 0,

        df["Delivery Gap"] > 0

    ]

    labels = [

        "Early",

        "On-Time",

        "Delayed"

    ]

    df["Delivery Performance"] = np.select(

        conditions,

        labels,

        default="Unknown"

    )

    return df


# ==========================================================
# Dataset Information
# ==========================================================

def dataset_information(df):
    """
    Dataset summary.
    """

    info = {

        "Rows": len(df),

        "Columns": len(df.columns),

        "Missing Values":

            int(df.isnull().sum().sum()),

        "Duplicate Rows":

            int(df.duplicated().sum())

    }

    return info


# ==========================================================
# Numeric Summary
# ==========================================================

def numeric_summary(df):
    """
    Numeric statistics.
    """

    numeric_df = df.select_dtypes(

        include=["int64", "float64"]

    )

    return numeric_df.describe().round(2)


# ==========================================================
# Unique Values
# ==========================================================

def unique_values(df):
    """
    Count unique values.
    """

    unique_dict = {}

    for column in df.columns:

        unique_dict[column] = df[column].nunique()

    return pd.DataFrame(

        unique_dict.items(),

        columns=["Column", "Unique Values"]

    )


# ==========================================================
# Missing Values
# ==========================================================

def missing_value_summary(df):
    """
    Missing values summary.
    """

    summary = pd.DataFrame({

        "Column": df.columns,

        "Missing Values": df.isnull().sum().values,

        "Percentage": round(

            df.isnull().mean().values * 100,

            2

        )

    })

    return summary.sort_values(

        "Missing Values",

        ascending=False

    )
# ==========================================================
# KPI CALCULATOR
# ==========================================================

def calculate_kpis(df):
    """
    Calculate dashboard KPIs.
    """

    total_orders = len(df)

    on_time = len(
        df[df["Delivery Performance"] == "On-Time"]
    )

    delayed = len(
        df[df["Delivery Performance"] == "Delayed"]
    )

    early = len(
        df[df["Delivery Performance"] == "Early"]
    )

    average_delay = round(
        df["Delivery Gap"].mean(),
        2
    )

    late_risk = round(
        df["Late_delivery_risk"].mean() * 100,
        2
    )

    average_sales = round(
        df["Sales"].mean(),
        2
    )

    average_profit = round(
        df["Order Profit Per Order"].mean(),
        2
    )

    return {

        "Total Orders": total_orders,

        "On-Time Delivery %": round(
            (on_time / total_orders) * 100,
            2
        ),

        "Delayed Delivery %": round(
            (delayed / total_orders) * 100,
            2
        ),

        "Early Delivery %": round(
            (early / total_orders) * 100,
            2
        ),

        "Average Delay": average_delay,

        "Late Delivery Risk %": late_risk,

        "Average Sales": average_sales,

        "Average Profit": average_profit

    }


# ==========================================================
# FORMAT FUNCTIONS
# ==========================================================

def format_currency(value):
    """
    Convert number into currency.
    """

    return f"${value:,.2f}"


def format_percentage(value):
    """
    Percentage formatting.
    """

    return f"{value:.2f} %"


def format_number(value):
    """
    Integer formatting.
    """

    return f"{int(value):,}"


# ==========================================================
# FILTER FUNCTIONS
# ==========================================================

def filter_dataframe(
    df,
    shipping_mode=None,
    region=None,
    market=None,
    customer_segment=None
):
    """
    Apply dashboard filters.
    """

    filtered_df = df.copy()

    if shipping_mode and shipping_mode != "All":
        filtered_df = filtered_df[
            filtered_df["Shipping Mode"] == shipping_mode
        ]

    if region and region != "All":
        filtered_df = filtered_df[
            filtered_df["Order Region"] == region
        ]

    if market and market != "All":
        filtered_df = filtered_df[
            filtered_df["Market"] == market
        ]

    if customer_segment and customer_segment != "All":
        filtered_df = filtered_df[
            filtered_df["Customer Segment"] == customer_segment
        ]

    return filtered_df.reset_index(drop=True)


# ==========================================================
# SHIPPING MODE HELPERS
# ==========================================================

def best_shipping_mode(df):
    """
    Best shipping mode based on lowest delay.
    """

    summary = (

        df.groupby("Shipping Mode")

        ["Delivery Gap"]

        .mean()

        .sort_values()

    )

    return summary.index[0]


def worst_shipping_mode(df):
    """
    Worst shipping mode based on highest delay.
    """

    summary = (

        df.groupby("Shipping Mode")

        ["Delivery Gap"]

        .mean()

        .sort_values()

    )

    return summary.index[-1]


# ==========================================================
# REGION HELPERS
# ==========================================================

def highest_delay_region(df):
    """
    Region with highest average delay.
    """

    summary = (

        df.groupby("Order Region")

        ["Delivery Gap"]

        .mean()

        .sort_values()

    )

    return summary.index[-1]


# ==========================================================
# EXPORT CSV
# ==========================================================

def export_csv(df, file_name):
    """
    Export dataframe as CSV.
    """

    df.to_csv(
        file_name,
        index=False
    )


# ==========================================================
# DOWNLOAD BUTTON
# ==========================================================

def download_button(df, file_name):
    """
    Streamlit download button.
    """

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(

        label="📥 Download CSV",

        data=csv,

        file_name=file_name,

        mime="text/csv"

    )


# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

def sidebar_filters(df):
    """
    Create Streamlit sidebar filters.
    """

    shipping_mode = st.sidebar.selectbox(

        "Shipping Mode",

        ["All"] +
        sorted(
            df["Shipping Mode"].unique().tolist()
        )

    )

    region = st.sidebar.selectbox(

        "Order Region",

        ["All"] +
        sorted(
            df["Order Region"].unique().tolist()
        )

    )

    market = st.sidebar.selectbox(

        "Market",

        ["All"] +
        sorted(
            df["Market"].unique().tolist()
        )

    )

    customer_segment = st.sidebar.selectbox(

        "Customer Segment",

        ["All"] +
        sorted(
            df["Customer Segment"].unique().tolist()
        )

    )

    return (

        shipping_mode,

        region,

        market,

        customer_segment

    )


# ==========================================================
# METRIC CARD
# ==========================================================

def metric_card(title, value):

    st.markdown(

        f"""
        <div class="kpi-card">

        <div class="kpi-title">

        {title}

        </div>

        <div class="kpi-value">

        {value}

        </div>

        </div>
        """,

        unsafe_allow_html=True

    )


# ==========================================================
# LOAD CSS
# ==========================================================

def load_css(file_path):

    with open(file_path) as css:

        st.markdown(

            f"<style>{css.read()}</style>",

            unsafe_allow_html=True

        )


# ==========================================================
# FOOTER
# ==========================================================

def dashboard_footer():

    st.markdown(

        """
        <hr>

        <center>

        <b>

        Delivery Performance, Delay Risk and Logistics
        Efficiency Analysis

        </b>

        <br>

        APL Logistics (KWE Group)

        </center>

        """,

        unsafe_allow_html=True

    )