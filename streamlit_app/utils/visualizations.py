"""
Visualization utilities for Streamlit dashboard
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Color schemes
COLORS = {
    'primary': '#3b82f6',
    'secondary': '#8b5cf6',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#06b6d4',
    'population_groups': ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
}

def create_distribution_plot(df, column, title=None, color=COLORS['primary']):
    """Create histogram with distribution"""
    fig = px.histogram(
        df, 
        x=column,
        nbins=50,
        title=title or f'Distribution of {column}',
        color_discrete_sequence=[color]
    )
    
    fig.update_layout(
        showlegend=False,
        xaxis_title=column,
        yaxis_title='Count',
        template='plotly_white',
        height=400
    )
    
    return fig

def create_correlation_heatmap(df, columns):
    """Create correlation heatmap"""
    corr = df[columns].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr.values,
        texttemplate='%{text:.2f}',
        textfont={"size": 10}
    ))
    
    fig.update_layout(
        title='Correlation Heatmap',
        template='plotly_white',
        height=500,
        width=600
    )
    
    return fig

def create_population_group_chart(df):
    """Create population group distribution chart"""
    group_counts = df['population_group'].value_counts()
    
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'bar'}, {'type': 'pie'}]],
        subplot_titles=('Count by Population Group', 'Percentage Distribution')
    )
    
    # Bar chart
    fig.add_trace(
        go.Bar(
            x=group_counts.index,
            y=group_counts.values,
            marker_color=COLORS['population_groups'],
            text=group_counts.values,
            textposition='outside'
        ),
        row=1, col=1
    )
    
    # Pie chart
    fig.add_trace(
        go.Pie(
            labels=group_counts.index,
            values=group_counts.values,
            marker_colors=COLORS['population_groups']
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        template='plotly_white',
        height=400,
        showlegend=False
    )
    
    return fig

def create_regional_analysis(df):
    """Create regional analysis charts"""
    regional_stats = df.groupby('region').agg({
        'deposit_amount': ['sum', 'mean'],
        'no_of_offices': 'sum',
        'no_of_accounts': 'sum'
    }).round(2)
    
    regional_stats.columns = ['Total Deposits', 'Avg Deposits', 'Total Offices', 'Total Accounts']
    regional_stats = regional_stats.reset_index()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Total Deposits by Region',
            'Average Deposits by Region',
            'Total Offices by Region',
            'Total Accounts by Region'
        ),
        specs=[[{'type': 'bar'}, {'type': 'bar'}],
               [{'type': 'bar'}, {'type': 'bar'}]]
    )
    
    # Total Deposits
    fig.add_trace(
        go.Bar(x=regional_stats['region'], y=regional_stats['Total Deposits'],
               marker_color=COLORS['primary'], name='Total Deposits'),
        row=1, col=1
    )
    
    # Average Deposits
    fig.add_trace(
        go.Bar(x=regional_stats['region'], y=regional_stats['Avg Deposits'],
               marker_color=COLORS['success'], name='Avg Deposits'),
        row=1, col=2
    )
    
    # Total Offices
    fig.add_trace(
        go.Bar(x=regional_stats['region'], y=regional_stats['Total Offices'],
               marker_color=COLORS['warning'], name='Total Offices'),
        row=2, col=1
    )
    
    # Total Accounts
    fig.add_trace(
        go.Bar(x=regional_stats['region'], y=regional_stats['Total Accounts'],
               marker_color=COLORS['info'], name='Total Accounts'),
        row=2, col=2
    )
    
    fig.update_layout(
        template='plotly_white',
        height=800,
        showlegend=False
    )
    
    return fig

def create_model_comparison_chart(df):
    """Create model performance comparison"""
    top_15 = df.head(15)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=top_15['model_name'],
        x=top_15['test_r2'],
        orientation='h',
        marker_color=COLORS['primary'],
        text=top_15['test_r2'].round(4),
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Top 15 Models by R² Score',
        xaxis_title='R² Score',
        yaxis_title='Model',
        template='plotly_white',
        height=600,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def create_scatter_r2_vs_time(df):
    """Create scatter plot of R² vs Training Time"""
    # Create a safe size column (ensure positive values for marker size)
    df_plot = df.copy()
    df_plot['marker_size'] = df_plot['test_r2'].clip(lower=0) * 100 + 5  # Scale and add minimum size
    
    fig = px.scatter(
        df_plot,
        x='training_time',
        y='test_r2',
        color='test_r2',
        size='marker_size',
        hover_data=['model_name', 'test_rmse', 'test_mae'],
        title='R² Score vs Training Time Trade-off',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        xaxis_title='Training Time (seconds)',
        yaxis_title='R² Score',
        template='plotly_white',
        height=500
    )
    
    return fig

def create_actual_vs_predicted(y_true, y_pred):
    """Create actual vs predicted scatter plot"""
    fig = go.Figure()
    
    # Scatter plot
    fig.add_trace(go.Scatter(
        x=y_true,
        y=y_pred,
        mode='markers',
        marker=dict(
            color=COLORS['primary'],
            size=5,
            opacity=0.6
        ),
        name='Predictions'
    ))
    
    # Perfect prediction line
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    fig.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode='lines',
        line=dict(color='red', dash='dash'),
        name='Perfect Prediction'
    ))
    
    fig.update_layout(
        title='Actual vs Predicted Deposits',
        xaxis_title='Actual Deposit Amount',
        yaxis_title='Predicted Deposit Amount',
        template='plotly_white',
        height=500
    )
    
    return fig

def create_feature_importance_chart(features, importance):
    """Create feature importance bar chart"""
    df = pd.DataFrame({
        'feature': features,
        'importance': importance
    }).sort_values('importance', ascending=True).tail(15)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df['feature'],
        x=df['importance'],
        orientation='h',
        marker_color=COLORS['success']
    ))
    
    fig.update_layout(
        title='Top 15 Most Important Features',
        xaxis_title='Importance Score',
        yaxis_title='Feature',
        template='plotly_white',
        height=600
    )
    
    return fig

def create_box_plot_by_category(df, numerical_col, categorical_col):
    """Create box plot grouped by category"""
    fig = px.box(
        df,
        x=categorical_col,
        y=numerical_col,
        color=categorical_col,
        title=f'{numerical_col} by {categorical_col}'
    )
    
    fig.update_layout(
        template='plotly_white',
        height=500,
        showlegend=False
    )
    
    return fig

def create_top_states_chart(df, top_n=10):
    """Create top states by deposits chart"""
    top_states = df.groupby('state_name')['deposit_amount'].sum().sort_values(ascending=False).head(top_n)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=top_states.values,
        y=top_states.index,
        orientation='h',
        marker_color=COLORS['secondary'],
        text=[f'₹{val:,.0f}' for val in top_states.values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f'Top {top_n} States by Total Deposits',
        xaxis_title='Total Deposit Amount (₹)',
        yaxis_title='State',
        template='plotly_white',
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig
