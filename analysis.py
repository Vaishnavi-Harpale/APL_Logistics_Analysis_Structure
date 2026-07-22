"""
==========================================================
APL Logistics Data Analysis Module
Delivery Performance, Delay Risk, and Logistics Efficiency
==========================================================
"""

import os
import warnings
import pandas as pd
import numpy as np

warnings.filterwarnings("ignore")


# ==========================================================
# Load Dataset
# ==========================================================

def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load CSV dataset.

    Parameters
    ----------
    file_path : str
        Path to CSV file

    Returns
    -------
    pandas.DataFrame
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found : {file_path}")

    df = pd.read_csv(file_path, encoding="latin1")

    return df


# ==========================================================
# Validate Required Columns
# ==========================================================

def validate_columns(df: pd.DataFrame):
    """
    Validate required columns.
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
        "Benefit per order",
        "Order Profit Per Order"

    ]

    missing = []

    for col in required_columns:

        if col not in df.columns:

            missing.append(col)

    if len(missing) > 0:

        raise ValueError(
            f"Dataset is missing columns:\n{missing}"
        )

    return True


# ==========================================================
# Initial Cleaning
# ==========================================================

def clean_dataset(df: pd.DataFrame):

    """
    Clean logistics dataset.
    """

    df = df.copy()

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Remove rows with missing shipping values
    df.dropna(
        subset=[
            "Days for shipping (real)",
            "Days for shipment (scheduled)"
        ],
        inplace=True
    )

    # Remove negative shipping duration
    df = df[
        (df["Days for shipping (real)"] >= 0)
        &
        (df["Days for shipment (scheduled)"] >= 0)
    ]

    # Fill categorical missing values
    categorical_columns = [

        "Shipping Mode",
        "Delivery Status",
        "Order Region",
        "Order Country",
        "Market",
        "Customer Segment"

    ]

    for col in categorical_columns:

        if col in df.columns:

            df[col] = df[col].fillna("Unknown")

    # Fill numeric values

    numeric_columns = [

        "Sales",
        "Benefit per order",
        "Order Profit Per Order"

    ]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = df[col].fillna(
                df[col].median()
            )

    return df.reset_index(drop=True)


# ==========================================================
# Standardize Text
# ==========================================================

def standardize_text(df):

    """
    Standardize text columns.
    """

    columns = [

        "Shipping Mode",
        "Order Region",
        "Order Country",
        "Market",
        "Customer Segment",
        "Delivery Status"

    ]

    for col in columns:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.title()
            )

    return df


# ==========================================================
# Delivery Gap
# ==========================================================

def calculate_delivery_gap(df):

    """
    Calculate delay gap.
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
    Classify shipment.
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
# Dataset Summary
# ==========================================================

def dataset_summary(df):

    """
    Basic dataset summary.
    """

    summary = {

        "Total Records": len(df),

        "Total Columns": len(df.columns),

        "Duplicate Rows": df.duplicated().sum(),

        "Missing Values": int(df.isnull().sum().sum()),

        "Total Sales": round(df["Sales"].sum(), 2),

        "Average Sales": round(df["Sales"].mean(), 2),

        "Average Profit":
        round(
            df["Order Profit Per Order"].mean(),
            2
        ),

        "Average Benefit":
        round(
            df["Benefit per order"].mean(),
            2
        )

    }

    return summary


# ==========================================================
# Complete Preprocessing Pipeline
# ==========================================================

def preprocess_dataset(file_path):

    """
    Execute preprocessing pipeline.
    """

    df = load_dataset(file_path)

    validate_columns(df)

    df = clean_dataset(df)

    df = standardize_text(df)

    df = calculate_delivery_gap(df)

    df = classify_delivery(df)

    return df
# ==========================================================
# KPI CALCULATIONS
# ==========================================================

