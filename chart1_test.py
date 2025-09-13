import streamlit as st
from utils.data_loader import load_campaign_data, load_business_data, merge_campaign_business_data
from utils.chart_functions import create_revenue_by_platform_chart

st.set_page_config(page_title="Chart 1 Test", layout="wide")

st.title("📊 Chart 1: Revenue by Platform")

# Load data
with st.spinner("Loading data..."):
    campaign_df = load_campaign_data()
    business_df = load_business_data()

if campaign_df is not None and business_df is not None:
    # Merge data
    merged_df = merge_campaign_business_data(campaign_df, business_df)
    
    st.success(f"✅ Data loaded successfully! {len(merged_df)} records found.")
    
    # Create and display chart
    chart = create_revenue_by_platform_chart(merged_df)
    st.plotly_chart(chart, use_container_width=True)
    
    # Show data preview
    with st.expander("📋 View Data Preview"):
        st.dataframe(merged_df.head())
        
else:
    st.error("❌ Could not load data. Check your CSV files in the data folder.")
