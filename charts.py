"""
==========================================================
APL Logistics Dashboard
Charts Module (Part 1)
==========================================================
"""

import plotly.express as px
import plotly.graph_objects as go


# ==========================================================
# Dashboard Color Theme
# ==========================================================

PRIMARY = "#2563EB"
SUCCESS = "#16A34A"
WARNING = "#F59E0B"
DANGER = "#DC2626"
BACKGROUND = "#FFFFFF"


# ==========================================================
# Common Layout
# ==========================================================

def apply_layout(fig, title):

    fig.update_layout(
        title=title,
        title_x=0.5,
        template="plotly_white",
        height=500,
        paper_bgcolor=BACKGROUND,
        plot_bgcolor=BACKGROUND,
        font=dict(
            family="Poppins",
            size=14
        ),
        margin=dict(
            l=30,
            r=30,
            t=70,
            b=30
        )
    )

    return fig


# ==========================================================
# Delivery Performance Pie Chart
# ==========================================================

def delivery_performance_chart(df):

    summary = (

        df["Delivery Performance"]

        .value_counts()

        .reset_index()

    )

    summary.columns = [

        "Status",

        "Orders"

    ]

    fig = px.pie(

        summary,

        names="Status",

        values="Orders",

        hole=0.45,

        color="Status",

        color_discrete_map={

            "On-Time": SUCCESS,

            "Delayed": DANGER,

            "Early": PRIMARY

        }

    )

    fig.update_traces(
        textinfo="percent+label"
    )

    return apply_layout(
        fig,
        "Delivery Performance"
    )


# ==========================================================
# Delivery Gap Histogram
# ==========================================================

def delivery_gap_histogram(df):

    fig = px.histogram(

        df,

        x="Delivery Gap",

        nbins=30,

        title="Delivery Gap Distribution"

    )

    fig.update_traces(
        marker_color=PRIMARY
    )

    return apply_layout(
        fig,
        "Delivery Gap Distribution"
    )


# ==========================================================
# Late Delivery Risk
# ==========================================================

def late_delivery_risk_chart(df):

    summary = (

        df["Late_delivery_risk"]

        .value_counts()

        .reset_index()

    )

    summary.columns = [

        "Risk",

        "Orders"

    ]

    summary["Risk"] = summary["Risk"].replace(

        {

            0: "No Risk",

            1: "Late Delivery"

        }

    )

    fig = px.bar(

        summary,

        x="Risk",

        y="Orders",

        color="Risk",

        text="Orders",

        color_discrete_map={

            "No Risk": SUCCESS,

            "Late Delivery": DANGER

        }

    )

    fig.update_traces(

        textposition="outside"

    )

    return apply_layout(

        fig,

        "Late Delivery Risk"

    )


# ==========================================================
# Delivery Status Chart
# ==========================================================

def delivery_status_chart(df):

    summary = (

        df["Delivery Status"]

        .value_counts()

        .reset_index()

    )

    summary.columns = [

        "Status",

        "Orders"

    ]

    fig = px.bar(

        summary,

        x="Status",

        y="Orders",

        color="Status",

        text="Orders"

    )

    fig.update_traces(

        textposition="outside"

    )

    return apply_layout(

        fig,

        "Delivery Status"

    )


# ==========================================================
# Shipping Mode Performance
# ==========================================================

def shipping_mode_chart(df):

    summary = (

        df.groupby("Shipping Mode")

        .agg(

            Orders=("Shipping Mode", "count"),

            Average_Delay=("Delivery Gap", "mean")

        )

        .reset_index()

    )

    fig = px.bar(

        summary,

        x="Shipping Mode",

        y="Orders",

        color="Average_Delay",

        text="Orders",

        color_continuous_scale="Blues"

    )

    fig.update_traces(

        textposition="outside"

    )

    return apply_layout(

        fig,

        "Shipping Mode Performance"

    )


# ==========================================================
# Shipping Delay Comparison
# ==========================================================

def shipping_delay_chart(df):

    summary = (

        df.groupby("Shipping Mode")

        ["Delivery Gap"]

        .mean()

        .reset_index()

    )

    fig = px.bar(

        summary,

        x="Shipping Mode",

        y="Delivery Gap",

        color="Delivery Gap",

        text="Delivery Gap",

        color_continuous_scale="RdYlGn_r"

    )

    fig.update_traces(

        texttemplate="%{text:.2f}",

        textposition="outside"

    )

    return apply_layout(

        fig,

        "Average Delivery Delay by Shipping Mode"

    )


# ==========================================================
# Average Sales by Shipping Mode
# ==========================================================

def shipping_sales_chart(df):

    summary = (

        df.groupby("Shipping Mode")

        ["Sales"]

        .mean()

        .reset_index()

    )

    fig = px.bar(

        summary,

        x="Shipping Mode",

        y="Sales",

        color="Sales",

        text="Sales",

        color_continuous_scale="Greens"

    )

    fig.update_traces(

        texttemplate="%{text:.2f}",

        textposition="outside"

    )

    return apply_layout(

        fig,

        "Average Sales by Shipping Mode"

    )


# ==========================================================
# Average Profit by Shipping Mode
# ==========================================================