def calculate_kpis(df):
    """
    Calculate dashboard KPIs.
    """

    total_orders = len(df)

    on_time_orders = len(
        df[df["Delivery Performance"] == "On-Time"]
    )

    delayed_orders = len(
        df[df["Delivery Performance"] == "Delayed"]
    )

    early_orders = len(
        df[df["Delivery Performance"] == "Early"]
    )

    on_time_rate = (
        on_time_orders / total_orders * 100
        if total_orders > 0 else 0
    )

    delayed_rate = (
        delayed_orders / total_orders * 100
        if total_orders > 0 else 0
    )

    early_rate = (
        early_orders / total_orders * 100
        if total_orders > 0 else 0
    )

    average_delay = round(
        df["Delivery Gap"].mean(),
        2
    )

    late_delivery_risk = round(
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

    average_benefit = round(
        df["Benefit per order"].mean(),
        2
    )

    return {

        "Total Orders": total_orders,

        "On-Time Delivery %": round(on_time_rate, 2),

        "Delayed Delivery %": round(delayed_rate, 2),

        "Early Delivery %": round(early_rate, 2),

        "Average Delay": average_delay,

        "Late Delivery Risk %": late_delivery_risk,

        "Average Sales": average_sales,

        "Average Profit": average_profit,

        "Average Benefit": average_benefit

    }


# ==========================================================
# DELIVERY PERFORMANCE SUMMARY
# ==========================================================

def delivery_performance_summary(df):

    summary = (

        df.groupby("Delivery Performance")

        .size()

        .reset_index(name="Orders")

    )

    summary["Percentage"] = round(

        summary["Orders"]

        /

        summary["Orders"].sum()

        * 100,

        2

    )

    return summary


# ==========================================================
# SHIPPING MODE ANALYSIS
# ==========================================================

def shipping_mode_analysis(df):

    summary = (

        df.groupby("Shipping Mode")

        .agg(

            Total_Orders=("Shipping Mode", "count"),

            Average_Delay=("Delivery Gap", "mean"),

            Average_Sales=("Sales", "mean"),

            Average_Profit=("Order Profit Per Order", "mean"),

            Late_Delivery_Risk=("Late_delivery_risk", "mean")

        )

        .reset_index()

    )

    summary["Average_Delay"] = summary["Average_Delay"].round(2)

    summary["Average_Sales"] = summary["Average_Sales"].round(2)

    summary["Average_Profit"] = summary["Average_Profit"].round(2)

    summary["Late_Delivery_Risk"] = (
        summary["Late_Delivery_Risk"] * 100
    ).round(2)

    return summary


# ==========================================================
# REGIONAL ANALYSIS
# ==========================================================

def regional_analysis(df):

    summary = (

        df.groupby("Order Region")

        .agg(

            Orders=("Order Region", "count"),

            Average_Delay=("Delivery Gap", "mean"),

            Sales=("Sales", "sum"),

            Profit=("Order Profit Per Order", "sum"),

            Late_Risk=("Late_delivery_risk", "mean")

        )

        .reset_index()

    )

    summary["Average_Delay"] = summary["Average_Delay"].round(2)

    summary["Late_Risk"] = (
        summary["Late_Risk"] * 100
    ).round(2)

    return summary


# ==========================================================
# MARKET ANALYSIS
# ==========================================================

def market_analysis(df):

    summary = (

        df.groupby("Market")

        .agg(

            Orders=("Market", "count"),

            Average_Delay=("Delivery Gap", "mean"),

            Sales=("Sales", "sum"),

            Profit=("Order Profit Per Order", "sum"),

            Late_Risk=("Late_delivery_risk", "mean")

        )

        .reset_index()

    )

    summary["Average_Delay"] = summary["Average_Delay"].round(2)

    summary["Late_Risk"] = (
        summary["Late_Risk"] * 100
    ).round(2)

    return summary


# ==========================================================
# CUSTOMER SEGMENT ANALYSIS
# ==========================================================

def customer_segment_analysis(df):

    summary = (

        df.groupby("Customer Segment")

        .agg(

            Orders=("Customer Segment", "count"),

            Average_Delay=("Delivery Gap", "mean"),

            Sales=("Sales", "sum"),

            Profit=("Order Profit Per Order", "sum"),

            Late_Risk=("Late_delivery_risk", "mean")

        )

        .reset_index()

    )

    summary["Average_Delay"] = summary["Average_Delay"].round(2)

    summary["Late_Risk"] = (
        summary["Late_Risk"] * 100
    ).round(2)

    return summary


# ==========================================================
# EXPORT REPORTS
# ==========================================================

def export_reports(df, output_folder="outputs"):

    import os

    os.makedirs(output_folder, exist_ok=True)

    df.to_csv(
        os.path.join(output_folder, "cleaned_data.csv"),
        index=False
    )

    delivery_performance_summary(df).to_csv(
        os.path.join(output_folder, "delivery_summary.csv"),
        index=False
    )

    shipping_mode_analysis(df).to_csv(
        os.path.join(output_folder, "shipping_mode_summary.csv"),
        index=False
    )

    regional_analysis(df).to_csv(
        os.path.join(output_folder, "regional_summary.csv"),
        index=False
    )

    market_analysis(df).to_csv(
        os.path.join(output_folder, "market_summary.csv"),
        index=False
    )

    customer_segment_analysis(df).to_csv(
        os.path.join(output_folder, "customer_segment_summary.csv"),
        index=False
    )


# ==========================================================
# COMPLETE ANALYSIS PIPELINE
# ==========================================================

def run_analysis(file_path):

    df = preprocess_dataset(file_path)

    kpis = calculate_kpis(df)

    export_reports(df)

    return {

        "data": df,

        "kpis": kpis,

        "delivery_summary": delivery_performance_summary(df),

        "shipping_summary": shipping_mode_analysis(df),

        "regional_summary": regional_analysis(df),

        "market_summary": market_analysis(df),

        "customer_summary": customer_segment_analysis(df)

    }