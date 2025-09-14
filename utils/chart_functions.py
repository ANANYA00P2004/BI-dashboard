import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import config

def create_campaign_tactic_heatmap(merged_df):
    """Create Campaign Tactic Effectiveness Matrix Heatmap - FIXED TITLE SPACING"""
    from utils.data_loader import get_campaign_tactic_heatmap_data
    
    heatmap_data = get_campaign_tactic_heatmap_data(merged_df)
    
    if heatmap_data is None or len(heatmap_data) == 0:
        return None
    
    # Create pivot table for heatmap
    heatmap_pivot = heatmap_data.pivot(index='Platform', columns='Campaign Tactic', values='Performance Score')
    
    # FIXED: Use go.Heatmap with corrected colorbar configuration
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        colorscale='RdYlGn',
        text=heatmap_pivot.values,
        texttemplate="%{text:.0f}",
        textfont={"size": 11, "color": "black"},
        hovertemplate='<b>%{y}</b> on <b>%{x}</b><br>' + 
                     'Performance Score: <b>%{z:.0f}/100</b><br>' + 
                     '<i>Higher score = Better performance</i><extra></extra>',
        colorbar=dict(
            title=dict(text="Performance<br>Score", font=dict(size=10)),
            tickfont=dict(size=9)
        )
    ))
    
    fig.update_layout(
        title='Campaign Tactic Effectiveness Matrix',
        title_x=0.5,
        title_y=0.98,  # FIXED: Position title at very top
        height=350,    # FIXED: Reduced height to accommodate title
        margin=dict(t=100, b=10, l=60, r=80),  # FIXED: Proper margins
        xaxis_title="Campaign Tactics",
        yaxis_title="Platforms",
        xaxis=dict(
            tickfont=dict(size=10),
            tickangle=45,
            title_standoff=20  # FIXED: Add space between axis and title
        ),
        yaxis=dict(
            tickfont=dict(size=10),
            title_standoff=20  # FIXED: Add space between axis and title
        ),
        title_font=dict(size=14)  # FIXED: Smaller title font
    )
    
    return fig

def create_conversion_funnel_chart(merged_df):
    """Create Marketing Funnel Performance by Platform - WITH ENHANCED HOVER EFFECTS"""
    from utils.data_loader import get_conversion_funnel_data
    
    funnel_data = get_conversion_funnel_data(merged_df)
    
    if funnel_data is None or len(funnel_data) == 0:
        return None
    
    fig = go.Figure()
    
    # Platform colors
    platform_colors = {
        'Facebook': config.PLATFORM_COLORS.get('Facebook', '#1877F2'),
        'Google': config.PLATFORM_COLORS.get('Google', '#4285F4'),
        'TikTok': config.PLATFORM_COLORS.get('TikTok', '#FF0050')
    }
    
    platforms = funnel_data['Platform'].unique()
    stages = ['Impressions', 'Clicks', 'Orders', 'Revenue']
    
    # Create funnel for each platform
    for i, platform in enumerate(platforms):
        platform_data = funnel_data[funnel_data['Platform'] == platform]
        
        # Prepare funnel values and hover data
        funnel_values = []
        funnel_labels = []
        hover_customdata = []
        
        for stage in stages:
            stage_data = platform_data[platform_data['Stage'] == stage]
            if len(stage_data) > 0:
                value = stage_data['Value'].iloc[0]
                conversion_rate = stage_data['Conversion_Rate'].iloc[0]
                
                if stage == 'Revenue':
                    funnel_labels.append(f'{stage}<br>${value:,.0f}')
                    funnel_values.append(value / 1000)  # Scale down revenue for visualization
                    # Custom data for hover: [original_value, conversion_rate, stage, platform]
                    hover_customdata.append([value, f"${conversion_rate:,.0f}/order", stage, platform])
                else:
                    funnel_labels.append(f'{stage}<br>{value:,.0f}')
                    funnel_values.append(value)
                    # Custom data for hover
                    if stage == 'Impressions':
                        hover_customdata.append([value, "100%", stage, platform])
                    else:
                        hover_customdata.append([value, f"{conversion_rate:.2f}%", stage, platform])
        
        # Create funnel chart with COMPLETE enhanced hover template
        fig.add_trace(go.Funnel(
            y=funnel_labels,
            x=funnel_values,
            name=platform,
            marker=dict(
                color=platform_colors[platform],
                line=dict(width=2, color='white')
            ),
            textinfo="value+percent initial",
            textfont=dict(size=10, color='white'),
            # COMPLETE ENHANCED HOVER TEMPLATE WITH HTML FORMATTING
            hovertemplate='<b style="font-size: 14px; color: #FFD700;">🎯 %{fullData.name} Platform</b><br>' +
                         '<hr style="border: 1px solid #FFD700; margin: 5px 0;">' +
                         '<b style="color: #87CEEB;">📊 Stage:</b> <span style="color: white;">%{customdata[2]}</span><br>' +
                         '<b style="color: #87CEEB;">📈 Volume:</b> <span style="color: #90EE90; font-size: 13px;">%{customdata[0]:,.0f}</span><br>' +
                         '<b style="color: #87CEEB;">🎯 Rate:</b> <span style="color: #FFB6C1;">%{customdata[1]}</span><br>' +
                         '<b style="color: #87CEEB;">💡 Performance:</b> <span style="color: #F0E68C;">%{percent}</span><br>' +
                         '<hr style="border: 1px solid #FFD700; margin: 5px 0;">' +
                         '<i style="color: #DDA0DD; font-size: 11px;">🔍 Analyze conversion bottlenecks</i>' +
                         '<extra></extra>',
            customdata=hover_customdata,
            orientation='v'
        ))
    
    fig.update_layout(
        title='Marketing Funnel Performance by Platform',
        title_x=0.5,
        height=450,
        margin=dict(t=20, b=10, l=20, r=20),  # Add this line - increased top margin
        title_y=0.95,  # Add this line - position title lower
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        ),
        font=dict(size=11),
        # Enhanced hover interaction
        hoverlabel=dict(
            bgcolor="rgba(0,0,0,0.8)",
            bordercolor="rgba(255,215,0,0.8)",
            font_size=12,
            font_family="Arial"
        )
    )
    
    return fig


