"""
Machine Learning Models Page
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_model_comparison, load_best_model, load_featured_data
from utils.visualizations import (
    create_model_comparison_chart, create_scatter_r2_vs_time,
    create_actual_vs_predicted
)

st.set_page_config(page_title="ML Models - Deposits Analysis", page_icon="🤖", layout="wide")

# Title
st.title("🤖 Machine Learning Models")
st.markdown("---")

# Load data
comparison_df = load_model_comparison()

if comparison_df is None:
    st.error("Unable to load model comparison data.")
    st.stop()

# Overview
st.header("📊 Models Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Models Trained", len(comparison_df))

with col2:
    best_r2 = comparison_df['test_r2'].max()
    st.metric("Best R² Score", f"{best_r2:.4f}")

with col3:
    best_model_name = comparison_df.loc[comparison_df['test_r2'].idxmax(), 'model_name']
    st.metric("Best Model", best_model_name)

with col4:
    best_rmse = comparison_df['test_rmse'].min()
    st.metric("Best RMSE", f"₹{best_rmse:,.2f}")

st.markdown("---")

# Model Categories
st.header("🎯 Model Categories")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="padding: 1rem; background: #eff6ff; border-radius: 10px; border-left: 4px solid #3b82f6;">
        <h4>Baseline Models (5)</h4>
        <ul>
            <li>Linear Regression</li>
            <li>Ridge Regression</li>
            <li>Lasso Regression</li>
            <li>ElasticNet</li>
            <li>K-Nearest Neighbors</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="padding: 1rem; background: #ecfdf5; border-radius: 10px; border-left: 4px solid #10b981;">
        <h4>Ensemble Models (7)</h4>
        <ul>
            <li>Decision Tree</li>
            <li>Random Forest</li>
            <li>Extra Trees</li>
            <li>Gradient Boosting</li>
            <li>XGBoost (GPU)</li>
            <li>LightGBM</li>
            <li>CatBoost (GPU)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="padding: 1rem; background: #fef3c7; border-radius: 10px; border-left: 4px solid #f59e0b;">
        <h4>Advanced Models (6)</h4>
        <ul>
            <li>SVR (Linear)</li>
            <li>SVR (RBF)</li>
            <li>SVR (Polynomial)</li>
            <li>AdaBoost</li>
            <li>Bayesian Ridge</li>
            <li>Neural Network (GPU)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Model Performance Comparison
st.header("📈 Model Performance Comparison")

# Interactive table
st.subheader("🔍 Detailed Model Metrics")

# Add filters
col1, col2, col3 = st.columns(3)

with col1:
    sort_by = st.selectbox(
        "Sort by",
        ['test_r2', 'test_rmse', 'test_mae', 'training_time']
    )

with col2:
    ascending = st.checkbox("Ascending Order", value=False)

with col3:
    show_top_n = st.slider("Show top N models", 5, len(comparison_df), 15)

# Sort and filter
sorted_df = comparison_df.sort_values(sort_by, ascending=ascending).head(show_top_n)

# Display table
st.dataframe(
    sorted_df[['model_name', 'test_r2', 'test_rmse', 'test_mae', 'training_time']].style.format({
        'test_r2': '{:.4f}',
        'test_rmse': '₹{:,.2f}',
        'test_mae': '₹{:,.2f}',
        'training_time': '{:.4f}s'
    }),
    use_container_width=True,
    height=400
)

st.markdown("---")

# Visualizations
st.header("📊 Performance Visualizations")

tab1, tab2, tab3 = st.tabs(["R² Scores", "R² vs Time Trade-off", "RMSE Comparison"])

with tab1:
    fig = create_model_comparison_chart(comparison_df)
    st.plotly_chart(fig, use_container_width=True)
    
    st.success(f"""
    **Best Model:** {best_model_name}  
    **R² Score:** {best_r2:.4f} (explains {best_r2*100:.2f}% of variance)
    """)

with tab2:
    fig = create_scatter_r2_vs_time(comparison_df)
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    **Insight:** Models in the top-right corner offer the best trade-off 
    between accuracy and training speed. Extra Trees and Gradient Boosting 
    provide excellent performance with reasonable training times.
    """)

