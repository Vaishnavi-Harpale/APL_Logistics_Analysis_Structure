

import streamlit as st

# --------------------------------------------------------
# Streamlit Page Configuration
# --------------------------------------------------------

PAGE_TITLE = "APL Logistics Dashboard"

PAGE_ICON = "🚚"

LAYOUT = "wide"

INITIAL_SIDEBAR = "expanded"

# --------------------------------------------------------
# Dashboard Theme
# --------------------------------------------------------

PRIMARY_COLOR = "#2563EB"

SUCCESS_COLOR = "#16A34A"

WARNING_COLOR = "#F59E0B"

DANGER_COLOR = "#DC2626"

BACKGROUND_COLOR = "#F8FAFC"

CARD_COLOR = "#FFFFFF"

TEXT_COLOR = "#1F2937"

# --------------------------------------------------------
# KPI Names
# --------------------------------------------------------

KPI_TOTAL_ORDERS = "Total Orders"

KPI_ON_TIME = "On-Time Delivery %"

KPI_DELAYED = "Delayed Delivery %"

KPI_AVG_DELAY = "Average Delay (Days)"

KPI_LATE_RISK = "Late Delivery Risk %"

KPI_AVG_SALES = "Average Sales"

KPI_AVG_PROFIT = "Average Profit"

# --------------------------------------------------------
# Required Dataset Columns
# --------------------------------------------------------

REQUIRED_COLUMNS = [

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

# --------------------------------------------------------
# Delay Labels
# --------------------------------------------------------

EARLY = "Early"

ON_TIME = "On-Time"

DELAYED = "Delayed"

# --------------------------------------------------------
# Dashboard Footer
# --------------------------------------------------------

FOOTER_TEXT = (
    "Delivery Performance, Delay Risk, and Logistics "
    "Efficiency Analysis | APL Logistics"
)


# --------------------------------------------------------
# Streamlit Configuration Function
# --------------------------------------------------------

def configure_page():
    """
    Configure Streamlit page settings.
    """

    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT,
        initial_sidebar_state=INITIAL_SIDEBAR,
    )