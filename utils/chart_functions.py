import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import config

def create_revenue_by_platform_chart(merged_df):
    """Create Revenue by Platform Bar Chart"""
    from utils.data_loader import get_revenue_by_platform_data
    
    revenue_data = get_revenue_by_platform_data(merged_df)
    
    if revenue_data is None or len(revenue_data) == 0:
        return None
    
    fig = px.bar(
        revenue_data,
        x='platform',
        y='total_revenue',
        title='Revenue by Platform',
        color='platform',
        color_discrete_map=config.PLATFORM_COLORS
    )
    
    # Clean hover template with white background
    fig.update_traces(
        texttemplate='$%{y:,.0f}', 
        textposition='outside',
        textfont_size=11,
        hovertemplate='<b>💰 %{x} Platform</b><br>' +
                     'Total Revenue: $%{y:,.0f}<br>' +
                     'Platform: %{x}<br>' +
                     'Platform revenue comparison<extra></extra>'
    )
    
    fig.update_layout(
        xaxis_title="Platform",
        yaxis_title="Total Revenue ($)",
        showlegend=False,
        height=260,
        title_x=0.5,
        xaxis=dict(
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            tickformat='$,.0f',
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            tickfont=dict(size=10)
        ),
        title_font=dict(size=12),
        # White background hover
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="black",
            font_size=12,
            font_family="Arial",
            font_color="black"
        )
    )
    
    return fig

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
        colorscale='Greens',
        text=heatmap_pivot.values,
        texttemplate="%{text:.0f}",
        textfont={"size": 11, "color": "black"},
        hovertemplate='<b>%{y}</b> on <b>%{x}</b><br>' + 
                     'Performance Score: <b>%{z:.0f}/100</b><br>' + 
                     'Higher score = Better performance<extra></extra>',
        colorbar=dict(
            title=dict(text="Performance<br>Score", font=dict(size=10)),
            tickfont=dict(size=9)
        )
    ))
    
    fig.update_layout(
        title='Campaign Tactic Effectiveness Matrix',
        title_x=0.5,
        title_y=0.98,  # FIXED: Position title at very top
        height=320,    # FIXED: Reduced height to accommodate title
        margin=dict(t=70, b=10, l=60, r=80),  # FIXED: Proper margins
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
        title_font=dict(size=14),  # FIXED: Smaller title font
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="black",
            font_size=12,
            font_family="Arial",
            font_color="black"
        )
    )
    
    return fig

