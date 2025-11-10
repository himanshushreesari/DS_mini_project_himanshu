"""
Geographic Insights Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_cleaned_data, get_regions, get_states, get_districts
from utils.visualizations import COLORS

st.set_page_config(page_title="Geographic Insights", page_icon="🗺️", layout="wide")

# Title
st.title("🗺️ Geographic Insights")
st.markdown("---")

# Load data
df = load_cleaned_data()

if df is None:
    st.error("Unable to load data. Please check if the data file exists.")
    st.stop()

# Overview Metrics
st.header("📊 Geographic Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="padding: 1rem; background: linear-gradient(135deg, {COLORS['primary']} 0%, #5a67d8 100%); 
                border-radius: 10px; color: white; text-align: center;">
        <h4>Total States</h4>
        <p style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">
            {df['state_name'].nunique()}
        </p>
        <p style="font-size: 0.9rem;">Across India</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="padding: 1rem; background: linear-gradient(135deg, {COLORS['success']} 0%, #059669 100%); 
                border-radius: 10px; color: white; text-align: center;">
        <h4>Total Districts</h4>
        <p style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">
            {df['district_name'].nunique()}
        </p>
        <p style="font-size: 0.9rem;">Coverage Area</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="padding: 1rem; background: linear-gradient(135deg, {COLORS['warning']} 0%, #d97706 100%); 
                border-radius: 10px; color: white; text-align: center;">
        <h4>Total Regions</h4>
        <p style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">
            {df['region'].nunique()}
        </p>
        <p style="font-size: 0.9rem;">Geographic Zones</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    total_deposits = df['deposit_amount'].sum()
    st.markdown(f"""
    <div style="padding: 1rem; background: linear-gradient(135deg, {COLORS['secondary']} 0%, #7c3aed 100%); 
                border-radius: 10px; color: white; text-align: center;">
        <h4>Total Deposits</h4>
        <p style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">
            ₹{total_deposits/1e9:.1f}B
        </p>
        <p style="font-size: 0.9rem;">Nationwide</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Regional Analysis
st.header("🌍 Regional Performance")

col1, col2 = st.columns([3, 2])

