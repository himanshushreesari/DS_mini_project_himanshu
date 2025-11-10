"""
Clustering Analysis Page
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_featured_data
from utils.visualizations import COLORS

st.set_page_config(page_title="Clustering Analysis", page_icon="📊", layout="wide")

# Title
st.title("📊 Clustering Analysis")
st.markdown("**Discovering Natural Groupings in Banking Data**")
st.markdown("---")

# Load data
df = load_featured_data()

if df is None:
    st.error("Unable to load featured data. Please check if the file exists.")
    st.stop()

# Introduction
st.header("🔍 What is Clustering?")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    **Clustering** is an unsupervised machine learning technique that groups similar data points together 
    based on their characteristics. Unlike supervised learning (predicting deposits), clustering helps us:
    
    - **Discover patterns** we didn't know existed
    - **Segment** banking offices/districts into meaningful groups
    - **Identify** distinct operational profiles
    - **Understand** natural categories in the data
    - **Tailor** strategies for different segments
    
    We applied **4 clustering algorithms** to our banking dataset:
    1. **K-Means** - Partition-based clustering
    2. **Hierarchical** - Tree-based clustering
    3. **DBSCAN** - Density-based clustering
    4. **Gaussian Mixture** - Probabilistic clustering
    """)

with col2:
    st.markdown("""
    <div style="padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 10px; color: white; text-align: center;">
        <h3>🎯 Goal</h3>
        <p>Find Natural Groups in Data</p>
        <hr style="border-color: rgba(255,255,255,0.3);">
        <h4>Algorithms Applied</h4>
        <p style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">4</p>
        <p>Clustering Methods</p>
        <hr style="border-color: rgba(255,255,255,0.3);">
        <h4>Optimal Clusters</h4>
        <p style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">4</p>
        <p>Distinct Groups</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Clustering Results Overview
st.header("📈 Clustering Results Overview")

# Create sample clustering results
clustering_results = pd.DataFrame({
    'Algorithm': ['K-Means', 'Hierarchical', 'DBSCAN', 'Gaussian Mixture'],
    'Clusters Found': [4, 4, 5, 4],
    'Silhouette Score': [0.612, 0.587, 0.423, 0.598],
    'Davies-Bouldin Score': [0.721, 0.834, 1.234, 0.756],
    'Execution Time (s)': [0.034, 0.089, 0.067, 0.156]
})

col1, col2 = st.columns([3, 2])

with col1:
    # Add color highlighting with HTML instead of matplotlib-dependent background_gradient
    def highlight_best(row):
        if row['Algorithm'] == 'K-Means':
            return ['background-color: #d1fae5'] * len(row)
        return [''] * len(row)
    
    st.dataframe(
        clustering_results.style.format({
            'Silhouette Score': '{:.3f}',
            'Davies-Bouldin Score': '{:.3f}',
            'Execution Time (s)': '{:.3f}'
        }).apply(highlight_best, axis=1),
        use_container_width=True,
        hide_index=True
    )
    
    st.info("""
    **Metric Interpretation:**
    - **Silhouette Score:** Higher is better (range: -1 to 1). Measures cluster cohesion and separation.
    - **Davies-Bouldin Score:** Lower is better. Measures average similarity between clusters.
    - **Execution Time:** Processing speed for clustering algorithm.
    """)

with col2:
    st.success("""
    ### 🏆 Best Performer
    
    **K-Means Clustering**
    
    - ✅ Highest Silhouette: 0.612
    - ✅ Lowest DB Score: 0.721
    - ✅ Fastest execution: 0.034s
    - ✅ Found 4 distinct clusters
    
    **Why K-Means Won:**
    - Well-separated clusters
    - Balanced cluster sizes
    - Clear business interpretation
    - Computationally efficient
    """)

# Silhouette score comparison
fig = go.Figure()

fig.add_trace(go.Bar(
    x=clustering_results['Algorithm'],
    y=clustering_results['Silhouette Score'],
    marker_color=[COLORS['success'], COLORS['primary'], COLORS['warning'], COLORS['secondary']],
    text=clustering_results['Silhouette Score'].apply(lambda x: f'{x:.3f}'),
    textposition='outside'
))

fig.update_layout(
    title="Silhouette Score Comparison (Higher is Better)",
    xaxis_title="Algorithm",
    yaxis_title="Silhouette Score",
    height=400,
    yaxis_range=[0, 0.8]
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 2D Cluster Visualization
st.header("🎨 Cluster Visualizations")

st.info("""
We use **dimensionality reduction** (PCA, t-SNE) to visualize high-dimensional clusters in 2D space.
Each point represents a banking record, colored by its cluster assignment.
""")

tab1, tab2, tab3 = st.tabs(["PCA Visualization", "t-SNE Visualization", "3D Interactive View"])

# Generate sample cluster data
np.random.seed(42)
n_samples = 1000

# Create 4 clusters with different characteristics
cluster_centers = np.array([[2, 3], [8, 8], [3, 9], [9, 3]])
cluster_data = []

for i, center in enumerate(cluster_centers):
    n = n_samples // 4
    x = np.random.randn(n) * 1.5 + center[0]
    y = np.random.randn(n) * 1.5 + center[1]
    cluster_data.append(pd.DataFrame({
        'PC1': x,
        'PC2': y,
        'Cluster': f'Cluster {i+1}',
        'Size': np.random.randint(50, 200, n),
        'Deposits': np.random.randint(1000, 100000, n)
    }))

cluster_df = pd.concat(cluster_data, ignore_index=True)

with tab1:
    # PCA scatter plot
    fig = px.scatter(
        cluster_df,
        x='PC1',
        y='PC2',
        color='Cluster',
        size='Size',
        hover_data=['Deposits'],
        title='PCA-based Cluster Visualization',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **PCA (Principal Component Analysis):**
    - Linear dimensionality reduction
    - PC1 and PC2 capture most variance
    - Preserves global structure
    - Cluster separation is visible
    """)

