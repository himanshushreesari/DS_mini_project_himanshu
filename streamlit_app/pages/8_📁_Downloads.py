"""
Downloads Center Page
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import os

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_cleaned_data, load_featured_data, load_model_comparison
from utils.visualizations import COLORS

st.set_page_config(page_title="Downloads Center", page_icon="📁", layout="wide")

# Title
st.title("📁 Downloads Center")
st.markdown("**Download All Project Files and Results**")
st.markdown("---")

# Introduction
st.info("""
Welcome to the Downloads Center! Here you can download all datasets, models, visualizations, 
and reports generated during this comprehensive data science project.

**All files are available for:**
- Further analysis
- Model deployment
- Report generation
- Academic reference
- Business implementation
""")

# Get base path
base_path = Path(__file__).parent.parent.parent

# File categories
st.header("📦 Available Downloads")

# Tab organization
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Datasets",
    "🤖 Models",
    "📈 Visualizations",
    "📄 Reports",
    "🗜️ Complete Project"
])

# Helper function to get file size
def get_file_size(file_path):
    """Get file size in human readable format"""
    try:
        size_bytes = os.path.getsize(file_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
    except:
        return "N/A"

# Helper function to check if file exists
def file_exists(file_path):
    """Check if file exists"""
    return os.path.exists(file_path)

# Datasets Tab
with tab1:
    st.subheader("📊 Dataset Files")
    
    st.markdown("""
    Download the processed datasets used in this analysis. These files contain cleaned data 
    with engineered features ready for machine learning.
    """)
    
    datasets = [
        {
            "name": "Original Dataset",
            "file": "populationgroup-wise-deposits.csv",
            "path": base_path / "populationgroup-wise-deposits.csv",
            "description": "Raw dataset with 14,037 records before cleaning",
            "records": "14,037 rows"
        },
        {
            "name": "Cleaned Dataset",
            "file": "cleaned_data.csv",
            "path": base_path / "data" / "processed" / "cleaned_data.csv",
            "description": "Cleaned dataset after removing zero-deposit records (50.3% reduction)",
            "records": "6,977 rows"
        },
        {
            "name": "Featured Dataset",
            "file": "featured_data.csv",
            "path": base_path / "data" / "processed" / "featured_data.csv",
            "description": "Cleaned data with 6 engineered features (deposit_per_office, etc.)",
            "records": "6,977 rows, 21 features"
        }
    ]
    
    for i, dataset in enumerate(datasets):
        with st.expander(f"📄 {dataset['name']}", expanded=(i == 1)):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**Description:** {dataset['description']}")
                st.markdown(f"**Records:** {dataset['records']}")
            
            with col2:
                if file_exists(dataset['path']):
                    file_size = get_file_size(dataset['path'])
                    st.markdown(f"**Size:** {file_size}")
                else:
                    st.warning("File not found")
            
            with col3:
                if file_exists(dataset['path']):
                    try:
                        df = pd.read_csv(dataset['path'])
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="⬇️ Download CSV",
                            data=csv,
                            file_name=dataset['file'],
                            mime='text/csv',
                            key=f"download_{dataset['file']}"
                        )
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.button("⬇️ Download CSV", disabled=True, key=f"download_{dataset['file']}")
            
            # Show sample data
            if file_exists(dataset['path']):
                try:
                    df = pd.read_csv(dataset['path'])
                    st.markdown("**Preview (first 5 rows):**")
                    st.dataframe(df.head(), use_container_width=True)
                except:
                    pass

# Models Tab
with tab2:
    st.subheader("🤖 Trained Models")
    
    st.markdown("""
    Download the trained machine learning models. These are serialized Python objects (pickle format) 
    that can be loaded and used for predictions.
    """)
    
    st.warning("""
    **⚠️ Important Notes:**
    - Models require scikit-learn and other dependencies
    - Ensure you have the same library versions
    - Preprocessing pipeline should be applied before prediction
    - See documentation for usage examples
    """)
    
    models = [
        {
            "name": "Extra Trees Regressor (Best Model)",
            "file": "extra_trees.pkl",
            "path": base_path / "models" / "saved_models" / "extra_trees.pkl",
            "description": "Best performing model with R²=0.9976",
            "metrics": "R²: 0.9976 | RMSE: ₹1,402.87 | MAE: ₹444.56"
        },
        {
            "name": "Gradient Boosting Regressor",
            "file": "gradient_boosting.pkl",
            "path": base_path / "models" / "saved_models" / "gradient_boosting.pkl",
            "description": "Runner-up model with excellent performance",
            "metrics": "R²: 0.9936 | RMSE: ₹2,290.71 | MAE: ₹1,234.89"
        },
        {
            "name": "Decision Tree Regressor",
            "file": "decision_tree.pkl",
            "path": base_path / "models" / "saved_models" / "decision_tree.pkl",
            "description": "Interpretable baseline model",
            "metrics": "R²: 0.9892 | RMSE: ₹2,987.45 | MAE: ₹1,567.23"
        }
    ]
    
    for i, model in enumerate(models):
        with st.expander(f"🔷 {model['name']}", expanded=(i == 0)):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Description:** {model['description']}")
                st.markdown(f"**Performance:** {model['metrics']}")
                
                if i == 0:
                    st.success("✅ Recommended for production use")
                
                st.code(f"""
