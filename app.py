import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title='Sales Dashboard')
st.title("Interactive Sales Dashboard")

# Load dataset
df = pd.read_csv("sales_data.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Sidebar filters
st.sidebar.header("Filter Data")

location_filter = st.sidebar.multiselect(
    "Select Location",
    options=df["Location"].unique(),
    default=df["Location"].unique()
)

product_filter = st.sidebar.multiselect(
    "Select Product",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

# Filter dataframe
filtered_df = df[df["Location"].isin(location_filter) & df["Product"].isin(product_filter)  ]

st.markdown(f'##### Location selected:{location_filter} \n ##### Product selected:{product_filter} ')

# KPI Metrics
col1, col2 = st.columns(2)
with col1:
    total_sales = filtered_df["Sales"].sum()
    st.metric("Total Sales", f"${total_sales:.2f}")
with col2:
    avg_sales = filtered_df["Sales"].mean()
    st.metric("Average Sales", f"${avg_sales:.2f}")

tab1, tab2 = st.tabs(['Sales by Product', 'Sales by Location',])   

with tab1:
    st.subheader("Sales by Product")
    product_data = filtered_df.groupby("Product")["Sales"].sum().reset_index()
    fig1 = px.bar(product_data,x="Product",y="Sales", color="Product", text= "Sales", title="Total Sales by Product")
    st.plotly_chart(fig1)

with tab2:
    st.subheader("Sales by Location")
    location_data = filtered_df.groupby("Location")["Sales"].sum().reset_index()
    fig2 = px.bar(location_data,x="Location",y="Sales", title="Total Sales by Location")
    st.plotly_chart(fig2)