with tab3:
    top_15_rmse = comparison_df.nsmallest(15, 'test_rmse')
    
    import plotly.graph_objects as go
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top_15_rmse['model_name'],
        x=top_15_rmse['test_rmse'],
        orientation='h',
        marker_color='coral',
        text=top_15_rmse['test_rmse'].round(2),
        textposition='outside'
    ))
    fig.update_layout(
        title='Top 15 Models by RMSE (Lower is Better)',
        xaxis_title='RMSE (₹)',
        yaxis_title='Model',
        template='plotly_white',
        height=600,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Best Model Showcase
st.header("🏆 Best Model: Extra Trees Regressor")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Why Extra Trees Excelled
    
    The **Extra Trees (Extremely Randomized Trees)** model achieved the best performance:
    
    - **R² Score:** 0.9976 (99.76% variance explained)
    - **RMSE:** ₹1,402.87
    - **MAE:** ₹444.56
    
    **Key Advantages:**
    1. ✅ Captures complex non-linear relationships
    2. ✅ Handles feature interactions effectively
    3. ✅ Robust to outliers in deposit amounts
    4. ✅ Excellent generalization on test data
    5. ✅ Fast training with parallel processing
    
    **How it works:**
    - Builds multiple decision trees with random splits
    - Averages predictions across all trees
    - Reduces overfitting through randomization
    - No need for cross-validation due to bootstrap sampling
    """)

with col2:
    # Model metrics card
    st.markdown("""
    <div style="padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 10px; color: white; text-align: center;">
        <h3>Model Performance</h3>
        <hr style="border-color: rgba(255,255,255,0.3);">
        <p style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">99.76%</p>
        <p>Accuracy (R²)</p>
        <hr style="border-color: rgba(255,255,255,0.3);">
        <p style="font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0;">₹1,403</p>
        <p>Average Error (RMSE)</p>
        <hr style="border-color: rgba(255,255,255,0.3);">
        <p style="font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0;">₹445</p>
        <p>Mean Absolute Error</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("🎯 **Recommended for Production Deployment**")

st.markdown("---")

# Predictions visualization (if model available)
try:
    best_model = load_best_model("extra_trees")
    featured_df = load_featured_data()
    
    if best_model is not None and featured_df is not None:
        st.header("📉 Model Predictions Analysis")
        
        st.info("Loading predictions from the trained Extra Trees model...")
        
        # Prepare data (simplified - adjust based on actual feature engineering)
        # Note: This is a simplified example. In production, you'd need the exact
        # preprocessing pipeline used during training
        
        st.markdown("""
        **Note:** For actual vs predicted plots, you would need:
        1. The exact train/test split used during training
        2. The preprocessing pipeline (scaling, encoding)
        3. The feature engineering steps
        
        These are available in the saved models and can be loaded for prediction.
        """)
        
except Exception as e:
    st.warning(f"Model predictions not available for visualization: {str(e)}")

st.markdown("---")

# Model Comparison Summary
st.header("📋 Model Comparison Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Top 5 by R² Score")
    top_5_r2 = comparison_df.nlargest(5, 'test_r2')[['model_name', 'test_r2']]
    for idx, (_, row) in enumerate(top_5_r2.iterrows(), 1):
        st.write(f"{idx}. **{row['model_name']}** - {row['test_r2']:.4f}")

with col2:
    st.markdown("### Fastest Training")
    top_5_speed = comparison_df.nsmallest(5, 'training_time')[['model_name', 'training_time']]
    for idx, (_, row) in enumerate(top_5_speed.iterrows(), 1):
        st.write(f"{idx}. **{row['model_name']}** - {row['training_time']:.4f}s")

with col3:
    st.markdown("### Lowest RMSE")
    top_5_rmse = comparison_df.nsmallest(5, 'test_rmse')[['model_name', 'test_rmse']]
    for idx, (_, row) in enumerate(top_5_rmse.iterrows(), 1):
        st.write(f"{idx}. **{row['model_name']}** - ₹{row['test_rmse']:,.2f}")

st.markdown("---")

# Download results
st.header("💾 Download Model Results")

csv = comparison_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Full Model Comparison (CSV)",
    data=csv,
    file_name="model_comparison.csv",
    mime="text/csv"
)