def create_conversion_funnel_chart(merged_df):
    """Create Marketing Funnel Performance by Platform - NEW IMPROVED VERSION"""
    from utils.data_loader import get_conversion_funnel_data
    
    funnel_data = get_conversion_funnel_data(merged_df)
    
    if funnel_data is None or len(funnel_data) == 0:
        return None
    
    # Create subplot for multiple funnels side by side
    from plotly.subplots import make_subplots
    
    platforms = funnel_data['Platform'].unique()
    
    # Create subplots - one column per platform
    fig = make_subplots(
        rows=1, 
        cols=len(platforms),
        specs=[[{"type": "funnel"} for _ in platforms]],
        subplot_titles=[f"{platform} Funnel" for platform in platforms],
        horizontal_spacing=0.15
    )
    
    # Enhanced platform colors
    platform_colors = {
       'Facebook': '#d63a29',
       'Google': '#65ad52', 
       'TikTok': '#37b0c8'
    }
    
    stages = ['Impressions', 'Clicks', 'Orders', 'Revenue']
    
    # Create funnel for each platform
    for col_idx, platform in enumerate(platforms):
        platform_data = funnel_data[funnel_data['Platform'] == platform]
        
        # Prepare funnel data
        funnel_values = []
        funnel_labels = []
        hover_data = []
        conversion_rates = []
        
        # Calculate conversion rates between stages
        stage_values = {}
        for stage in stages:
            stage_data = platform_data[platform_data['Stage'] == stage]
            if len(stage_data) > 0:
                stage_values[stage] = stage_data['Value'].iloc[0]
        
        # Build funnel data with conversion rates
        for i, stage in enumerate(stages):
            if stage in stage_values:
                value = stage_values[stage]
                
                # Calculate conversion rate from previous stage
                if i == 0:
                    conv_rate = 100.0  # Impressions = 100%
                    rate_text = "100%"
                elif i == 1:  # Clicks
                    conv_rate = (value / stage_values['Impressions'] * 100) if stage_values['Impressions'] > 0 else 0
                    rate_text = f"{conv_rate:.2f}%"
                elif i == 2:  # Orders
                    conv_rate = (value / stage_values['Clicks'] * 100) if stage_values['Clicks'] > 0 else 0
                    rate_text = f"{conv_rate:.2f}%"
                else:  # Revenue
                    avg_order_value = value / stage_values['Orders'] if stage_values['Orders'] > 0 else 0
                    conv_rate = avg_order_value
                    rate_text = f"${avg_order_value:,.0f}/order"
                
                # Format values appropriately
                if stage == 'Revenue':
                    display_value = value / 1000  # Scale for visualization
                    label_text = f"{stage}<br>${value:,.0f}"
                else:
                    display_value = value
                    label_text = f"{stage}<br>{value:,.0f}"
                
                funnel_values.append(display_value)
                funnel_labels.append(label_text)
                conversion_rates.append(rate_text)
                
                # Hover data
                hover_data.append({
                    'stage': stage,
                    'value': value,
                    'rate': rate_text,
                    'platform': platform
                })
        
        # Add funnel trace
        fig.add_trace(
            go.Funnel(
                y=funnel_labels,
                x=funnel_values,
                name=platform,
                marker=dict(
                    color=platform_colors.get(platform, '#666666'),
                    line=dict(color='white', width=3)
                ),
                textinfo="value+percent initial",
                textfont=dict(size=11, color='white', family='Arial Black'),
                # Enhanced hover template
                hovertemplate=(
                    '<b>🎯 %{fullData.name} Platform</b><br>' +
                    '<b>Stage:</b> %{customdata[0]}<br>' +
                    '<b>Volume:</b> %{customdata[1]:,.0f}<br>' +
                    '<b>Conversion Rate:</b> %{customdata[2]}<br>' +
                    '<b>Performance:</b> %{percent}<br>' +
                    '<i>Click to analyze bottlenecks</i><extra></extra>'
                ),
                customdata=[[hd['stage'], hd['value'], hd['rate']] for hd in hover_data],
                textposition='inside'
            ),
            row=1, col=col_idx+1
        )
    
    # Update layout with enhanced styling
    fig.update_layout(
        title={
            'text': '""Marketing Funnel Performance by Platform""',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 12, 'family': 'Arial Black', 'color': '#2c3e50'}
        },
        height=450,
        margin=dict(t=80, b=60, l=40, r=40),
        showlegend=False,  # Individual titles show platform names
        font=dict(family="Arial", size=12),
        # White background hover
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="black",
            font_size=13,
            font_family="Arial",
            font_color="black"
        ),
        # Enhanced subplot titles
        annotations=[
            dict(
                text=f"<b>{platform}</b>",
                x=(i + 0.5) / len(platforms),
                y=1.02,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=14, color=platform_colors.get(platform, '#666666'), family='Arial Black')
            ) for i, platform in enumerate(platforms)
        ]
    )
    
    # Add conversion rate annotations below each funnel
    for col_idx, platform in enumerate(platforms):
        platform_data = funnel_data[funnel_data['Platform'] == platform]
        
        # Calculate overall funnel efficiency
        impressions = platform_data[platform_data['Stage'] == 'Impressions']['Value'].iloc[0] if len(platform_data[platform_data['Stage'] == 'Impressions']) > 0 else 1
        orders = platform_data[platform_data['Stage'] == 'Orders']['Value'].iloc[0] if len(platform_data[platform_data['Stage'] == 'Orders']) > 0 else 0
        
        overall_conversion = (orders / impressions * 100) if impressions > 0 else 0
        
        fig.add_annotation(
            text=f"<b>Overall Conversion: {overall_conversion:.3f}%</b>",
            x=(col_idx + 0.5) / len(platforms),
            y=-0.12,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=11, color='#34495e', family='Arial'),
            bgcolor="rgba(236, 240, 241, 0.8)",
            bordercolor="#bdc3c7",
            borderwidth=1
        )
    
    return fig

