"""
Predictions Tool Page
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import (
    load_best_model, get_population_groups, get_regions, 
    get_states, get_districts, load_cleaned_data
)

st.set_page_config(page_title="Prediction Tool", page_icon="🎯", layout="wide")

# Title
st.title("🎯 Deposit Amount Prediction Tool")
st.markdown("---")

st.info("""
**How to use this tool:**
1. Enter the banking infrastructure details below
2. Click "Predict Deposit Amount" to get the prediction
3. Compare your scenario with average values
4. Experiment with different combinations to see the impact
""")

st.markdown("---")

# Load data for reference
df = load_cleaned_data()

if df is None:
    st.error("Unable to load reference data.")
    st.stop()

# Calculate reference statistics
avg_offices = df['no_of_offices'].mean()
avg_accounts = df['no_of_accounts'].mean()
avg_deposits = df['deposit_amount'].mean()

# Input Form
st.header("📝 Enter Banking Details")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Infrastructure")
    
    no_of_offices = st.number_input(
        "Number of Offices",
        min_value=1,
        max_value=int(df['no_of_offices'].max()),
        value=int(avg_offices),
        step=1,
        help=f"Average: {avg_offices:.0f} offices"
    )
    
    no_of_accounts = st.number_input(
        "Number of Accounts",
        min_value=1,
        max_value=int(df['no_of_accounts'].max()),
        value=int(avg_accounts),
        step=100,
        help=f"Average: {avg_accounts:.0f} accounts"
    )
    
    st.metric("Accounts per Office", f"{no_of_accounts/no_of_offices:.2f}")

with col2:
    st.subheader("Location Details")
    
    population_group = st.selectbox(
        "Population Group",
        get_population_groups()
    )
    
    region = st.selectbox(
        "Region",
        get_regions()
    )
    
    state = st.selectbox(
        "State",
        get_states()
    )
    
    district = st.selectbox(
        "District",
        get_districts(state)
    )

st.markdown("---")

# Prediction Button
if st.button("🔮 Predict Deposit Amount", type="primary"):
    with st.spinner("Calculating prediction..."):
        # Note: This is a simplified prediction example
        # In production, you'd need:
        # 1. The exact preprocessing pipeline used during training
        # 2. Feature engineering steps (derived features)
        # 3. Encoding for categorical variables
        
        # For demonstration, we'll use a simple estimation based on similar records
        # In real deployment, load the actual model and use its predict method
        
        # Find similar records
        similar_records = df[
            (df['population_group'] == population_group) &
            (df['region'] == region)
        ]
        
        if len(similar_records) > 0:
            # Calculate prediction based on linear relationship from similar records
            avg_deposit_per_office = similar_records['deposit_amount'].sum() / similar_records['no_of_offices'].sum()
            avg_deposit_per_account = similar_records['deposit_amount'].sum() / similar_records['no_of_accounts'].sum()
            
            # Weighted prediction
            predicted_deposit = (
                (no_of_offices * avg_deposit_per_office * 0.5) +
                (no_of_accounts * avg_deposit_per_account * 0.5)
            )
            
            st.success("✅ Prediction Complete!")
            
            # Display prediction
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style="padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            border-radius: 10px; color: white; text-align: center;">
                    <h3>Predicted Deposit</h3>
                    <p style="font-size: 2.5rem; font-weight: bold; margin: 1rem 0;">
                        ₹{predicted_deposit:,.0f}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                comparison_avg = ((predicted_deposit - avg_deposits) / avg_deposits) * 100
                color = "green" if comparison_avg > 0 else "red"
                arrow = "↑" if comparison_avg > 0 else "↓"
                
                st.markdown(f"""
                <div style="padding: 2rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            border-radius: 10px; color: white; text-align: center;">
                    <h3>vs Average</h3>
                    <p style="font-size: 2.5rem; font-weight: bold; margin: 1rem 0; color: {color};">
                        {arrow} {abs(comparison_avg):.1f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                confidence = 85 if len(similar_records) > 10 else 70
                
                st.markdown(f"""
                <div style="padding: 2rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                            border-radius: 10px; color: white; text-align: center;">
                    <h3>Confidence</h3>
                    <p style="font-size: 2.5rem; font-weight: bold; margin: 1rem 0;">
                        {confidence}%
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Detailed breakdown
            st.subheader("📊 Prediction Breakdown")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Input Summary")
                st.write(f"**Offices:** {no_of_offices:,}")
                st.write(f"**Accounts:** {no_of_accounts:,}")
                st.write(f"**Population Group:** {population_group}")
                st.write(f"**Region:** {region}")
                st.write(f"**State:** {state}")
                st.write(f"**District:** {district}")
            
            with col2:
                st.markdown("### Comparison Metrics")
                st.write(f"**Predicted Deposit:** ₹{predicted_deposit:,.0f}")
                st.write(f"**Average Deposit:** ₹{avg_deposits:,.0f}")
                st.write(f"**Deposit per Office:** ₹{predicted_deposit/no_of_offices:,.0f}")
                st.write(f"**Deposit per Account:** ₹{predicted_deposit/no_of_accounts:,.0f}")
                st.write(f"**Similar Records Found:** {len(similar_records):,}")
            
            st.markdown("---")
            
            # Insights
            st.subheader("💡 Insights")
            
            if population_group == "Metropolitan":
                st.info("🏙️ Metropolitan areas typically have higher average deposits due to concentrated wealth and better banking infrastructure.")
            elif population_group == "Rural":
                st.warning("🌾 Rural areas generally show lower deposit amounts but represent significant growth potential for financial inclusion.")
            
            if no_of_accounts / no_of_offices > 15:
                st.success("✅ Above-average accounts per office ratio indicates good operational efficiency!")
            elif no_of_accounts / no_of_offices < 10:
                st.warning("⚠️ Low accounts per office ratio suggests potential for account acquisition growth.")
            
        else:
            st.error("No similar records found for this combination. Please try different parameters.")

st.markdown("---")

# Scenario Comparison
st.header("📊 Scenario Comparison")

st.info("Compare multiple scenarios side-by-side to understand the impact of different parameters.")

num_scenarios = st.slider("Number of scenarios to compare", 2, 4, 2)

scenario_cols = st.columns(num_scenarios)

for idx, col in enumerate(scenario_cols):
    with col:
        st.markdown(f"### Scenario {idx + 1}")
        
        with st.expander(f"Configure Scenario {idx + 1}", expanded=False):
            s_offices = st.number_input(f"Offices (S{idx+1})", min_value=1, value=int(avg_offices)*(idx+1), key=f"offices_{idx}")
            s_accounts = st.number_input(f"Accounts (S{idx+1})", min_value=1, value=int(avg_accounts)*(idx+1), key=f"accounts_{idx}")
            s_pop_group = st.selectbox(f"Pop Group (S{idx+1})", get_population_groups(), key=f"pop_{idx}")
            s_region = st.selectbox(f"Region (S{idx+1})", get_regions(), key=f"region_{idx}")
            
            # Simple prediction for scenario
            similar = df[(df['population_group'] == s_pop_group) & (df['region'] == s_region)]
            if len(similar) > 0:
                avg_per_office = similar['deposit_amount'].sum() / similar['no_of_offices'].sum()
                s_prediction = s_offices * avg_per_office
            else:
                s_prediction = avg_deposits
            
            st.metric("Predicted Deposit", f"₹{s_prediction:,.0f}")
            st.metric("Per Office", f"₹{s_prediction/s_offices:,.0f}")

st.markdown("---")

# Reference Statistics
st.header("📈 Reference Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Avg Offices", f"{avg_offices:.0f}")
with col2:
    st.metric("Avg Accounts", f"{avg_accounts:.0f}")
with col3:
    st.metric("Avg Deposits", f"₹{avg_deposits:,.0f}")
with col4:
    st.metric("Avg Accounts/Office", f"{avg_accounts/avg_offices:.1f}")

st.markdown("---")

# Note about model
st.warning("""
**⚠️ Note:** This prediction tool uses a simplified estimation based on similar records in the dataset. 
For production deployment, the actual Extra Trees model should be loaded with the complete preprocessing 
pipeline including:
- Feature engineering (deposit_per_office, deposit_per_account, accounts_per_office, etc.)
- Categorical encoding (one-hot encoding for population groups and regions)
- Label encoding (for states and districts)
- Feature scaling (StandardScaler)

The saved model files are available in the `models/saved_models/` directory.
""")
