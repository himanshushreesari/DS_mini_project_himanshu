"""
Population Group-wise Deposits Analysis
Streamlit Dashboard - Main App

Author: Himanshu
Date: November 9, 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Population Deposits Analysis",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    st.markdown("""
    <style>
    /* Main title styling */
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Info boxes */
    .info-box {
        padding: 1rem;
        border-left: 4px solid #3b82f6;
        background-color: #eff6ff;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Success boxes */
    .success-box {
        padding: 1rem;
        border-left: 4px solid #10b981;
        background-color: #ecfdf5;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

load_css()

# Title and introduction
st.markdown('<h1 class="main-title">🏦 Population Group-wise Deposits Analysis</h1>', unsafe_allow_html=True)
st.markdown("---")

# Welcome section
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h2>Welcome to the Interactive Dashboard</h2>
        <p style="font-size: 1.2rem; color: #64748b;">
            Explore comprehensive insights from our analysis of population group-wise 
            bank deposits across Indian states and districts.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Quick stats section
st.markdown("### 📊 Project Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3 style="margin:0;">6,977</h3>
        <p style="margin:0.5rem 0 0 0;">Records Analyzed</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3 style="margin:0;">18</h3>
        <p style="margin:0.5rem 0 0 0;">ML Models Trained</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3 style="margin:0;">99.76%</h3>
        <p style="margin:0.5rem 0 0 0;">Best Model R² Score</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h3 style="margin:0;">₹58.8B</h3>
        <p style="margin:0.5rem 0 0 0;">Total Deposits</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Navigation guide
st.markdown("### 🧭 Navigation Guide")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-box">
        <h4>📈 Exploratory Analysis</h4>
        <p>Dive into data distributions, correlations, and statistical insights.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-box">
        <h4>🤖 Machine Learning</h4>
        <p>Explore model performance, comparisons, and predictions.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-box">
        <h4>💡 Insights & Recommendations</h4>
        <p>Discover actionable business insights and strategic recommendations.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Key findings
st.markdown("### 🌟 Key Highlights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="success-box">
        <h4>✅ Data Quality</h4>
        <ul>
            <li>36 states covered</li>
            <li>717 districts analyzed</li>
            <li>50.3% data cleaning performed</li>
            <li>Zero missing values in final dataset</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="success-box">
        <h4>✅ Model Performance</h4>
        <ul>
            <li>Extra Trees: R² = 0.9976</li>
            <li>Gradient Boosting: R² = 0.9936</li>
            <li>GPU acceleration utilized</li>
            <li>SHAP interpretability applied</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Getting started
st.markdown("### 🚀 Getting Started")
st.info("""
**How to use this dashboard:**
1. Use the **sidebar** on the left to navigate between different pages
2. Apply **filters** to customize your analysis
3. Interact with **charts** by hovering, zooming, and clicking
4. Download **data and visualizations** from the Downloads page
5. Try the **Prediction Tool** to forecast deposit amounts

👈 **Start by selecting a page from the sidebar!**
""")

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #64748b;">
    <p><strong>Population Group-wise Deposits Analysis Dashboard</strong></p>
    <p>Built with ❤️ using Streamlit | Author: Himanshu | Date: November 9, 2025</p>
</div>
""", unsafe_allow_html=True)
