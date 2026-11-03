
import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# 1. PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Sales Data Analysis Dashboard")
st.caption("Electronics Store Orders | 2019")

# =====================================
# 2. LOAD DATASET
# =====================================

@st.cache_data
def load_data():
    df = pd.read_csv("Sales Data.csv")

    # Remove unnecessary column
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # Handle missing values
    df = df.dropna()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Convert columns into correct data types
    df["Quantity Ordered"] = pd.to_numeric(
        df["Quantity Ordered"], errors="coerce"
    )

    df["Price Each"] = pd.to_numeric(
        df["Price Each"], errors="coerce"
    )

    df["Order Date"] = pd.to_datetime(
        df["Order Date"], errors="coerce"
    )

    df = df.dropna()

    # Create new columns
    df["Sales"] = (
        df["Quantity Ordered"] * df["Price Each"]
    )

    df["Month"] = df["Order Date"].dt.month_name()
    df["Hour"] = df["Order Date"].dt.hour
    df["Day"] = df["Order Date"].dt.day_name()

    df["City"] = df["Purchase Address"].apply(
        lambda address: address.split(",")[-2].strip()
        if len(address.split(",")) >= 2 else "Unknown"
    )

    df["State"] = df["Purchase Address"].apply(
        lambda address: address.split(",")[-1].strip().split(" ")[0]
        if len(address.split(",")) >= 3 else "Unknown"
    )

    df["City"] = df["City"] + " (" + df["State"] + ")"

    return df


df = load_data()

# =====================================
# 3. DATASET INFORMATION
# =====================================

st.sidebar.header("Dashboard Filters")

st.sidebar.write("Dataset Information")
st.sidebar.write("Total Rows:", len(df))

# =====================================
# 4. SIDEBAR FILTERS
# =====================================

months = sorted(
    df["Month"].dropna().unique(),
    key=lambda x: pd.to_datetime(x, format="%B").month
)

cities = sorted(df["City"].unique())
products = sorted(df["Product"].unique())

selected_months = st.sidebar.multiselect(
    "Select Month",
    months,
    default=months
)

selected_cities = st.sidebar.multiselect(
    "Select City",
    cities,
    default=cities
)

selected_products = st.sidebar.multiselect(
    "Select Product",
    products,
    default=products
)

# =====================================
# 5. FILTER DATA
# =====================================

filtered_df = df[
    (df["Month"].isin(selected_months)) &
    (df["City"].isin(selected_cities)) &
    (df["Product"].isin(selected_products))
]

# =====================================
# 6. DASHBOARD TABS
# =====================================

dashboard_tab, cleaning_tab = st.tabs(
    ["Dashboard", "Data Cleaning"]
)

with dashboard_tab:

    if filtered_df.empty:
        st.warning(
            "No data available. Please change your filters."
        )

    else:

        # =====================================
        # 7. KPI CARDS
        # =====================================

        total_sales = filtered_df["Sales"].sum()
        total_orders = filtered_df["Order ID"].nunique()
        items_sold = filtered_df["Quantity Ordered"].sum()
        average_order = total_sales / total_orders

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Sales",
            f"${total_sales:,.2f}"
        )

        col2.metric(
            "Number of Orders",
            f"{total_orders:,}"
        )

        col3.metric(
            "Items Sold",
            f"{items_sold:,}"
        )

        col4.metric(
            "Average Order Value",
            f"${average_order:,.2f}"
        )

        st.divider()

        # =====================================
        # 8. UNIVARIATE ANALYSIS
        # =====================================

        st.header("Univariate Analysis")

        # Quantity Ordered
        st.subheader("Quantity Ordered Distribution")

        fig = px.histogram(
            filtered_df,
            x="Quantity Ordered",
            title="Distribution of Quantity Ordered"
        )

        st.plotly_chart(fig, use_container_width=True)

        # TODO: Write your observation here

        # Price Each
        st.subheader("Price Each Distribution")

        fig = px.histogram(
            filtered_df,
            x="Price Each",
            title="Distribution of Product Prices"
        )

        st.plotly_chart(fig, use_container_width=True)

        # TODO: Add Sales, Product, City, Month and Hour graphs.

        # =====================================
        # 9. BIVARIATE ANALYSIS
        # =====================================

        st.header("Bivariate Analysis")

        # TODO 1: Average Sales per Order by City
        # TODO 2: Quantity Ordered by Product
        # TODO 3: Monthly and Hourly Sales
        # TODO 4: Relationship between Price and Quantity

        # =====================================
        # 10. RESEARCH QUESTIONS
        # =====================================

        st.header("Research Questions")

        # TODO: Select two original research questions.
        # Create Plotly visualizations and write insights.

        # =====================================
        # 11. CONCLUSION
        # =====================================

        st.header("Conclusion")

        # TODO: Add 4-5 findings from your actual analysis.


with cleaning_tab:

    st.header("Data Cleaning Report")

    st.write("Dataset Shape:", df.shape)

    st.write("Missing Values:")
    st.dataframe(df.isnull().sum())

    st.write("Duplicate Rows:", df.duplicated().sum())

    st.write("Summary Statistics:")
    st.dataframe(df.describe())

    # TODO: Add cleaning steps row-count table.
    # TODO: Add Quantity and Sales outlier graphs.
    # TODO: Explain your outlier decisions.