def create_platform_revenue_pie_chart(merged_df):
    """Create Platform Revenue Distribution Pie Chart with ROAS context"""
    from utils.data_loader import get_revenue_by_platform_data, get_roas_by_platform_data
    
    revenue_data = get_revenue_by_platform_data(merged_df)
    roas_data = get_roas_by_platform_data(merged_df)
    
    if revenue_data is None or len(revenue_data) == 0:
        return None
    
    # Merge revenue and ROAS data
    combined_data = revenue_data.merge(roas_data[['platform', 'roas', 'total_spend']], on='platform', how='left')
    
    # Calculate percentages
    total_revenue = combined_data['total_revenue'].sum()
    combined_data['percentage'] = (combined_data['total_revenue'] / total_revenue * 100)
    
    fig = px.pie(
        combined_data,
        values='total_revenue',
        names='platform',
        title='Platform Revenue Distribution and ROAS Performance',
        color='platform',
        color_discrete_map=config.PLATFORM_COLORS
    )
    
    # Clean hover template
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=12,
        hovertemplate='<b>💰 %{label} Platform</b><br>' +
                     'Revenue: $%{value:,.0f}<br>' +
                     'Share: %{percent}<br>' +
                     'ROAS: %{customdata[0]:.2f}x<br>' +
                     'Ad Spend: $%{customdata[1]:,.0f}<br>' +
                     'Revenue efficiency analysis<extra></extra>',
        customdata=list(zip(combined_data['roas'].fillna(0), combined_data['total_spend'].fillna(0)))
    )
    
    fig.update_layout(
        title_x=0.5,
        height=320,
        margin=dict(t=70, b=10, l=20, r=20),
        title_font=dict(size=14),
        font=dict(size=11),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(size=10)
        ),
        # White background hover
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="black",
            font_size=12,
            font_family="Arial",
            font_color="black"
        )
    )
    
    return fig

