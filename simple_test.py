import streamlit as st

st.title("🎉 Hello Marketing Dashboard!")
st.write("If you can see this, Streamlit is working correctly.")

# Test if we can load libraries
try:
    import pandas as pd
    import plotly.express as px
    st.success("✅ All required libraries loaded successfully!")
    
    # Create a simple test chart
    test_data = {'Platform': ['Facebook', 'Google', 'TikTok'], 
                 'Revenue': [50000, 75000, 25000]}
    df = pd.DataFrame(test_data)
    
    fig = px.bar(df, x='Platform', y='Revenue', title='Test Chart')
    st.plotly_chart(fig)
    
except Exception as e:
    st.error(f"Error loading libraries: {e}")

st.write("📁 Current working directory files:")
import os
files = os.listdir('.')
st.write(files)