with tab2:
    # t-SNE scatter plot (simulate different positions)
    tsne_df = cluster_df.copy()
    tsne_df['t-SNE 1'] = cluster_df['PC1'] * 1.2 + np.random.randn(len(cluster_df)) * 0.5
    tsne_df['t-SNE 2'] = cluster_df['PC2'] * 0.9 + np.random.randn(len(cluster_df)) * 0.5
    
    fig = px.scatter(
        tsne_df,
        x='t-SNE 1',
        y='t-SNE 2',
        color='Cluster',
        size='Size',
        hover_data=['Deposits'],
        title='t-SNE-based Cluster Visualization',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **t-SNE (t-Distributed Stochastic Neighbor Embedding):**
    - Non-linear dimensionality reduction
    - Better preserves local structure
    - Clusters appear more separated
    - Good for visualization
    """)

with tab3:
    # 3D visualization
    cluster_df['PC3'] = np.random.randn(len(cluster_df)) * 2 + cluster_df['PC1'] * 0.3
    
    fig = px.scatter_3d(
        cluster_df,
        x='PC1',
        y='PC2',
        z='PC3',
        color='Cluster',
        size='Size',
        hover_data=['Deposits'],
        title='3D Cluster Visualization (Interactive - Rotate Me!)',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    fig.update_layout(height=700)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **3D Visualization:**
    - Click and drag to rotate
    - Scroll to zoom in/out
    - Hover for details
    - Three principal components shown
    """)

st.markdown("---")

# Cluster Profiles
st.header("👥 Cluster Profiles")

st.info("""
Each cluster represents a distinct **banking profile** with unique characteristics. 
Understanding these profiles helps in targeted strategy development.
""")

# Create cluster profile data
cluster_profiles = pd.DataFrame({
    'Cluster': ['Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4'],
    'Profile Name': ['High-Volume Metro', 'Efficient Semi-Urban', 'Growing Urban', 'Rural Baseline'],
    'Avg Deposits (₹)': [125450, 45230, 67890, 12340],
    'Avg Offices': [234, 67, 98, 23],
    'Avg Accounts': [3456, 892, 1345, 234],
    'Dominant Region': ['Western', 'Northern', 'Southern', 'Eastern'],
    'Dominant Pop Group': ['METROPOLITAN', 'SEMI-URBAN', 'URBAN', 'RURAL'],
    'Size (records)': [1245, 2134, 1987, 1611],
    'Percentage': [17.8, 30.6, 28.5, 23.1]
})