def create_engagement_metrics_chart(merged_df):
    """Create Reach and Engagement Metrics Comparison - Multiple Metrics Chart"""
    from utils.data_loader import get_engagement_metrics_data
    
    engagement_data = get_engagement_metrics_data(merged_df)
    
    if engagement_data is None or len(engagement_data) == 0:
        return None
    
    # Create subplots with secondary y-axis
    fig = make_subplots(
        specs=[[{"secondary_y": True}]]
    )
    
    platforms = engagement_data['platform'].unique()
    
    # Colors for different metrics
    impression_colors = {
        'Facebook': '#d63a29',
        'Google': '#65ad52', 
        'TikTok': '#37b0c8'
    }
    
    click_colors = {
        'Facebook': '#42A5F5',
        'Google': '#66BB6A',
        'TikTok': '#AB47BC'
    }
    
    # Add Impressions bars (primary y-axis)
    fig.add_trace(
        go.Bar(
            x=engagement_data['platform'],
            y=engagement_data['total_impressions'],
            name='Impressions',
            marker_color=[impression_colors[p] for p in engagement_data['platform']],
            yaxis='y',
            offsetgroup=1,
            hovertemplate='<b>👁️ %{x} Impressions</b><br>' +
                         'Total Impressions: %{y:,.0f}<br>' +
                         'Platform: %{x}<br>' +
                         'Reach Metric: Primary KPI<br>' +
                         'Total audience reached<extra></extra>'
        ),
        secondary_y=False
    )
    
    # Add Clicks bars (primary y-axis, different offset)
    fig.add_trace(
        go.Bar(
            x=engagement_data['platform'],
            y=engagement_data['total_clicks'],
            name='Clicks',
            marker_color=[click_colors[p] for p in engagement_data['platform']],
            yaxis='y',
            offsetgroup=2,
            hovertemplate='<b>👆 %{x} Clicks</b><br>' +
                         'Total Clicks: %{y:,.0f}<br>' +
                         'Platform: %{x}<br>' +
                         'Engagement: Click Volume<br>' +
                         'User interaction count<extra></extra>'
        ),
        secondary_y=False
    )
    
    # Add CTR line (secondary y-axis)
    fig.add_trace(
        go.Scatter(
            x=engagement_data['platform'],
            y=engagement_data['ctr_percentage'],
            mode='lines+markers',
            name='CTR %',
            line=dict(color='#FF6B35', width=4),
            marker=dict(size=12, color='#FF6B35', symbol='diamond'),
            yaxis='y2',
            hovertemplate='<b>📈 %{x} CTR</b><br>' +
                         'Click-Through Rate: %{y:.2f}%<br>' +
                         'Platform: %{x}<br>' +
                         'Efficiency: Engagement Rate<br>' +
                         'Clicks per 100 impressions<extra></extra>'
        ),
        secondary_y=True
    )
    
    # Update layout
    fig.update_layout(
        title='Reach and Engagement Metrics Comparison',
        title_x=0.5,
        height=320,
        margin=dict(t=70, b=10, l=20, r=20),
        title_font=dict(size=14),
        xaxis_title="Platform",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        ),
        hovermode='x unified',
        # White background hover
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="black",
            font_size=12,
            font_family="Arial",
            font_color="black"
        )
    )
    
    # Update y-axes
    fig.update_yaxes(
        title_text="Volume (Impressions & Clicks)",
        secondary_y=False,
        tickformat=',.0f',
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128,128,128,0.2)'
    )
    
    fig.update_yaxes(
        title_text="CTR Percentage (%)",
        secondary_y=True,
        tickformat='.2f',
        showgrid=False
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
    
    # Clean hover template
    fig.update_traces(
        hovertemplate='<b>%{fullData.name}</b><br>' +
                     'CAC: $%{x:.2f}<br>' +
                     'Estimated CLV: $%{y:.2f}<br>' +
                     'New Customers: %{customdata:,.0f}<br>' +
                     'CLV should be 3x+ higher than CAC<extra></extra>',
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
        margin=dict(r=100),
        # White background hover
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="black",
            font_size=12,
            font_family="Arial",
            font_color="black"
        )
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
                             'Profit Contribution: $%{y:,.0f}<br>' +
                             'After COGS and Ad Spend<extra></extra>'
            ))
        else:
            # Total bar
            fig.add_trace(go.Bar(
                x=[row['category']],
                y=[row['cumulative']],
                name='Total',
                marker_color=default_colors['total'],
                showlegend=False,
                hovertemplate='<b>Total Gross Profit</b><br>Value: $%{y:,.0f}<extra></extra>'
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
        paper_bgcolor='rgba(0,0,0,0)',
        # White background hover
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="black",
            font_size=12,
            font_family="Arial",
            font_color="black"
        )
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
    
    # Clean hover template
    fig.update_traces(
        texttemplate='%{x:.2f}x', 
        textposition='outside',
        textfont_size=11,
        hovertemplate='<b>%{y} Platform</b><br>' +
                     'ROAS: %{x:.2f}x<br>' +
                     'Revenue: $%{customdata[0]:,.0f}<br>' +
                     'Total Spend: $%{customdata[1]:,.0f}<br>' +
                     'Higher ROAS = More Profitable<extra></extra>',
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
        margin=dict(l=80, r=50, t=60, b=50),  # Adjust margins
        # White background hover
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="black",
            font_size=12,
            font_family="Arial",
            font_color="black"
        )
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
        'Facebook': '#d63a29',
        'Google': '#65ad52', 
        'TikTok': '#37b0c8'
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
                f'{platform} Weekly CPC Trend<extra></extra>',
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
                f'{platform} Weekly CPA Trend<extra></extra>',
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
        title='Weekly Campaign Efficiency Trends',
        title_x=0.5,
        height=320,
        margin=dict(t=70, b=40, l=50, r=50),
        title_font=dict(size=14),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=9)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        # White background hover
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="black",
            font_size=12,
            font_family="Arial",
            font_color="black"
        )
    )
    
    return fig

# Alternative function names for compatibility
def create_platform_performance_pie_chart(merged_df):
    """Alternative name for the pie chart - ensuring compatibility"""
    return create_platform_revenue_pie_chart(merged_df)

def create_engagement_performance_chart(merged_df):
    """Alternative name for engagement chart - ensuring compatibility"""
    return create_engagement_metrics_chart(merged_df)
