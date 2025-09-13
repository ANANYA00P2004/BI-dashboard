import streamlit as st
import pandas as pd
from utils.data_loader import load_all_data, merge_campaign_business_data
from utils.chart_functions import create_revenue_by_platform_chart

st.set_page_config(page_title="Chart 1 Test", layout="wide")

st.title("📊 Chart 1: Revenue by Platform Test")

# Load data
campaign_df, business_df = load_all_data()

if campaign_df is not None and business_df is not None:
    # Merge data
    merged_df = merge_campaign_business_data(campaign_df, business_df)
    
    # Display the chart
    st.subheader("💰 Total Revenue by Marketing Platform")
    revenue_chart = create_revenue_by_platform_chart(merged_df)
    st.plotly_chart(revenue_chart, use_container_width=True)
    
    # Show data summary
    platform_summary = merged_df.groupby('platform')['total_revenue'].agg(['sum', 'count']).reset_index()
    st.subheader("📈 Revenue Summary by Platform")
    st.dataframe(platform_summary)
    
else:
    st.error("Could not load data. Please check your CSV files.")