with col1:
    # Regional aggregate
    regional_data = df.groupby('region').agg({
        'deposit_amount': ['sum', 'mean', 'count'],
        'no_of_offices': 'sum',
        'no_of_accounts': 'sum'
    }).round(2)
    
    regional_data.columns = ['Total Deposits', 'Avg Deposits', 'Records', 'Total Offices', 'Total Accounts']
    regional_data = regional_data.reset_index()
    regional_data = regional_data.sort_values('Total Deposits', ascending=False)
    
    # Bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=regional_data['region'],
        y=regional_data['Total Deposits'],
        marker_color=COLORS['primary'],
        text=regional_data['Total Deposits'].apply(lambda x: f'₹{x/1e9:.1f}B'),
        textposition='outside',
        name='Total Deposits'
    ))
    
    fig.update_layout(
        title="Total Deposits by Region",
        xaxis_title="Region",
        yaxis_title="Total Deposits (₹)",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### Regional Statistics")
    
    # Display table
    display_df = regional_data.copy()
    display_df['Total Deposits'] = display_df['Total Deposits'].apply(lambda x: f'₹{x/1e6:.1f}M')
    display_df['Avg Deposits'] = display_df['Avg Deposits'].apply(lambda x: f'₹{x:,.0f}')
    display_df['Total Offices'] = display_df['Total Offices'].apply(lambda x: f'{int(x):,}')
    display_df['Total Accounts'] = display_df['Total Accounts'].apply(lambda x: f'{int(x):,}')
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# Regional Comparison Tool
st.markdown("---")
st.header("📊 Regional Comparison Tool")

regions = get_regions()
selected_regions = st.multiselect(
    "Select regions to compare:",
    options=regions,
    default=regions[:3] if len(regions) >= 3 else regions
)

if selected_regions:
    comparison_df = df[df['region'].isin(selected_regions)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Deposits comparison
        deposits_by_region = comparison_df.groupby('region')['deposit_amount'].sum().reset_index()
        
        fig = px.pie(
            deposits_by_region,
            values='deposit_amount',
            names='region',
            title='Deposit Distribution Across Selected Regions',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Infrastructure comparison
        infra_comparison = comparison_df.groupby('region').agg({
            'no_of_offices': 'sum',
            'no_of_accounts': 'sum'
        }).reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Offices',
            x=infra_comparison['region'],
            y=infra_comparison['no_of_offices'],
            marker_color=COLORS['primary']
        ))
        
        fig.add_trace(go.Bar(
            name='Accounts',
            x=infra_comparison['region'],
            y=infra_comparison['no_of_accounts'],
            marker_color=COLORS['success']
        ))
        
        fig.update_layout(
            title='Infrastructure Comparison',
            barmode='group',
            xaxis_title='Region',
            yaxis_title='Count',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Efficiency metrics
    st.subheader("Efficiency Metrics Comparison")
    
    efficiency_df = comparison_df.groupby('region').agg({
        'deposit_amount': 'sum',
        'no_of_offices': 'sum',
        'no_of_accounts': 'sum'
    })
    
    efficiency_df['Deposit per Office'] = (efficiency_df['deposit_amount'] / efficiency_df['no_of_offices']).round(2)
    efficiency_df['Deposit per Account'] = (efficiency_df['deposit_amount'] / efficiency_df['no_of_accounts']).round(2)
    efficiency_df['Accounts per Office'] = (efficiency_df['no_of_accounts'] / efficiency_df['no_of_offices']).round(2)
    
    efficiency_display = efficiency_df[['Deposit per Office', 'Deposit per Account', 'Accounts per Office']].reset_index()
    
    st.dataframe(
        efficiency_display.style.format({
            'Deposit per Office': '₹{:,.0f}',
            'Deposit per Account': '₹{:,.0f}',
            'Accounts per Office': '{:.1f}'
        }),
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

# State-Level Analysis
st.header("🏛️ State-Level Analysis")

col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("Top 15 States by Deposits")
    
    state_deposits = df.groupby('state_name')['deposit_amount'].sum().sort_values(ascending=False).head(15)
    
    fig = go.Figure(go.Bar(
        x=state_deposits.values,
        y=state_deposits.index,
        orientation='h',
        marker_color=COLORS['secondary'],
        text=[f'₹{x/1e6:.1f}M' for x in state_deposits.values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Top 15 States",
        xaxis_title="Total Deposits (₹)",
        yaxis_title="State",
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("State Performance Details")
    
    state_details = df.groupby('state_name').agg({
        'deposit_amount': ['sum', 'mean'],
        'no_of_offices': 'sum',
        'no_of_accounts': 'sum',
        'district_name': 'nunique'
    }).round(2)
    
    state_details.columns = ['Total Deposits', 'Avg Deposits', 'Offices', 'Accounts', 'Districts']
    state_details = state_details.sort_values('Total Deposits', ascending=False).head(15)
    
    # Create heatmap
    normalized_data = state_details.copy()
    for col in normalized_data.columns:
        normalized_data[col] = (normalized_data[col] - normalized_data[col].min()) / (normalized_data[col].max() - normalized_data[col].min())
    
    fig = go.Figure(data=go.Heatmap(
        z=normalized_data.values.T,
        x=normalized_data.index,
        y=normalized_data.columns,
        colorscale='Blues',
        text=state_details.values.T,
        texttemplate='%{text:.0f}',
        textfont={"size": 10},
        colorbar=dict(title="Normalized<br>Score")
    ))
    
    fig.update_layout(
        title="State Performance Heatmap (Top 15)",
        height=500,
        xaxis={'side': 'bottom'},
        yaxis={'side': 'left'}
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# District-Level Analysis
st.header("📍 District-Level Analysis")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("District Finder")
    
    # Search district
    search_district = st.text_input("Search for a district:", "")
    
    if search_district:
        matching_districts = df[df['district_name'].str.contains(search_district, case=False, na=False)]
        
        if not matching_districts.empty:
            st.success(f"Found {len(matching_districts)} matching records")
            
            # Show district stats
            district_stats = matching_districts.groupby('district_name').agg({
                'deposit_amount': 'sum',
                'no_of_offices': 'sum',
                'no_of_accounts': 'sum',
                'state_name': 'first',
                'region': 'first'
            }).reset_index()
            
            for _, row in district_stats.iterrows():
                with st.expander(f"📍 {row['district_name']} ({row['state_name']})"):
                    st.write(f"**Region:** {row['region']}")
                    st.write(f"**Total Deposits:** ₹{row['deposit_amount']:,.0f}")
                    st.write(f"**Offices:** {int(row['no_of_offices']):,}")
                    st.write(f"**Accounts:** {int(row['no_of_accounts']):,}")
                    
                    if row['no_of_offices'] > 0:
                        st.write(f"**Deposit per Office:** ₹{row['deposit_amount']/row['no_of_offices']:,.0f}")
        else:
            st.warning("No matching districts found")
    else:
        st.info("Enter a district name to search")

with col2:
    st.subheader("Top & Bottom Performers")
    
    tab1, tab2 = st.tabs(["Top 10 Districts", "Bottom 10 Districts"])
    
    with tab1:
        top_districts = df.groupby('district_name').agg({
            'deposit_amount': 'sum',
            'state_name': 'first'
        }).sort_values('deposit_amount', ascending=False).head(10)
        
        fig = go.Figure(go.Bar(
            x=top_districts['deposit_amount'],
            y=[f"{district} ({state})" for district, state in zip(top_districts.index, top_districts['state_name'])],
            orientation='h',
            marker_color=COLORS['success'],
            text=top_districts['deposit_amount'].apply(lambda x: f'₹{x/1e6:.1f}M'),
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Top 10 Districts by Total Deposits",
            xaxis_title="Total Deposits (₹)",
            height=400,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        bottom_districts = df.groupby('district_name').agg({
            'deposit_amount': 'sum',
            'state_name': 'first'
        }).sort_values('deposit_amount', ascending=True).head(10)
        
        fig = go.Figure(go.Bar(
            x=bottom_districts['deposit_amount'],
            y=[f"{district} ({state})" for district, state in zip(bottom_districts.index, bottom_districts['state_name'])],
            orientation='h',
            marker_color=COLORS['danger'],
            text=bottom_districts['deposit_amount'].apply(lambda x: f'₹{x/1e3:.1f}K'),
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Bottom 10 Districts by Total Deposits",
            xaxis_title="Total Deposits (₹)",
            height=400,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Infrastructure Efficiency by Geography
st.header("⚡ Infrastructure Efficiency by Geography")

efficiency_metric = st.selectbox(
    "Select efficiency metric:",
    ["Accounts per Office", "Deposit per Office", "Deposit per Account"]
)

if efficiency_metric == "Accounts per Office":
    df['metric'] = df['no_of_accounts'] / df['no_of_offices'].replace(0, 1)
    metric_label = "Accounts/Office"
elif efficiency_metric == "Deposit per Office":
    df['metric'] = df['deposit_amount'] / df['no_of_offices'].replace(0, 1)
    metric_label = "₹/Office"
else:
    df['metric'] = df['deposit_amount'] / df['no_of_accounts'].replace(0, 1)
    metric_label = "₹/Account"

col1, col2 = st.columns(2)

with col1:
    # By Region
    region_efficiency = df.groupby('region')['metric'].mean().sort_values(ascending=False)
    
    fig = go.Figure(go.Bar(
        x=region_efficiency.index,
        y=region_efficiency.values,
        marker_color=COLORS['primary'],
        text=[f'{x:,.1f}' for x in region_efficiency.values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f"{efficiency_metric} by Region",
        xaxis_title="Region",
        yaxis_title=metric_label,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # By Population Group
    pop_efficiency = df.groupby('population_group')['metric'].mean().sort_values(ascending=False)
    
    fig = go.Figure(go.Bar(
        x=pop_efficiency.index,
        y=pop_efficiency.values,
        marker_color=COLORS['success'],
        text=[f'{x:,.1f}' for x in pop_efficiency.values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f"{efficiency_metric} by Population Group",
        xaxis_title="Population Group",
        yaxis_title=metric_label,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Top states by efficiency
st.subheader(f"Top 15 States by {efficiency_metric}")

state_efficiency = df.groupby('state_name')['metric'].mean().sort_values(ascending=False).head(15)

fig = go.Figure(go.Bar(
    x=state_efficiency.values,
    y=state_efficiency.index,
    orientation='h',
    marker_color=COLORS['warning'],
    text=[f'{x:,.1f}' for x in state_efficiency.values],
    textposition='outside'
))

fig.update_layout(
    title=f"Top 15 States by {efficiency_metric}",
    xaxis_title=metric_label,
    yaxis_title="State",
    height=500,
    yaxis={'categoryorder': 'total ascending'}
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Key Insights
st.header("💡 Geographic Insights")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    ### 🌟 Key Observations
    
    **Regional Patterns:**
    - Deposits are unevenly distributed across regions
    - Metropolitan regions show higher deposit concentrations
    - Rural areas have more coverage but lower deposit volumes
    
    **State-Level Insights:**
    - Top 15 states account for majority of deposits
    - Infrastructure density varies significantly
    - Efficiency metrics differ across states
    
    **District Analysis:**
    - Urban districts outperform rural counterparts
    - Infrastructure efficiency is location-dependent
    - Opportunities exist in underserved districts
    """)

with col2:
    st.success("""
    ### 🎯 Strategic Recommendations
    
    **For Expansion:**
    - Target high-efficiency districts for replication
    - Focus on underserved regions with potential
    - Balance infrastructure across geographies
    
    **For Optimization:**
    - Improve efficiency in low-performing areas
    - Redistribute resources based on demand
    - Benchmark against top performers
    
    **For Policy:**
    - Address regional disparities
    - Incentivize rural banking
    - Promote balanced development
    """)

# Footer
st.markdown("---")
st.markdown("*Use the filters and tools above to explore geographic patterns in detail.*")
