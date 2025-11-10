"""
Data loading utilities for Streamlit dashboard
"""

import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
import streamlit as st

# Base path - adjust based on directory structure
BASE_PATH = Path(__file__).parent.parent.parent

@st.cache_data
def load_cleaned_data():
    """Load cleaned dataset"""
    try:
        data_path = BASE_PATH / "data" / "processed" / "cleaned_data.csv"
        df = pd.read_csv(data_path)
        return df
    except Exception as e:
        st.error(f"Error loading cleaned data: {e}")
        return None

@st.cache_data
def load_featured_data():
    """Load featured dataset with engineered features"""
    try:
        data_path = BASE_PATH / "data" / "processed" / "featured_data.csv"
        df = pd.read_csv(data_path)
        return df
    except Exception as e:
        st.error(f"Error loading featured data: {e}")
        return None

@st.cache_data
def load_model_comparison():
    """Load model comparison results"""
    try:
        comparison_path = BASE_PATH / "reports" / "model_results" / "final_model_comparison.csv"
        df = pd.read_csv(comparison_path)
        return df
    except Exception as e:
        st.error(f"Error loading model comparison: {e}")
        return None

@st.cache_resource
def load_best_model(model_name="extra_trees"):
    """Load trained model"""
    try:
        model_path = BASE_PATH / "models" / "saved_models" / f"{model_name}.pkl"
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model {model_name}: {e}")
        return None

@st.cache_data
def load_project_summary():
    """Load project summary JSON"""
    try:
        summary_path = BASE_PATH / "reports" / "model_results" / "project_summary.json"
        with open(summary_path, 'r') as f:
            summary = json.load(f)
        return summary
    except Exception as e:
        st.error(f"Error loading project summary: {e}")
        return None

@st.cache_data
def load_insights_narrative():
    """Load data storytelling insights"""
    try:
        insights_path = BASE_PATH / "reports" / "model_results" / "data_storytelling_insights.txt"
        with open(insights_path, 'r') as f:
            narrative = f.read()
        return narrative
    except Exception as e:
        st.error(f"Error loading insights: {e}")
        return None

def get_population_groups():
    """Get list of population groups"""
    return ['Metropolitan', 'Urban', 'Semi-urban', 'Rural']

def get_regions():
    """Get list of regions"""
    df = load_cleaned_data()
    if df is not None:
        return sorted(df['region'].unique().tolist())
    return []

def get_states():
    """Get list of states"""
    df = load_cleaned_data()
    if df is not None:
        return sorted(df['state_name'].unique().tolist())
    return []

def get_districts(state=None):
    """Get list of districts, optionally filtered by state"""
    df = load_cleaned_data()
    if df is not None:
        if state:
            return sorted(df[df['state_name'] == state]['district_name'].unique().tolist())
        return sorted(df['district_name'].unique().tolist())
    return []

def filter_data(df, population_group=None, region=None, state=None):
    """Apply filters to dataframe"""
    filtered_df = df.copy()
    
    if population_group and population_group != "All":
        filtered_df = filtered_df[filtered_df['population_group'] == population_group]
    
    if region and region != "All":
        filtered_df = filtered_df[filtered_df['region'] == region]
    
    if state and state != "All":
        filtered_df = filtered_df[filtered_df['state_name'] == state]
    
    return filtered_df

def get_summary_stats(df):
    """Calculate summary statistics"""
    stats = {
        'total_records': len(df),
        'total_deposits': df['deposit_amount'].sum(),
        'avg_deposits': df['deposit_amount'].mean(),
        'total_offices': df['no_of_offices'].sum(),
        'total_accounts': df['no_of_accounts'].sum(),
        'unique_states': df['state_name'].nunique(),
        'unique_districts': df['district_name'].nunique()
    }
    return stats
