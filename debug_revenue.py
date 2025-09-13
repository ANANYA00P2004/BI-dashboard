import streamlit as st
import pandas as pd

st.title("🔍 Revenue Calculation Debug")

# Load business data
business_df = pd.read_csv('data/Business.csv')
business_df['date'] = pd.to_datetime(business_df['date'])

# Fix column name
if 'total revenue' in business_df.columns:
    business_df = business_df.rename(columns={'total revenue': 'total_revenue'})

st.subheader("📊 Business Data Summary")
st.write(f"Business data shape: {business_df.shape}")
st.write(f"Date range: {business_df['date'].min()} to {business_df['date'].max()}")
st.write(f"Total revenue in business file: ${business_df['total_revenue'].sum():,.0f}")
st.dataframe(business_df.head())

# Load campaign data
campaign_files = ['Facebook.csv', 'Google.csv', 'TikTok.csv']
all_campaigns = []

for file in campaign_files:
    df = pd.read_csv(f'data/{file}')
    df['platform'] = file.replace('.csv', '')
    df['date'] = pd.to_datetime(df['date'])
    all_campaigns.append(df)
    
    st.subheader(f"📄 {file}")
    st.write(f"Shape: {df.shape}")
    st.write(f"Date range: {df['date'].min()} to {df['date'].max()}")
    st.dataframe(df.head(3))

# Combine campaign data
campaign_df = pd.concat(all_campaigns, ignore_index=True)
st.subheader("📈 Combined Campaign Data")
st.write(f"Combined shape: {campaign_df.shape}")
st.write("Platforms:", campaign_df['platform'].unique())

# Show date overlaps
st.subheader("📅 Date Analysis")
campaign_dates = set(campaign_df['date'].unique())
business_dates = set(business_df['date'].unique())
common_dates = campaign_dates.intersection(business_dates)

st.write(f"Campaign unique dates: {len(campaign_dates)}")
st.write(f"Business unique dates: {len(business_dates)}")
st.write(f"Common dates: {len(common_dates)}")

# Merge and analyze
merged_df = pd.merge(campaign_df, business_df, on='date', how='inner')
st.subheader("🔗 After Merge Analysis")
st.write(f"Merged shape: {merged_df.shape}")

# Check revenue by platform BEFORE grouping
st.write("Revenue per row by platform (first 10 rows):")
st.dataframe(merged_df[['date', 'platform', 'total_revenue']].head(10))

# Group by platform
platform_revenue = merged_df.groupby('platform')['total_revenue'].sum().reset_index()
st.subheader("💰 Platform Revenue (WRONG - This is what we see in chart)")
st.dataframe(platform_revenue)

# The CORRECT way - sum business revenue by unique dates first
st.subheader("✅ Correct Calculation")
# Get unique dates that have campaign activity
active_dates = merged_df['date'].unique()
correct_total = business_df[business_df['date'].isin(active_dates)]['total_revenue'].sum()
st.metric("Correct Total Revenue", f"${correct_total:,.0f}")

# Show the problem
st.error("🚨 PROBLEM: Each business day's revenue is being counted 3 times (once for each platform)!")
st.info("💡 SOLUTION: We need to allocate revenue based on platform performance, not duplicate it.")
