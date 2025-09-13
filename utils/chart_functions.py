import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import config

def create_efficiency_trends_chart(merged_df):
    """Create Chart 2: Campaign Efficiency Trends Multi-line Chart - WEEKLY TRENDS"""
    from utils.data_loader import get_efficiency_metrics_data
    
    efficiency_data = get_efficiency_metrics_data(merged_df)
    
    if efficiency_data is None or len(efficiency_data) == 0:
        return None
    
    # Create single y-axis chart (no secondary axis to avoid crowding)
    fig = go.Figure()
    
    # Updated color scheme - different colors for CPC vs CPA
    cpc_colors = {
        'Facebook': '#1877F2',  # Facebook Blue
        'Google': '#4285F4',    # Google Blue  
        'TikTok': '#FF0050'     # TikTok Pink
    }
    
    cpa_colors = {
        'Facebook': '#28A745',  # Green
        'Google': '#FFC107',    # Orange/Yellow
        'TikTok': '#6F42C1'     # Purple
    }
    
    platforms = efficiency_data['platform'].unique()
    
    # Add CPC and CPA lines for each platform (all solid lines, different colors)
    for platform in platforms:
        platform_data = efficiency_data[efficiency_data['platform'] == platform].sort_values('date')
        
        # Skip if no data for this platform
        if len(platform_data) == 0:
            continue
        
        # CPC Line (solid)
        fig.add_trace(
            go.Scatter(
                x=platform_data['date'],
                y=platform_data['cpc'],
                mode='lines+markers',
                name=f'{platform} CPC',
                line=dict(
                    color=cpc_colors.get(platform, '#000000'),
                    width=3
                ),
                marker=dict(
                    size=8,
                    symbol='circle'
                ),
                hovertemplate=
                '<b>%{fullData.name}</b><br>' +
                'Week of: %{x}<br>' +
                'Cost per Click: $%{y:.2f}<br>' +
                f'<i>💡 {platform} Weekly CPC Trend</i><extra></extra>',
                legendgroup=f'{platform}_CPC',
                showlegend=True
            )
        )
        
        # CPA Line (solid, different color)
        fig.add_trace(
            go.Scatter(
                x=platform_data['date'],
                y=platform_data['cpa'],
                mode='lines+markers',
                name=f'{platform} CPA',
                line=dict(
                    color=cpa_colors.get(platform, '#000000'),
                    width=3  # Same width as CPC, but different color
                ),
                marker=dict(
                    size=8,
                    symbol='diamond'
                ),
                hovertemplate=
                '<b>%{fullData.name}</b><br>' +
                'Week of: %{x}<br>' +
                'Cost per Acquisition: $%{y:.2f}<br>' +
                f'<i>💡 {platform} Weekly CPA Trend</i><extra></extra>',
                legendgroup=f'{platform}_CPA',
                showlegend=True
            )
        )
    
    # Update x-axis
    fig.update_xaxes(
        title_text="Week (17-Week Timeline)",
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128,128,128,0.2)',
        dtick="W1",
        showticklabels=False  # ADDED: Hide x-axis tick labels (dates)
    )
    
    # Single Y-axis (no secondary axis to avoid crowding)
    fig.update_yaxes(
        title_text="Cost ($)",  # Simplified title
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128,128,128,0.2)',
        tickformat='$,.2f',
        tickangle=0,  # Keep labels horizontal
        tickfont=dict(size=10)  # Smaller font for better readability
    )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text="Weekly Campaign Efficiency Trends",
            x=0.5,
            font=dict(size=16, color='#1565C0')
        ),
        height=500,
        hovermode='x unified',
        legend=dict(
            orientation="v",  # Vertical legend to save space
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(size=9)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        margin=dict(r=120)  # Add right margin for legend
    )
    
    return fig

def create_revenue_by_platform_chart(merged_df):
    """Create Revenue by Platform Bar Chart with hover insights"""
    from utils.data_loader import get_revenue_by_platform_data
    
    platform_revenue = get_revenue_by_platform_data(merged_df)
    
    if platform_revenue is None or len(platform_revenue) == 0:
        return None
    
    # Calculate percentages for better insights
    total_revenue = platform_revenue['total_revenue'].sum()
    platform_revenue['percentage'] = (platform_revenue['total_revenue'] / total_revenue * 100)
    
    fig = px.bar(
        platform_revenue,
        x='platform',
        y='total_revenue',
        title='Total Revenue by Marketing Platform',
        color='platform',
        color_discrete_map=config.PLATFORM_COLORS
    )
    
    # Enhanced hover template with percentage
    fig.update_traces(
        texttemplate='$%{y:,.0f}', 
        textposition='outside',
        textfont_size=11,
        hovertemplate='<b>%{x} Platform</b><br>' +
                     'Revenue: <b>$%{y:,.0f}</b><br>' +
                     'Share: <b>%{customdata:.1f}%</b><br>' +
                     '<i>💡 Hover to compare performance</i><extra></extra>',
        customdata=platform_revenue['percentage']
    )
    
    fig.update_layout(
        xaxis_title="Platform",
        yaxis_title="Total Revenue ($)",
        showlegend=False,
        height=500,
        title_x=0.5,
        yaxis=dict(tickformat='$,.0f')
    )
    
    return fig