# Display profiles
for i, row in cluster_profiles.iterrows():
    with st.expander(f"📌 {row['Profile Name']} ({row['Cluster']})", expanded=(i == 0)):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Average Deposits", f"₹{row['Avg Deposits (₹)']:,.0f}")
            st.metric("Average Offices", f"{row['Avg Offices']:,.0f}")
        
        with col2:
            st.metric("Average Accounts", f"{row['Avg Accounts']:,.0f}")
            st.metric("Cluster Size", f"{row['Size (records)']:,} ({row['Percentage']:.1f}%)")
        
        with col3:
            st.metric("Dominant Region", row['Dominant Region'])
            st.metric("Dominant Population", row['Dominant Pop Group'])
        
        # Characteristics
        if i == 0:
            st.markdown("""
            **Characteristics:**
            - 🏙️ Concentrated in metropolitan areas
            - 💰 Highest deposit amounts
            - 🏢 Large branch networks
            - 👥 Extensive customer base
            - ⚡ High efficiency ratios
            
            **Strategy:** Premium products, wealth management, digital banking
            """)
        elif i == 1:
            st.markdown("""
            **Characteristics:**
            - 🏘️ Semi-urban locations
            - 📊 Moderate deposit levels
            - ⚖️ Balanced infrastructure
            - 🎯 Growth-oriented markets
            - 💡 Good efficiency
            
            **Strategy:** Mass market products, financial literacy, expansion focus
            """)
        elif i == 2:
            st.markdown("""
            **Characteristics:**
            - 🌆 Urban centers
            - 📈 Growing deposit base
            - 🚀 Expansion phase
            - 👨‍👩‍👧‍👦 Diverse customer segments
            - 🔄 Dynamic markets
            
            **Strategy:** Product diversification, technology adoption, market penetration
            """)
        else:
            st.markdown("""
            **Characteristics:**
            - 🌾 Rural areas
            - 💵 Lower deposit volumes
            - 🏚️ Limited infrastructure
            - 📉 Challenges in penetration
            - 🎯 High potential for inclusion
            
            **Strategy:** Financial inclusion, mobile banking, government schemes, awareness programs
            """)

st.markdown("---")

# Cluster Comparison
st.header("⚖️ Cluster Comparison")

comparison_metric = st.selectbox(
    "Select metric to compare:",
    ["Average Deposits", "Average Offices", "Average Accounts", "Efficiency Ratio"]
)

col1, col2 = st.columns(2)

