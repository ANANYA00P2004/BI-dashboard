import streamlit as st
import pandas as pd
from utils.data_loader import load_campaign_data, load_business_data, merge_campaign_business_data
from utils.chart_functions import (create_revenue_by_platform_chart, create_efficiency_trends_chart, 
                                  create_roas_comparison_chart, create_cac_clv_scatter_chart, 
                                  create_gross_profit_waterfall_chart)
import config

# Page configuration
st.set_page_config(
    page_title="Marketing Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# Clean CSS for KPI cards + Hover effect for chart section + Partition line
st.markdown("""
<style>
    .dashboard-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #1565C0;
        margin-bottom: 30px;
    }
    
    div[data-testid="metric-container"] {
        background-color: #E3F2FD;
        border: 2px solid #BBDEFB;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        margin: 8px 0;
        transition: transform 0.2s ease;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    
    div[data-testid="metric-container"] > div[data-testid="stMarkdownContainer"] > div {
        color: #1565C0 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        text-align: center;
        margin-bottom: 10px !important;
        line-height: 1.2 !important;
    }
    
    div[data-testid="metric-container"] > div > div[data-testid="stMarkdownContainer"] > div {
        color: #0D47A1 !important;
        font-size: 28px !important;
        font-weight: bold !important;
        text-align: center;
    }
    
    .section-header {
        color: #1565C0;
        font-size: 24px;
        font-weight: 600;
        margin: 20px 0 15px 0;
        border-bottom: 2px solid #BBDEFB;
        padding-bottom: 5px;
    }
    
    /* Hover effect for chart container */
    .chart-container {
        position: relative;
    }
    
    .hover-insight {
        position: absolute;
        top: 50px;
        right: 10px;
        background-color: #E8F5E8;
        border: 2px solid #4CAF50;
        border-radius: 15px;
        padding: 15px;
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
        z-index: 1000;
        max-width: 250px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .chart-container:hover .hover-insight {
        opacity: 1;
    }
    
    /* Blue partition line between charts */
    .chart-partition {
        border-right: 4px solid #1565C0;
        padding-right: 15px;
        margin-right: 10px;
    }
    
    .chart-section {
        padding-left: 15px;
        margin-left: 10px;
    }
</style>
""", unsafe_allow_html=True)

def calculate_kpis(merged_df):
    """Calculate KPI values cleanly"""
    total_revenue = merged_df['total_revenue'].sum()
    total_orders = merged_df['total_orders'].sum()
    avg_cogs = merged_df['cogs_percentage'].mean()
    total_spend = merged_df['spend'].sum()
    overall_roas = total_revenue / total_spend if total_spend > 0 else 0
    
    return total_revenue, total_orders, avg_cogs, overall_roas

def main():
    # Dashboard Title
    st.markdown('<h1 class="dashboard-title">Marketing Intelligence Dashboard</h1>', unsafe_allow_html=True)
    
    # Load and merge data
    with st.spinner("Loading data..."):
        campaign_df = load_campaign_data()
        business_df = load_business_data()
    
    if campaign_df is None or business_df is None:
        st.error("❌ Could not load data. Please check your CSV files.")
        return
    
    merged_df = merge_campaign_business_data(campaign_df, business_df)
    
    if merged_df is None:
        st.error("❌ Could not merge data.")
        return
    
    # Calculate KPIs
    total_revenue, total_orders, avg_cogs, overall_roas = calculate_kpis(merged_df)
    
    # KPI Cards Row
    st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4, gap="medium")
    
    with kpi_col1:
        st.metric(
            label="💰 Total Revenue Across All Platforms",
            value=f"${total_revenue:,.0f}"
        )
    
    with kpi_col2:
        st.metric(
            label="🛒 Total Orders Generated",
            value=f"{total_orders:,.0f}"
        )
    
    with kpi_col3:
        st.metric(
            label="📊 Average COGS Percentage",
            value=f"{avg_cogs:.1f}%"
        )
    
    with kpi_col4:
        st.metric(
            label="📈 Overall ROAS",
            value=f"{overall_roas:.2f}x"
        )
    
    # Chart Section - Two charts side by side with blue partition line
    st.markdown('<div class="section-header">Platform Performance Analysis</div>', unsafe_allow_html=True)
    
    # Two charts side by side: Revenue (50%) and ROAS (50%) with partition
    revenue_col, roas_col = st.columns([1, 1], gap="small")
    
    with revenue_col:
        st.markdown('<div class="chart-partition">', unsafe_allow_html=True)
        st.subheader("📊 Revenue by Platform")
        
        # Get insight data for hover effect
        from utils.data_loader import get_revenue_by_platform_data
        platform_revenue = get_revenue_by_platform_data(merged_df)
        if platform_revenue is not None and len(platform_revenue) > 0:
            highest_platform = platform_revenue.iloc[0]['platform']
            highest_revenue = platform_revenue.iloc[0]['total_revenue']
            
            # Create chart container with hover insight
            st.markdown(f"""
            <div class="chart-container">
                <div class="hover-insight">
                    <strong>💡 Key Insight:</strong><br>
                    <span style="color: #2E7D32; font-weight: bold;">
                    {highest_platform}</span> generates the highest revenue<br>
                    with <span style="color: #1B5E20; font-size: 18px; font-weight: bold;">
                    ${highest_revenue:,.0f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Display the revenue chart
        revenue_chart = create_revenue_by_platform_chart(merged_df)
        if revenue_chart:
            st.plotly_chart(revenue_chart, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with roas_col:
        st.markdown('<div class="chart-section">', unsafe_allow_html=True)
        st.subheader("📈 Return on Ad Spend by Platform")
        
        # Get ROAS insight data for hover effect
        from utils.data_loader import get_roas_by_platform_data
        roas_data = get_roas_by_platform_data(merged_df)
        if roas_data is not None and len(roas_data) > 0:
            best_roas_platform = roas_data.iloc[0]['platform']
            best_roas_value = roas_data.iloc[0]['roas']
            
            # Create ROAS chart container with hover insight
            st.markdown(f"""
            <div class="chart-container">
                <div class="hover-insight" style="top: 50px; left: 10px;">
                    <strong>💰 ROAS Insight:</strong><br>
                    <span style="color: #2E7D32; font-weight: bold;">
                    {best_roas_platform}</span> has the highest ROAS<br>
                    at <span style="color: #1B5E20; font-size: 18px; font-weight: bold;">
                    {best_roas_value:.2f}x</span> return
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Display ROAS chart
        roas_chart = create_roas_comparison_chart(merged_df)
        if roas_chart:
            st.plotly_chart(roas_chart, use_container_width=True)
            
            # Add instruction for ROAS chart
            st.markdown("""
            <div style="
                background-color: #F3E5F5;
                border: 2px solid #9C27B0;
                border-radius: 15px;
                padding: 12px;
                margin: 10px 0;
                text-align: center;
            ">
                <span style="color: #6A1B9A; font-size: 14px;">
                💡 <strong>Higher ROAS = More Profitable Platform</strong><br>
                <strong>Hover over bars</strong> for detailed profitability metrics
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Efficiency Chart - 50% width, centered
    col1, efficiency_col, col3 = st.columns([1, 2, 1])
    
    with efficiency_col:
        st.subheader("📈 Weekly Campaign Efficiency Trends")
        
        # Create efficiency chart container with hover insight
        from utils.data_loader import get_efficiency_metrics_data
        efficiency_data = get_efficiency_metrics_data(merged_df)
        
        if efficiency_data is not None and len(efficiency_data) > 0:
            # Calculate best performing platform by average CPC
            avg_cpc_by_platform = efficiency_data.groupby('platform')['cpc'].mean().sort_values()
            best_platform = avg_cpc_by_platform.index[0]
            best_cpc = avg_cpc_by_platform.iloc[0]
            
            st.markdown(f"""
            <div class="chart-container">
                <div class="hover-insight" style="top: 50px; left: 10px;">
                    <strong>⚡ Weekly Efficiency Insight:</strong><br>
                    <span style="color: #2E7D32; font-weight: bold;">
                    {best_platform}</span> has the lowest average weekly CPC<br>
                    at <span style="color: #1B5E20; font-size: 18px; font-weight: bold;">
                    ${best_cpc:.2f}</span> per click
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Display efficiency chart
        efficiency_chart = create_efficiency_trends_chart(merged_df)
        if efficiency_chart:
            st.plotly_chart(efficiency_chart, use_container_width=True)
            
            # Updated instruction for efficiency chart
            st.markdown("""
            <div style="
                background-color: #E8F5E8;
                border: 2px solid #4CAF50;
                border-radius: 15px;
                padding: 12px;
                margin: 10px 0;
                text-align: center;
            ">
                <span style="color: #2E7D32; font-size: 14px;">
                📊 <strong>CPC:</strong> Blue tones | <strong>CPA:</strong> Green/Orange/Purple<br>
                <strong>Hover over lines</strong> for weekly efficiency metrics
                </span>
            </div>
            """, unsafe_allow_html=True)

    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)

    # NEW: CAC vs CLV and Gross Profit Charts Section
    st.markdown('<div class="section-header">Advanced Analytics</div>', unsafe_allow_html=True)
    
    # Two new charts: CAC/CLV (45%) and Gross Profit Waterfall (55%) with partition
    cac_col, profit_col = st.columns([0.45, 0.55], gap="small")
    
    with cac_col:
        st.markdown('<div class="chart-partition">', unsafe_allow_html=True)
        st.subheader("💰 Customer Acquisition Analysis")
        
        # Display CAC vs CLV scatter chart
        cac_chart = create_cac_clv_scatter_chart(merged_df)
        if cac_chart:
            st.plotly_chart(cac_chart, use_container_width=True)
            
            # Add instruction for CAC/CLV chart
            st.markdown("""
            <div style="
                background-color: #FFF8E1;
                border: 2px solid #FF9800;
                border-radius: 15px;
                padding: 12px;
                margin: 10px 0;
                text-align: center;
            ">
                <span style="color: #E65100; font-size: 14px;">
                💡 <strong>Ideal: CLV should be 3x+ higher than CAC</strong><br>
                <strong>Bubble size</strong> = Customer Volume
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with profit_col:
        st.markdown('<div class="chart-section">', unsafe_allow_html=True)
        st.subheader("📊 Gross Profit Impact Analysis")
        
        # Display Gross Profit Waterfall chart
        waterfall_chart = create_gross_profit_waterfall_chart(merged_df)
        if waterfall_chart:
            st.plotly_chart(waterfall_chart, use_container_width=True)
            
            # Add instruction for waterfall chart
            st.markdown("""
            <div style="
                background-color: #E3F2FD;
                border: 2px solid #2196F3;
                border-radius: 15px;
                padding: 12px;
                margin: 10px 0;
                text-align: center;
            ">
                <span style="color: #1565C0; font-size: 14px;">
                📈 <strong>Shows true profitability after COGS and ad spend</strong><br>
                <strong>Green</strong> = Profit | <strong>Red</strong> = Loss
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Future charts section
    st.markdown('<div class="section-header">Additional Analytics</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="
        background-color: #FFF3E0;
        border: 2px solid #FF9800;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
    ">
        <h4 style="color: #E65100;">📊 More Insights Coming Soon</h4>
        <p style="color: #BF360C;">
            Additional marketing analytics and performance metrics will be displayed here.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