def create_cac_clv_scatter_chart(merged_df):
    """Create Customer Acquisition Cost vs Customer Lifetime Value Scatter Plot"""
    from utils.data_loader import get_cac_clv_data
    
    cac_clv_data = get_cac_clv_data(merged_df)
    
    if cac_clv_data is None or len(cac_clv_data) == 0:
        return None
    
    fig = px.scatter(
        cac_clv_data,
        x='cac',
        y='estimated_clv',
        size='customer_volume',
        color='platform',
        title='Customer Acquisition Cost vs. Customer Lifetime Value',
        color_discrete_map=config.PLATFORM_COLORS,
        size_max=60
    )
    
    # Enhanced hover template
    fig.update_traces(
        hovertemplate='<b>%{fullData.name}</b><br>' +
                     'CAC: <b>$%{x:.2f}</b><br>' +
                     'Estimated CLV: <b>$%{y:.2f}</b><br>' +
                     'New Customers: <b>%{customdata:,.0f}</b><br>' +
                     '<i>CLV should be 3x+ higher than CAC</i><extra></extra>',
        customdata=cac_clv_data['new_customers']
    )
    
    # Add diagonal reference line (CAC = CLV)
    max_val = max(cac_clv_data['cac'].max(), cac_clv_data['estimated_clv'].max())
    fig.add_shape(
        type="line",
        x0=0, y0=0, x1=max_val, y1=max_val,
        line=dict(color="red", width=2, dash="dash"),
    )
    
    fig.update_layout(
        xaxis_title="Customer Acquisition Cost ($)",
        yaxis_title="Estimated Customer Value ($)",
        height=450,
        title_x=0.5,
        xaxis=dict(
            tickformat='$,.0f',
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            tickformat='$,.0f',
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            tickfont=dict(size=10)
        ),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(size=9)
        ),
        margin=dict(r=100)
    )
    
    return fig

