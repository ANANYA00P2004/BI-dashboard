import streamlit as st
import pandas as pd
from utils.data_loader import load_campaign_data, load_business_data, merge_campaign_business_data
from utils.chart_functions import (create_revenue_by_platform_chart, create_efficiency_trends_chart, 
                                  create_roas_comparison_chart, create_cac_clv_scatter_chart, 
                                  create_gross_profit_waterfall_chart, create_campaign_tactic_heatmap,
                                  create_conversion_funnel_chart, create_platform_revenue_pie_chart,
                                  create_engagement_metrics_chart)
import config

# Page configuration
st.set_page_config(
    page_title="Marketing Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# MINIMAL SPACING CSS with removed top margins and compact KPIs
st.markdown("""
<style>
    /* Hide Streamlit default header and remove all top spacing */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 1rem;
        max-width: none;
    }
    
    /* Remove default Streamlit margins */
    .stApp > header {
        background-color: transparent;
    }
    
    .dashboard-title {
        text-align: center;
        font-size: 26px;
        font-weight: bold;
        color: #1565C0;
        margin-bottom: 8px;
        margin-top: 0px !important;
        padding-top: 0px !important;
    }
    
    /* Ultra-minimal KPI cards */
    div[data-testid="metric-container"] {
        background-color: #E3F2FD;
        border: 1px solid #BBDEFB;
        padding: 8px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        margin: 2px 0;
        transition: transform 0.2s ease;
        min-height: 65px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    div[data-testid="metric-container"] > div[data-testid="stMarkdownContainer"] > div {
        color: #1565C0 !important;
        font-size: 10px !important;
        font-weight: 500 !important;
        text-align: center;
        margin-bottom: 4px !important;
        line-height: 1.0 !important;
    }
    
    div[data-testid="metric-container"] > div > div[data-testid="stMarkdownContainer"] > div {
        color: #0D47A1 !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-align: center;
    }
    
    .section-header {
        color: #1565C0;
        font-size: 16px;
        font-weight: 600;
        margin: 4px 0 3px 0;
        border-bottom: 1px solid #BBDEFB;
        padding-bottom: 1px;
    }
    
    /* Minimal chart containers */
    .chart-container-compact {
        background-color: #FAFAFA;
        border-radius: 6px;
        padding: 6px;
        margin: 1px 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    
    .chart-title-compact {
        color: #1565C0;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 3px;
        text-align: center;
    }
    
    /* Ultra-minimal hover effects */
    .chart-container {
        position: relative;
    }
    
    .hover-insight {
        position: absolute;
        top: 30px;
        right: 6px;
        background-color: #E8F5E8;
        border: 1px solid #4CAF50;
        border-radius: 6px;
        padding: 6px;
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
        z-index: 1000;
        max-width: 160px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        font-size: 10px;
    }
    
    .chart-container:hover .hover-insight {
        opacity: 1;
    }
    
    /* Ultra-compact info boxes */
    .info-box-compact {
        background-color: #F8F9FA;
        border: 1px solid #DEE2E6;
        border-radius: 4px;
        padding: 4px;
        margin: 1px 0;
        text-align: center;
        font-size: 10px;
    }
    
    /* Remove any extra spacing from columns */
    .stColumn > div {
        padding: 0 !important;
    }
    
    /* Advanced chart section styling */
    .advanced-section-divider {
        background: linear-gradient(90deg, #1565C0, #42A5F5, #1565C0);
        height: 2px;
        margin: 15px 0 10px 0;
        border-radius: 1px;
    }
    
    .chart-subsection {
        background-color: #FAFAFA;
        border-radius: 8px;
        padding: 8px;
        margin: 4px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        border-left: 3px solid #1565C0;
    }
    
    .subsection-title {
        color: #1565C0;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 8px;
        text-align: center;
        padding: 2px 0;
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
    # Dashboard Title - Ultra-compact
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
    
    # ROW 1: MINIMAL KPI Cards
    st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4, gap="small")
    
    with kpi_col1:
        st.metric(label="💰 Revenue", value=f"${total_revenue:,.0f}")
    
    with kpi_col2:
        st.metric(label="🛒 Orders", value=f"{total_orders:,.0f}")
    
    with kpi_col3:
        st.metric(label="📊 COGS %", value=f"{avg_cogs:.1f}%")
    
    with kpi_col4:
        st.metric(label="📈 ROAS", value=f"{overall_roas:.2f}x")
    
    # ROW 2: Three Charts - ULTRA-MINIMAL SPACING
    st.markdown('<div class="section-header">Platform Performance Overview</div>', unsafe_allow_html=True)
    
    chart_col1, chart_col2, chart_col3 = st.columns([1, 1, 1], gap="small")
    
    # Chart 1: Revenue by Platform
    with chart_col1:
        st.markdown('<div class="chart-title-compact">📊 Revenue by Platform</div>', unsafe_allow_html=True)
        
        # Ultra-minimal hover insight
        from utils.data_loader import get_revenue_by_platform_data
        platform_revenue = get_revenue_by_platform_data(merged_df)
        if platform_revenue is not None and len(platform_revenue) > 0:
            highest_platform = platform_revenue.iloc[0]['platform']
            highest_revenue = platform_revenue.iloc[0]['total_revenue']
            
            st.markdown(f"""
            <div class="chart-container">
                <div class="hover-insight">
                    <strong>Top:</strong> {highest_platform}<br>
                    ${highest_revenue:,.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        revenue_chart = create_revenue_by_platform_chart(merged_df)
        if revenue_chart:
            revenue_chart.update_layout(height=260, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(revenue_chart, use_container_width=True)
    
    # Chart 2: Customer Acquisition Analysis
    with chart_col2:
        st.markdown('<div class="chart-title-compact">💰 Customer Acquisition</div>', unsafe_allow_html=True)
        
        cac_chart = create_cac_clv_scatter_chart(merged_df)
        if cac_chart:
            cac_chart.update_layout(height=260, margin=dict(t=20, b=20, l=20, r=40))
            st.plotly_chart(cac_chart, use_container_width=True)
    
    # Chart 3: ROAS Comparison
    with chart_col3:
        st.markdown('<div class="chart-title-compact">📈 ROAS by Platform</div>', unsafe_allow_html=True)
        
        # Ultra-minimal ROAS insight
        from utils.data_loader import get_roas_by_platform_data
        roas_data = get_roas_by_platform_data(merged_df)
        if roas_data is not None and len(roas_data) > 0:
            best_roas_platform = roas_data.iloc[0]['platform']
            best_roas_value = roas_data.iloc[0]['roas']
            
            st.markdown(f"""
            <div class="chart-container">
                <div class="hover-insight">
                    <strong>Best:</strong> {best_roas_platform}<br>
                    {best_roas_value:.2f}x
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        roas_chart = create_roas_comparison_chart(merged_df)
        if roas_chart:
            roas_chart.update_layout(height=260, margin=dict(t=20, b=20, l=50, r=20))
            st.plotly_chart(roas_chart, use_container_width=True)
    
    # ROW 3: Two Charts - ULTRA-MINIMAL SPACING
    st.markdown('<div class="section-header">Performance Trends & Profitability</div>', unsafe_allow_html=True)
    
    trend_col1, trend_col2 = st.columns([0.6, 0.4], gap="small")
    
    # Chart 4: Weekly Campaign Efficiency Trends
    with trend_col1:
        st.markdown('<div class="chart-title-compact">📈 Weekly Campaign Efficiency</div>', unsafe_allow_html=True)
        
        # Ultra-minimal efficiency insight
        from utils.data_loader import get_efficiency_metrics_data
        efficiency_data = get_efficiency_metrics_data(merged_df)
        
        if efficiency_data is not None and len(efficiency_data) > 0:
            avg_cpc_by_platform = efficiency_data.groupby('platform')['cpc'].mean().sort_values()
            best_platform = avg_cpc_by_platform.index[0]
            best_cpc = avg_cpc_by_platform.iloc[0]
            
            st.markdown(f"""
            <div class="chart-container">
                <div class="hover-insight">
                    <strong>Best:</strong> {best_platform}<br>
                    ${best_cpc:.2f} CPC
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        efficiency_chart = create_efficiency_trends_chart(merged_df)
        if efficiency_chart:
            efficiency_chart.update_layout(height=280, margin=dict(t=20, b=20, l=20, r=60))
            st.plotly_chart(efficiency_chart, use_container_width=True)
    
    # Chart 5: Gross Profit Impact Analysis
    with trend_col2:
        st.markdown('<div class="chart-title-compact">📊 Gross Profit Impact</div>', unsafe_allow_html=True)
        
        waterfall_chart = create_gross_profit_waterfall_chart(merged_df)
        if waterfall_chart:
            waterfall_chart.update_layout(height=280, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(waterfall_chart, use_container_width=True)
    
    # ULTRA-MINIMAL Info Boxes - Single Row
    info_col1, info_col2, info_col3 = st.columns(3, gap="small")
    
    with info_col1:
        st.markdown('<div class="info-box-compact" style="color: #2E7D32;">💡 Revenue & ROAS comparison</div>', unsafe_allow_html=True)
    
    with info_col2:
        st.markdown('<div class="info-box-compact" style="color: #E65100;">🎯 CLV vs CAC analysis</div>', unsafe_allow_html=True)
    
    with info_col3:
        st.markdown('<div class="info-box-compact" style="color: #1565C0;">📊 Weekly trends & profit</div>', unsafe_allow_html=True)

    # SECTION: Advanced Campaign Analysis - UPDATED WITH 4 CHARTS
    st.markdown('<div class="advanced-section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Advanced Campaign Analysis</div>', unsafe_allow_html=True)
    
    # Row 1: Pie Chart and Engagement Metrics (New Charts)
    advanced_row1_col1, advanced_row1_col2 = st.columns([0.45, 0.55], gap="small")
    
    with advanced_row1_col1:
        st.markdown('<div class="chart-subsection">', unsafe_allow_html=True)
        st.markdown('<div class="subsection-title">🥧 Platform Revenue Distribution</div>', unsafe_allow_html=True)
        
        pie_chart = create_platform_revenue_pie_chart(merged_df)
        if pie_chart:
            pie_chart.update_layout(height=320, margin=dict(t=50, b=15, l=15, r=60))
            st.plotly_chart(pie_chart, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with advanced_row1_col2:
        st.markdown('<div class="chart-subsection">', unsafe_allow_html=True)
        st.markdown('<div class="subsection-title">📊 Reach and Engagement Performance</div>', unsafe_allow_html=True)
        
        engagement_chart = create_engagement_metrics_chart(merged_df)
        if engagement_chart:
            engagement_chart.update_layout(height=320, margin=dict(t=50, b=15, l=15, r=15))
            st.plotly_chart(engagement_chart, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Heatmap and Funnel (Existing Charts)  
    advanced_row2_col1, advanced_row2_col2 = st.columns([0.45, 0.55], gap="small")
    
    with advanced_row2_col1:
        st.markdown('<div class="chart-subsection">', unsafe_allow_html=True)
        st.markdown('<div class="subsection-title">🎯 Campaign Tactic Analysis</div>', unsafe_allow_html=True)
        
        tactic_chart = create_campaign_tactic_heatmap(merged_df)
        if tactic_chart:
            tactic_chart.update_layout(height=320, margin=dict(t=50, b=15, l=15, r=60))
            st.plotly_chart(tactic_chart, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with advanced_row2_col2:
        st.markdown('<div class="chart-subsection">', unsafe_allow_html=True)
        st.markdown('<div class="subsection-title">📈 Conversion Funnel Analysis</div>', unsafe_allow_html=True)
        
        funnel_chart = create_conversion_funnel_chart(merged_df)
        if funnel_chart:
            funnel_chart.update_layout(height=320, margin=dict(t=50, b=15, l=15, r=15))
            st.plotly_chart(funnel_chart, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Ultra-compact final message with enhanced styling
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #E3F2FD, #F3E5F5);
        border-radius: 8px;
        padding: 12px;
        margin: 12px 0;
        text-align: center;
        border: 1px solid #BBDEFB;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    ">
        <span style="color: #1565C0; font-size: 14px; font-weight: 600;">
        📊 Complete Marketing Intelligence Dashboard - 9 Interactive Charts
        </span><br>
        <span style="color: #666; font-size: 11px; margin-top: 4px; display: inline-block;">
        Revenue Analysis • Customer Acquisition • Campaign Efficiency • Conversion Funnels
        </span>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()