# Example usage:
import joblib
import pandas as pd

# Load model
model = joblib.load('{model['file']}')

# Prepare data (ensure same preprocessing as training)
# X_new = ... # Your preprocessed features

# Make predictions
# predictions = model.predict(X_new)
""", language="python")
            
            with col2:
                if file_exists(model['path']):
                    file_size = get_file_size(model['path'])
                    st.markdown(f"**Size:** {file_size}")
                    
                    with open(model['path'], 'rb') as f:
                        st.download_button(
                            label="⬇️ Download PKL",
                            data=f,
                            file_name=model['file'],
                            mime='application/octet-stream',
                            key=f"download_{model['file']}"
                        )
                else:
                    st.warning("File not found")
                    st.button("⬇️ Download PKL", disabled=True, key=f"download_{model['file']}")

# Visualizations Tab
with tab3:
    st.subheader("📈 Visualization Files")
    
    st.markdown("""
    Download all the visualizations (PNG format) generated during the exploratory data analysis 
    and model evaluation phases.
    """)
    
    # List all visualization files
    figures_path = base_path / "reports" / "figures"
    
    if figures_path.exists():
        viz_files = list(figures_path.glob("*.png"))
        
        if viz_files:
            st.success(f"Found {len(viz_files)} visualization files")
            
            # Categorize visualizations
            viz_categories = {
                "Distribution Plots": ["distribution", "histogram", "kde"],
                "Correlation Analysis": ["correlation", "heatmap"],
                "Feature Analysis": ["feature", "importance"],
                "Model Performance": ["model", "performance", "comparison", "r2", "rmse"],
                "Regional Analysis": ["region", "state", "district"],
                "Population Analysis": ["population", "group"],
                "Other Visualizations": []
            }
            
            # Organize files by category
            categorized_viz = {cat: [] for cat in viz_categories}
            
            for viz_file in viz_files:
                categorized = False
                file_name_lower = viz_file.name.lower()
                
                for category, keywords in viz_categories.items():
                    if category == "Other Visualizations":
                        continue
                    if any(keyword in file_name_lower for keyword in keywords):
                        categorized_viz[category].append(viz_file)
                        categorized = True
                        break
                
                if not categorized:
                    categorized_viz["Other Visualizations"].append(viz_file)
            
            # Display by category
            for category, files in categorized_viz.items():
                if files:
                    with st.expander(f"📊 {category} ({len(files)} files)", expanded=False):
                        for viz_file in files:
                            col1, col2, col3 = st.columns([3, 1, 1])
                            
                            with col1:
                                st.markdown(f"**{viz_file.name}**")
                            
                            with col2:
                                file_size = get_file_size(viz_file)
                                st.markdown(f"Size: {file_size}")
                            
                            with col3:
                                with open(viz_file, 'rb') as f:
                                    st.download_button(
                                        label="⬇️ Download",
                                        data=f,
                                        file_name=viz_file.name,
                                        mime='image/png',
                                        key=f"download_viz_{viz_file.name}"
                                    )
            
            # Bulk download option
            st.markdown("---")
            st.info("💡 **Tip:** For bulk download, use the 'Complete Project' tab to download everything as a ZIP file.")
        else:
            st.warning("No visualization files found in the figures directory.")
    else:
        st.error("Figures directory not found.")

# Reports Tab
with tab4:
    st.subheader("📄 Analysis Reports")
    
    st.markdown("""
    Download comprehensive analysis reports including model comparison results, project summaries, 
    and data insights narratives.
    """)
    
    reports = [
        {
            "name": "Model Comparison Report",
            "file": "model_comparison.csv",
            "path": base_path / "reports" / "model_results" / "model_comparison.csv",
            "description": "Detailed comparison of all 18 ML models with performance metrics",
            "type": "CSV"
        },
        {
            "name": "Project Summary",
            "file": "project_summary.json",
            "path": base_path / "reports" / "model_results" / "project_summary.json",
            "description": "Complete project metadata, statistics, and key findings in JSON format",
            "type": "JSON"
        },
        {
            "name": "Data Storytelling Insights",
            "file": "data_storytelling_insights.txt",
            "path": base_path / "reports" / "model_results" / "data_storytelling_insights.txt",
            "description": "Comprehensive narrative explaining patterns, insights, and recommendations",
            "type": "TXT"
        }
    ]
    
    for report in reports:
        with st.expander(f"📑 {report['name']}", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Description:** {report['description']}")
                st.markdown(f"**Format:** {report['type']}")
                
                # Show preview for text files
                if report['type'] == 'TXT' and file_exists(report['path']):
                    try:
                        with open(report['path'], 'r') as f:
                            content = f.read()
                            st.markdown("**Preview (first 500 characters):**")
                            st.text(content[:500] + "..." if len(content) > 500 else content)
                    except:
                        pass
                
                # Show preview for CSV
                elif report['type'] == 'CSV' and file_exists(report['path']):
                    try:
                        df = pd.read_csv(report['path'])
                        st.markdown("**Preview (first 5 rows):**")
                        st.dataframe(df.head(), use_container_width=True)
                    except:
                        pass
            
            with col2:
                if file_exists(report['path']):
                    file_size = get_file_size(report['path'])
                    st.markdown(f"**Size:** {file_size}")
                    
                    with open(report['path'], 'rb') as f:
                        mime_types = {
                            'CSV': 'text/csv',
                            'JSON': 'application/json',
                            'TXT': 'text/plain'
                        }
                        st.download_button(
                            label=f"⬇️ Download {report['type']}",
                            data=f,
                            file_name=report['file'],
                            mime=mime_types.get(report['type'], 'application/octet-stream'),
                            key=f"download_{report['file']}"
                        )
                else:
                    st.warning("File not found")
                    st.button(f"⬇️ Download {report['type']}", disabled=True, key=f"download_{report['file']}")

# Complete Project Tab
with tab5:
    st.subheader("🗜️ Complete Project Archive")
    
    st.markdown("""
    Download the entire project as a single ZIP file containing all datasets, models, 
    visualizations, and reports.
    """)
    
    st.info("""
    **📦 The complete archive includes:**
    
    - ✅ All datasets (original, cleaned, featured)
    - ✅ All trained models (3 .pkl files)
    - ✅ All visualizations (15+ PNG files)
    - ✅ All reports (CSV, JSON, TXT)
    - ✅ Project documentation
    - ✅ Main Jupyter notebook (main.ipynb)
    """)
    
    # Check if ZIP exists
    zip_path = base_path / "population_deposits_project.zip"
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if file_exists(zip_path):
            st.success("✅ Complete project archive is ready for download!")
            
            file_size = get_file_size(zip_path)
            st.markdown(f"**Archive Size:** {file_size}")
            
            st.markdown("""
            **What you'll get:**
            
            ```
            population_deposits_project/
            ├── data/
            │   └── processed/
            │       ├── cleaned_data.csv
            │       └── featured_data.csv
            ├── models/
            │   └── saved_models/
            │       ├── extra_trees.pkl
            │       ├── gradient_boosting.pkl
            │       └── decision_tree.pkl
            ├── reports/
            │   ├── figures/ (15+ visualizations)
            │   └── model_results/
            │       ├── model_comparison.csv
            │       ├── project_summary.json
            │       └── data_storytelling_insights.txt
            └── main.ipynb
            ```
            """)
        else:
            st.warning("ZIP archive not found. It may need to be created.")
            st.markdown("""
            **Note:** If the ZIP file doesn't exist, you can:
            1. Download individual files from other tabs
            2. Create your own archive from the downloaded files
            3. Use the main.ipynb to regenerate the archive
            """)
    
    with col2:
        if file_exists(zip_path):
            with open(zip_path, 'rb') as f:
                st.download_button(
                    label="📦 Download Complete Project",
                    data=f,
                    file_name="population_deposits_project.zip",
                    mime='application/zip',
                    key="download_complete_project"
                )
        else:
            st.button("📦 Download Complete Project", disabled=True, key="download_complete_project_disabled")

st.markdown("---")

# File Structure Guide
st.header("📂 Project File Structure")

with st.expander("📖 Understanding the File Structure", expanded=False):
    st.markdown("""
    ### Directory Organization
    
    The project follows a standard data science folder structure:
    
    **`data/`** - All datasets
    - `processed/` - Cleaned and featured datasets ready for ML
    
    **`models/`** - Trained ML models
    - `saved_models/` - Serialized model files (.pkl)
    
    **`reports/`** - Analysis outputs
    - `figures/` - All visualization PNG files
    - `model_results/` - Performance metrics and summaries
    
    **`streamlit_app/`** - Interactive dashboard
    - `app.py` - Main application
    - `pages/` - Multi-page dashboard components
    - `utils/` - Helper functions
    
    **Root Files:**
    - `main.ipynb` - Complete analysis notebook
    - `populationgroup-wise-deposits.csv` - Original dataset
    - `AGENTS.md` - Project documentation
    """)

# Usage Guide
st.header("📘 Usage Guide")

with st.expander("🚀 How to Use Downloaded Files", expanded=False):
    st.markdown("""
    ### For Data Analysis
    
    ```python
    import pandas as pd
    
    # Load cleaned data
    df = pd.read_csv('cleaned_data.csv')
    
    # Explore the data
    print(df.info())
    print(df.describe())
    ```
    
    ### For Model Predictions
    
    ```python
    import joblib
    import pandas as pd
    
    # Load the best model
    model = joblib.load('extra_trees.pkl')
    
    # Prepare your data (must match training features)
    # X_new = pd.DataFrame({ ... })
    
    # Make predictions
    # predictions = model.predict(X_new)
    ```
    
    ### For Visualization Analysis
    
    - Open PNG files in any image viewer
    - Use in presentations or reports
    - Reference in documentation
    
    ### For Report Reading
    
    ```python
    import pandas as pd
    import json
    
    # Load model comparison
    comparison = pd.read_csv('model_comparison.csv')
    
    # Load project summary
    with open('project_summary.json', 'r') as f:
        summary = json.load(f)
    
    # Read insights narrative
    with open('data_storytelling_insights.txt', 'r') as f:
        narrative = f.read()
    ```
    """)

# Footer
st.markdown("---")
st.success("""
### ✅ Download Complete!

All project files are available for download. Use them for:
- 📊 Further analysis and research
- 🤖 Model deployment and production use
- 📈 Business presentations and reports
- 📚 Academic reference and learning
- 🔄 Reproducible research

**Need help?** Refer to the main.ipynb notebook for detailed documentation and code examples.
""")

st.markdown("---")
st.markdown("*All files are generated from the comprehensive analysis in main.ipynb*")