def create_gross_profit_waterfall_chart(merged_df):
    """Create Gross Profit Attribution Waterfall Chart - FIXED with different platform colors"""
    from utils.data_loader import get_gross_profit_attribution_data
    
    waterfall_data = get_gross_profit_attribution_data(merged_df)
    
    if waterfall_data is None or len(waterfall_data) == 0:
        return None
    
    fig = go.Figure()
    
    # FIXED: Use platform-specific colors from config
    platform_colors = {
        'Facebook': config.PLATFORM_COLORS.get('Facebook', '#1877F2'),
        'Google': config.PLATFORM_COLORS.get('Google', '#4285F4'),
        'TikTok': config.PLATFORM_COLORS.get('TikTok', '#FF0050')
    }
    
    # Default colors for non-platform bars
    default_colors = {
        'start': '#E0E0E0',
        'total': '#2196F3'
    }
    
    # Add waterfall bars with platform-specific colors
    for i, row in waterfall_data.iterrows():
        if row['type'] == 'start':
            # Starting bar
            fig.add_trace(go.Bar(
                x=[row['category']],
                y=[0],
                name='Start',
                marker_color=default_colors['start'],
                showlegend=False,
                hovertemplate='<b>%{x}</b><br>Value: $0<extra></extra>'
            ))
        elif row['type'] in ['positive', 'negative']:
            # Platform contribution bars - use platform colors
            platform_name = row['platform']
            bar_color = platform_colors.get(platform_name, '#666666')
            
            fig.add_trace(go.Bar(
                x=[row['category']],
                y=[row['value']],
                name=row['platform'],
                marker_color=bar_color,
                showlegend=False,
                hovertemplate='<b>%{x}</b><br>' +
                             'Profit Contribution: <b>$%{y:,.0f}</b><br>' +
                             '<i>After COGS and Ad Spend</i><extra></extra>'
            ))
        else:
            # Total bar
            fig.add_trace(go.Bar(
                x=[row['category']],
                y=[row['cumulative']],
                name='Total',
                marker_color=default_colors['total'],
                showlegend=False,
                hovertemplate='<b>Total Gross Profit</b><br>Value: <b>$%{y:,.0f}</b><extra></extra>'
            ))
    
    fig.update_layout(
        title='Gross Profit Attribution by Platform',
        title_x=0.5,
        xaxis_title="Platform Contribution",
        yaxis_title="Gross Profit Impact ($)",
        height=450,
        xaxis=dict(
            tickfont=dict(size=10),
            tickangle=0
        ),
        yaxis=dict(
            tickformat='$,.0f',
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            tickfont=dict(size=10)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_roas_comparison_chart(merged_df):
    """Create ROAS Comparison Horizontal Bar Chart - Thin bars with correct ROAS values"""
    from utils.data_loader import get_roas_by_platform_data
    
    roas_data = get_roas_by_platform_data(merged_df)
    
    if roas_data is None or len(roas_data) == 0:
        return None
    
    # Sort by ROAS ascending for horizontal bars (highest at top)
    roas_data = roas_data.sort_values('roas', ascending=True)
    
    fig = px.bar(
        roas_data,
        x='roas',
        y='platform',
        orientation='h',  # Horizontal bars
        title='Return on Ad Spend by Platform',
        color='platform',
        color_discrete_map=config.PLATFORM_COLORS
    )
    
    # Enhanced hover template with insights
    fig.update_traces(
        texttemplate='%{x:.2f}x', 
        textposition='outside',
        textfont_size=11,
        hovertemplate='<b>%{y} Platform</b><br>' +
                     'ROAS: <b>%{x:.2f}x</b><br>' +
                     'Revenue: <b>$%{customdata[0]:,.0f}</b><br>' +
                     'Total Spend: <b>$%{customdata[1]:,.0f}</b><br>' +
                     '<i>Higher ROAS = More Profitable</i><extra></extra>',
        customdata=list(zip(roas_data['total_revenue'], roas_data['total_spend']))
    )
    
    fig.update_layout(
        xaxis_title="ROAS Value (Revenue ÷ Spend)",
        yaxis_title="Platform",
        showlegend=False,
        height=400,  # Reduced height for thinner appearance
        title_x=0.5,
        xaxis=dict(
            tickformat='.2f',
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)'
        ),
        yaxis=dict(
            categoryorder='total ascending',
            tickfont=dict(size=12)
        ),
        # Reduce bar thickness
        bargap=0.6,  # Increase gap between bars to make them thinner
        margin=dict(l=80, r=50, t=60, b=50)  # Adjust margins
    )
    
    return fig

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
                f'<i>{platform} Weekly CPC Trend</i><extra></extra>',
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
                    width=3
                ),
                marker=dict(
                    size=8,
                    symbol='diamond'
                ),
                hovertemplate=
                '<b>%{fullData.name}</b><br>' +
                'Week of: %{x}<br>' +
                'Cost per Acquisition: $%{y:.2f}<br>' +
                f'<i>{platform} Weekly CPA Trend</i><extra></extra>',
                legendgroup=f'{platform}_CPA',
                showlegend=True
            )
        )
    
    # Update x-axis - REMOVED title_text AND showticklabels to hide x-axis values
    fig.update_xaxes(
        title_text="",  # No x-axis label
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128,128,128,0.2)',
        showticklabels=False  # Hide x-axis tick labels (dates)
    )
    
    # Single Y-axis
    fig.update_yaxes(
        title_text="Cost ($)",
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128,128,128,0.2)',
        tickformat='$,.2f',
        tickangle=0,
        tickfont=dict(size=10)
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
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(size=9)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        margin=dict(r=120)
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
                     '<i>Hover to compare performance</i><extra></extra>',
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