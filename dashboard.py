import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Sales Insight Dashboard",
    layout="wide"
)


# Load data
df = pd.read_csv("output/cleaned_data.csv")


st.title("📊 Sales Insight Dashboard")
st.caption("Business Intelligence & Data Automation System")
st.sidebar.markdown("---")
st.sidebar.success("Python + SQLite + Streamlit")

st.sidebar.markdown("---")

st.sidebar.markdown("""
### Project Details

**Developer:** Pratham Mishra

**Technology Stack:**
- Python
- Pandas
- SQLite
- Streamlit

**Dataset Records:** 9800+
""")

st.sidebar.markdown("---")

selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + sorted(df["Region"].unique())
)

if selected_region != "All":
    df = df[df["Region"] == selected_region]


# KPIs
total_sales = round(df["Sales"].sum(), 2)
total_orders = len(df)
total_customers = df["Customer Name"].nunique()




st.markdown("""
### 📈 Business Performance Overview
Real-time sales analytics and reporting dashboard
""")

# KPI cards
col1, col2, col3, col4 = st.columns(4)
total_regions = df["Region"].nunique()
col4.metric("🌍 Regions", total_regions)

col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📦 Total Orders", total_orders)
col3.metric("👥 Customers", total_customers)
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Regional Sales Performance")

    region_sales = (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    fig = px.bar(
    region_sales,
    title="Regional Sales Analysis",
    color=region_sales.values
)

st.plotly_chart(
    fig,
    use_container_width=True
)

with col2:
    st.subheader("Top 10 Customers")

    top_customers = (
        df.groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig = px.bar(
    top_customers,
    title="Top Customer Analysis",
    color=top_customers.values
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("Category Sales Distribution")

category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

fig = px.pie(
    values=category_sales.values,
    names=category_sales.index,
    title="Category Sales Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)




st.divider()

st.subheader("📋 Dataset Preview")
st.caption("Sample records from the processed sales dataset")

st.markdown("### Database Statistics")

c1, c2, c3 = st.columns(3)

c1.metric("Rows", len(df))
c2.metric("Columns", len(df.columns))
c3.metric("Unique Customers", df["Customer Name"].nunique())

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Processed Dataset",
    csv,
    "processed_sales_data.csv",
    "text/csv"
)

st.dataframe(
    df[
        [
            "Customer Name",
            "Region",
            "Category",
            "Sales"
        ]
    ].head(20)
)