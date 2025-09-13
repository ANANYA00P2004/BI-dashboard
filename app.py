import streamlit as st
from utils.data_loader import get_revenue_by_platform_data  # move import to top

def display_revenue_chart(merged_df):
    """Display Chart 1: Revenue by Platform"""
    st.subheader("💰 Total Revenue by Marketing Platform")
    
    # Create and display the chart (make sure this function is defined/imported)
    revenue_chart = create_revenue_by_platform_chart(merged_df)
    st.plotly_chart(revenue_chart, use_container_width=True)
    
    # Get revenue data
    platform_revenue = get_revenue_by_platform_data(merged_df)
    
    # Safely find the highest revenue platform
    highest_row = platform_revenue.loc[platform_revenue['total_revenue'].idxmax()]
    highest_platform = highest_row['platform']
    highest_revenue = highest_row['total_revenue']
    
    # Show key insight
    st.info(
        f"💡 **Insight**: {highest_platform} is the highest revenue-generating platform "
        f"with ${highest_revenue:,.0f} in total revenue over the 120-day period."
    )