def shipping_profit_chart(df):

    summary = (

        df.groupby("Shipping Mode")

        ["Order Profit Per Order"]

        .mean()

        .reset_index()

    )

    fig = px.bar(

        summary,

        x="Shipping Mode",

        y="Order Profit Per Order",

        color="Order Profit Per Order",

        text="Order Profit Per Order",

        color_continuous_scale="Purples"

    )

    fig.update_traces(

        texttemplate="%{text:.2f}",

        textposition="outside"

    )

    return apply_layout(

        fig,

        "Average Profit by Shipping Mode"

    )
# ==========================================================
# Regional Analysis
# ==========================================================

def regional_delay_chart(df):

    summary = (
        df.groupby("Order Region")
        .agg(
            Average_Delay=("Delivery Gap", "mean")
        )
        .reset_index()
        .sort_values("Average_Delay", ascending=False)
    )

    fig = px.bar(
        summary,
        x="Order Region",
        y="Average_Delay",
        color="Average_Delay",
        text="Average_Delay",
        color_continuous_scale="Reds"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    return apply_layout(
        fig,
        "Regional Average Delivery Delay"
    )


# ==========================================================
# Market Analysis
# ==========================================================

def market_delay_chart(df):

    summary = (
        df.groupby("Market")
        .agg(
            Average_Delay=("Delivery Gap", "mean")
        )
        .reset_index()
        .sort_values("Average_Delay", ascending=False)
    )

    fig = px.bar(
        summary,
        x="Market",
        y="Average_Delay",
        color="Average_Delay",
        text="Average_Delay",
        color_continuous_scale="Oranges"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    return apply_layout(
        fig,
        "Market Wise Average Delay"
    )


# ==========================================================
# Customer Segment
# ==========================================================

def customer_segment_chart(df):

    summary = (
        df.groupby("Customer Segment")
        .agg(
            Average_Delay=("Delivery Gap", "mean")
        )
        .reset_index()
    )

    fig = px.bar(
        summary,
        x="Customer Segment",
        y="Average_Delay",
        color="Average_Delay",
        text="Average_Delay",
        color_continuous_scale="Teal"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    return apply_layout(
        fig,
        "Customer Segment Delay Analysis"
    )


# ==========================================================
# Sales vs Delay
# ==========================================================

def sales_vs_delay(df):

    fig = px.scatter(

        df,

        x="Delivery Gap",

        y="Sales",

        color="Shipping Mode",

        hover_data=["Order Country"],

        opacity=0.75

    )

    return apply_layout(

        fig,

        "Sales vs Delivery Delay"

    )


# ==========================================================
# Profit vs Delay
# ==========================================================

def profit_vs_delay(df):

    fig = px.scatter(

        df,

        x="Delivery Gap",

        y="Order Profit Per Order",

        color="Shipping Mode",

        hover_data=["Order Country"],

        opacity=0.75

    )

    return apply_layout(

        fig,

        "Profit vs Delivery Delay"

    )


# ==========================================================
# Delay Heatmap
# ==========================================================

def region_market_heatmap(df):

    summary = (

        df.pivot_table(

            values="Delivery Gap",

            index="Order Region",

            columns="Market",

            aggfunc="mean"

        )

    )

    fig = px.imshow(

        summary,

        text_auto=".2f",

        color_continuous_scale="RdYlGn_r",

        aspect="auto"

    )

    return apply_layout(

        fig,

        "Regional & Market Delay Heatmap"

    )


# ==========================================================
# Country Delay
# ==========================================================

def country_delay_chart(df):

    summary = (

        df.groupby("Order Country")

        .agg(

            Average_Delay=("Delivery Gap","mean")

        )

        .reset_index()

        .sort_values(

            "Average_Delay",

            ascending=False

        )

        .head(15)

    )

    fig = px.bar(

        summary,

        x="Order Country",

        y="Average_Delay",

        color="Average_Delay",

        text="Average_Delay",

        color_continuous_scale="Reds"

    )

    fig.update_traces(

        texttemplate="%{text:.2f}",

        textposition="outside"

    )

    return apply_layout(

        fig,

        "Top 15 Countries by Delivery Delay"

    )


# ==========================================================
# Delivery Gap Boxplot
# ==========================================================

def delivery_gap_boxplot(df):

    fig = px.box(

        df,

        x="Shipping Mode",

        y="Delivery Gap",

        color="Shipping Mode"

    )

    return apply_layout(

        fig,

        "Delivery Gap Distribution by Shipping Mode"

    )


# ==========================================================
# Sales Distribution
# ==========================================================

def sales_distribution(df):

    fig = px.histogram(

        df,

        x="Sales",

        nbins=40,

        color_discrete_sequence=["#2563EB"]

    )

    return apply_layout(

        fig,

        "Sales Distribution"

    )


# ==========================================================
# Profit Distribution
# ==========================================================

def profit_distribution(df):

    fig = px.histogram(

        df,

        x="Order Profit Per Order",

        nbins=40,

        color_discrete_sequence=["#16A34A"]

    )

    return apply_layout(

        fig,

        "Profit Distribution"

    )


# ==========================================================
# KPI Gauge
# ==========================================================

def on_time_gauge(on_time_percentage):

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=on_time_percentage,

            title={"text":"On-Time Delivery %"},

            gauge={

                "axis":{"range":[0,100]},

                "bar":{"color":"green"},

                "steps":[

                    {"range":[0,50],"color":"#FEE2E2"},

                    {"range":[50,80],"color":"#FEF3C7"},

                    {"range":[80,100],"color":"#DCFCE7"}

                ]

            }

        )

    )

    fig.update_layout(height=400)

    return fig