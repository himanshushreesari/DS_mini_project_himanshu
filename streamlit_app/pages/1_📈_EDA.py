"""
EDA Page - Exploratory Data Analysis
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_cleaned_data, filter_data, get_summary_stats
from utils.visualizations import (
    create_distribution_plot, create_correlation_heatmap,
    create_population_group_chart, create_regional_analysis,
    create_box_plot_by_category, create_top_states_chart
)

st.set_page_config(page_title="EDA - Deposits Analysis", page_icon="📈", layout="wide")

# Title
st.title("📈 Exploratory Data Analysis")
st.markdown("---")

# Load data
df = load_cleaned_data()

if df is None:
    st.error("Unable to load data. Please check if the data files exist in the correct directory.")
    st.stop()

# Sidebar filters
st.sidebar.header("🔍 Filters")

population_filter = st.sidebar.selectbox(
    "Population Group",
    ["All"] + df['population_group'].unique().tolist()
)

region_filter = st.sidebar.selectbox(
    "Region",
    ["All"] + sorted(df['region'].unique().tolist())
)

state_filter = st.sidebar.selectbox(
    "State",
    ["All"] + sorted(df['state_name'].unique().tolist())
)

# Apply filters
filtered_df = filter_data(
    df,
    population_group=population_filter if population_filter != "All" else None,
    region=region_filter if region_filter != "All" else None,
    state=state_filter if state_filter != "All" else None
)

# Summary Statistics
st.header("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

stats = get_summary_stats(filtered_df)

with col1:
    st.metric("Total Records", f"{stats['total_records']:,}")
    
with col2:
    st.metric("Total Deposits", f"₹{stats['total_deposits']:,.0f}")
    
with col3:
    st.metric("Total Offices", f"{stats['total_offices']:,}")
    
with col4:
    st.metric("Total Accounts", f"{stats['total_accounts']:,}")

st.markdown("---")

# Data table
with st.expander("📋 View Raw Data", expanded=False):
    st.dataframe(filtered_df, use_container_width=True, height=400)
    
    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_deposits_data.csv",
        mime="text/csv"
    )

st.markdown("---")

# Statistical Summary
st.header("📉 Statistical Summary")

tab1, tab2 = st.tabs(["Numerical Features", "Categorical Features"])

with tab1:
    numerical_cols = ['no_of_offices', 'no_of_accounts', 'deposit_amount']
    st.dataframe(filtered_df[numerical_cols].describe(), use_container_width=True)
    
with tab2:
    categorical_cols = ['state_name', 'region', 'population_group', 'district_name']
    
    for col in categorical_cols:
        with st.expander(f"📌 {col.replace('_', ' ').title()}", expanded=False):
            value_counts = filtered_df[col].value_counts().head(10)
            st.dataframe(value_counts, use_container_width=True)

st.markdown("---")

# Distributions
st.header("📊 Distribution Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    fig = create_distribution_plot(filtered_df, 'no_of_offices', 'Number of Offices Distribution')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = create_distribution_plot(filtered_df, 'no_of_accounts', 'Number of Accounts Distribution')
    st.plotly_chart(fig, use_container_width=True)

with col3:
    fig = create_distribution_plot(filtered_df, 'deposit_amount', 'Deposit Amount Distribution')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Correlation Analysis
st.header("🔗 Correlation Analysis")

col1, col2 = st.columns([1, 1])

with col1:
    numerical_features = ['no_of_offices', 'no_of_accounts', 'deposit_amount']
    fig = create_correlation_heatmap(filtered_df, numerical_features)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### Key Correlations")
    
    corr = filtered_df[numerical_features].corr()
    
    st.success(f"**Offices ↔ Accounts:** {corr.loc['no_of_offices', 'no_of_accounts']:.3f}")
    st.info(f"**Offices ↔ Deposits:** {corr.loc['no_of_offices', 'deposit_amount']:.3f}")
    st.warning(f"**Accounts ↔ Deposits:** {corr.loc['no_of_accounts', 'deposit_amount']:.3f}")
    
    st.markdown("---")
    
    st.markdown("""
    **Insights:**
    - Very strong positive correlation between offices and accounts (0.91+)
    - Strong positive correlation between accounts and deposits (0.79+)
    - More banking infrastructure → More accounts → Higher deposits
    """)

st.markdown("---")

# Population Group Analysis
st.header("🌆 Population Group Analysis")

fig = create_population_group_chart(filtered_df)
st.plotly_chart(fig, use_container_width=True)

# Detailed stats by population group
st.markdown("### Statistics by Population Group")
pop_stats = filtered_df.groupby('population_group').agg({
    'deposit_amount': ['count', 'sum', 'mean', 'median'],
    'no_of_offices': 'sum',
    'no_of_accounts': 'sum'
}).round(2)

pop_stats.columns = ['Count', 'Total Deposits', 'Avg Deposits', 'Median Deposits', 'Total Offices', 'Total Accounts']
st.dataframe(pop_stats, use_container_width=True)

st.markdown("---")

# Regional Analysis
st.header("🗺️ Regional Analysis")

fig = create_regional_analysis(filtered_df)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Deposit Analysis by Category
st.header("💰 Deposit Analysis by Category")

col1, col2 = st.columns(2)

with col1:
    fig = create_box_plot_by_category(filtered_df, 'deposit_amount', 'population_group')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = create_box_plot_by_category(filtered_df, 'deposit_amount', 'region')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Top States
st.header("🏆 Top Performing States")

fig = create_top_states_chart(filtered_df, top_n=15)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Footer
st.info("💡 **Tip:** Use the filters in the sidebar to drill down into specific population groups, regions, or states!")