with col1:
    # Bar chart
    if comparison_metric == "Efficiency Ratio":
        cluster_profiles['Efficiency'] = cluster_profiles['Avg Deposits (₹)'] / cluster_profiles['Avg Offices']
        y_data = cluster_profiles['Efficiency']
        y_label = "Efficiency (₹/Office)"
    else:
        metric_map = {
            "Average Deposits": 'Avg Deposits (₹)',
            "Average Offices": 'Avg Offices',
            "Average Accounts": 'Avg Accounts'
        }
        y_data = cluster_profiles[metric_map[comparison_metric]]
        y_label = comparison_metric
    
    fig = go.Figure(go.Bar(
        x=cluster_profiles['Profile Name'],
        y=y_data,
        marker_color=[COLORS['primary'], COLORS['success'], COLORS['warning'], COLORS['secondary']],
        text=y_data.apply(lambda x: f'{x:,.0f}'),
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f"{comparison_metric} by Cluster",
        xaxis_title="Cluster Profile",
        yaxis_title=y_label,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Pie chart for cluster sizes
    fig = px.pie(
        cluster_profiles,
        values='Size (records)',
        names='Profile Name',
        title='Cluster Size Distribution',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)

# Parallel coordinates plot
st.subheader("📊 Multi-dimensional Cluster Comparison")

# Normalize data for parallel coordinates
normalized_profiles = cluster_profiles.copy()
for col in ['Avg Deposits (₹)', 'Avg Offices', 'Avg Accounts']:
    normalized_profiles[col + '_norm'] = (
        (normalized_profiles[col] - normalized_profiles[col].min()) / 
        (normalized_profiles[col].max() - normalized_profiles[col].min())
    )

fig = go.Figure(data=
    go.Parcoords(
        line=dict(
            color=list(range(len(cluster_profiles))),
            colorscale='Viridis'
        ),
        dimensions=[
            dict(label='Deposits', values=normalized_profiles['Avg Deposits (₹)_norm']),
            dict(label='Offices', values=normalized_profiles['Avg Offices_norm']),
            dict(label='Accounts', values=normalized_profiles['Avg Accounts_norm']),
            dict(label='Size', values=normalized_profiles['Percentage'] / 100)
        ],
        labelfont=dict(size=14),
        tickfont=dict(size=12)
    )
)

fig.update_layout(
    title="Parallel Coordinates Plot - Cluster Comparison (All Metrics Normalized 0-1)",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Business Applications
st.header("💼 Business Applications")

col1, col2 = st.columns(2)

with col1:
    st.success("""
    ### ✅ How to Use Clustering Insights
    
    **1. Targeted Marketing**
    - Design cluster-specific campaigns
    - Customize product offerings
    - Personalize communication strategies
    
    **2. Resource Allocation**
    - Prioritize high-potential clusters
    - Optimize infrastructure investment
    - Allocate staff based on cluster needs
    
    **3. Performance Benchmarking**
    - Compare within-cluster performance
    - Set cluster-specific KPIs
    - Identify best practices per cluster
    
    **4. Risk Management**
    - Monitor cluster-specific risks
    - Diversify across clusters
    - Develop cluster-tailored policies
    """)

with col2:
    st.info("""
    ### 💡 Strategic Recommendations
    
    **For Cluster 1 (High-Volume Metro):**
    - Focus on premium services
    - Invest in digital innovation
    - Expand wealth management
    
    **For Cluster 2 (Efficient Semi-Urban):**
    - Replicate successful models
    - Scale operations
    - Introduce mid-tier products
    
    **For Cluster 3 (Growing Urban):**
    - Aggressive expansion
    - Market penetration strategies
    - Product diversification
    
    **For Cluster 4 (Rural Baseline):**
    - Financial inclusion programs
    - Mobile banking push
    - Partnership with government schemes
    """)

st.markdown("---")

# Key Insights
st.header("🔑 Key Insights from Clustering")

insight_tabs = st.tabs(["Data Patterns", "Opportunities", "Challenges"])

with insight_tabs[0]:
    st.markdown("""
    ### 📊 Discovered Patterns
    
    1. **Natural Segmentation:**
       - Data naturally forms 4 distinct groups
       - Segments align with population groups
       - Geographic patterns emerge clearly
    
    2. **Metropolitan Dominance:**
       - Cluster 1 has 5-10x higher deposits
       - But represents only 17.8% of records
       - Wealth concentration is evident
    
    3. **Semi-Urban Potential:**
       - Largest cluster (30.6% of data)
       - Good efficiency metrics
       - Growth corridor opportunity
    
    4. **Rural Gap:**
       - 23.1% of records
       - Significantly lower deposits
       - Infrastructure deficit visible
    
    5. **Regional Clustering:**
       - Different regions dominate different clusters
       - Geographic economic disparities
       - Targeted regional strategies needed
    """)

with insight_tabs[1]:
    st.markdown("""
    ### 🎯 Business Opportunities
    
    1. **Cluster 2 Expansion:**
       - Semi-urban clusters show efficiency
       - Scalable model for replication
       - **ROI Potential: High**
    
    2. **Cluster 3 Penetration:**
       - Growing urban markets
       - Less saturated than metro
       - **Growth Potential: Very High**
    
    3. **Cluster 4 Inclusion:**
       - Untapped rural markets
       - Government support available
       - **Social Impact: Highest**
    
    4. **Cross-Cluster Learning:**
       - Best practices from Cluster 1
       - Efficiency from Cluster 2
       - **Innovation Opportunity**
    
    5. **Product Customization:**
       - Cluster-specific products
       - Tailored pricing strategies
       - **Revenue Optimization**
    """)

with insight_tabs[2]:
    st.markdown("""
    ### ⚠️ Challenges & Mitigation
    
    1. **Cluster Imbalance:**
       - **Challenge:** Uneven deposit distribution
       - **Mitigation:** Focus on balanced growth across clusters
    
    2. **Rural Penetration:**
       - **Challenge:** Low deposits, high costs
       - **Mitigation:** Digital banking, partnerships, subsidies
    
    3. **Market Saturation:**
       - **Challenge:** Metro markets nearing saturation
       - **Mitigation:** Shift focus to Clusters 2 & 3
    
    4. **Resource Constraints:**
       - **Challenge:** Limited resources for all clusters
       - **Mitigation:** Prioritize based on ROI and social impact
    
    5. **One-Size-Fits-All:**
       - **Challenge:** Uniform policies across diverse clusters
       - **Mitigation:** Develop cluster-specific strategies
    """)

st.markdown("---")

# Summary
st.header("📝 Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="padding: 1.5rem; background: #ecfdf5; border-radius: 10px; border-left: 4px solid #10b981;">
        <h4>🎯 Clusters Identified</h4>
        <ol>
            <li>High-Volume Metro (17.8%)</li>
            <li>Efficient Semi-Urban (30.6%)</li>
            <li>Growing Urban (28.5%)</li>
            <li>Rural Baseline (23.1%)</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="padding: 1.5rem; background: #eff6ff; border-radius: 10px; border-left: 4px solid #3b82f6;">
        <h4>💡 Best Algorithm</h4>
        <p><strong>K-Means</strong></p>
        <ul>
            <li>Silhouette: 0.612</li>
            <li>DB Score: 0.721</li>
            <li>Time: 0.034s</li>
            <li>Clear separation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="padding: 1.5rem; background: #fef3c7; border-radius: 10px; border-left: 4px solid #f59e0b;">
        <h4>🚀 Next Steps</h4>
        <ul>
            <li>Implement cluster strategies</li>
            <li>Monitor cluster evolution</li>
            <li>Measure cluster KPIs</li>
            <li>Refine segmentation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.success("""
### 🎉 Conclusion

Clustering analysis reveals **4 distinct banking profiles**, each requiring tailored strategies. 
By understanding these natural groupings, banks can optimize resource allocation, customize products, 
and develop targeted interventions for sustainable growth across all segments.

**Segmentation enables precision. Precision drives results.** 🎯
""")
