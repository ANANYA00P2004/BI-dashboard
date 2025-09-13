import pandas as pd
import streamlit as st

@st.cache_data
def load_campaign_data():
    """Load and combine all campaign data from CSV files"""
    try:
        facebook_df = pd.read_csv('data/Facebook.csv')
        google_df = pd.read_csv('data/Google.csv')
        tiktok_df = pd.read_csv('data/TikTok.csv')
        
        facebook_df['platform'] = 'Facebook'
        google_df['platform'] = 'Google'
        tiktok_df['platform'] = 'TikTok'
        
        campaign_df = pd.concat([facebook_df, google_df, tiktok_df], ignore_index=True)
        campaign_df['date'] = pd.to_datetime(campaign_df['date'])
        
        return campaign_df
        
    except Exception as e:
        st.error(f"Error loading campaign data: {e}")
        return None

@st.cache_data
def load_business_data():
    """Load business performance data"""
    try:
        business_df = pd.read_csv('data/Business.csv')
        business_df['date'] = pd.to_datetime(business_df['date'])
        
        # Rename columns to standard names
        column_mapping = {
            '# of orders': 'total_orders',
            '# of new orders': 'new_orders', 
            'new customers': 'new_customers',
            'total revenue': 'total_revenue',
            'gross profit': 'gross_profit',
            'COGS': 'cogs_percentage'
        }
        
        business_df = business_df.rename(columns=column_mapping)
        return business_df
        
    except Exception as e:
        st.error(f"Error loading business data: {e}")
        return None

# UPDATED: Weekly efficiency metrics calculation
def get_efficiency_metrics_data(merged_df):
    """Calculate CPC and CPA metrics for efficiency trends - WEEKLY aggregation"""
    try:
        # Create a copy to avoid modifying original data
        df_copy = merged_df.copy()
        
        # Create week column for weekly aggregation
        df_copy['week'] = df_copy['date'].dt.to_period('W').dt.start_time
        
        # Group by WEEK and platform to get weekly metrics
        efficiency_data = df_copy.groupby(['week', 'platform']).agg({
            'spend': 'sum',
            'clicks': 'sum', 
            'total_orders': 'sum'
        }).reset_index()
        
        # Calculate CPC and CPA on weekly aggregated data for better accuracy
        efficiency_data['cpc'] = efficiency_data['spend'] / efficiency_data['clicks'].replace(0, 1)
        efficiency_data['cpa'] = efficiency_data['spend'] / efficiency_data['total_orders'].replace(0, 1)
        
        # Rename week column back to date for consistency
        efficiency_data = efficiency_data.rename(columns={'week': 'date'})
        
        # Remove any infinite or NaN values
        efficiency_data = efficiency_data.replace([float('inf'), -float('inf')], 0)
        efficiency_data = efficiency_data.fillna(0)
        
        # Sort by date for proper line chart display
        efficiency_data = efficiency_data.sort_values('date')
        
        return efficiency_data
        
    except Exception as e:
        st.error(f"Error calculating weekly efficiency metrics: {e}")
        return None

def merge_campaign_business_data(campaign_df, business_df):
    """Merge campaign and business data with proper allocation"""
    if campaign_df is None or business_df is None:
        return None
    
    # Revenue allocation based on ad spend
    daily_platform_spend = campaign_df.groupby(['date', 'platform'])['spend'].sum().reset_index()
    daily_total_spend = daily_platform_spend.groupby('date')['spend'].sum().reset_index()
    daily_total_spend.columns = ['date', 'total_daily_spend']
    
    daily_platform_spend = pd.merge(daily_platform_spend, daily_total_spend, on='date')
    daily_platform_spend['spend_proportion'] = daily_platform_spend['spend'] / daily_platform_spend['total_daily_spend']
    
    # Merge with business data
    allocation_df = pd.merge(daily_platform_spend, business_df, on='date')
    
    # Allocate business metrics based on spend proportion
    allocation_df['allocated_revenue'] = allocation_df['total_revenue'] * allocation_df['spend_proportion']
    allocation_df['allocated_orders'] = allocation_df['total_orders'] * allocation_df['spend_proportion']
    
    # Merge with campaign data
    merged_df = pd.merge(campaign_df, 
                       allocation_df[['date', 'platform', 'allocated_revenue', 'allocated_orders']], 
                       on=['date', 'platform'], how='inner')
    
    # Rename allocated columns
    merged_df = merged_df.rename(columns={
        'allocated_revenue': 'total_revenue',
        'allocated_orders': 'total_orders'
    })
    
    # Add COGS data (same for all platforms on same day)
    cogs_data = business_df[['date', 'cogs_percentage']].drop_duplicates()
    merged_df = pd.merge(merged_df, cogs_data, on='date', how='left')
    
    return merged_df

def get_revenue_by_platform_data(merged_df):
    """Get revenue data aggregated by platform"""
    platform_revenue = merged_df.groupby('platform')['total_revenue'].sum().reset_index()
    platform_revenue = platform_revenue.sort_values('total_revenue', ascending=False)
    return platform_revenue
