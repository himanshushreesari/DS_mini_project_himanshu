# 🏦 Population Group-wise Deposits Analysis Dashboard

An interactive Streamlit dashboard showcasing comprehensive data science analysis of banking deposits across different population groups in India.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📊 Project Overview

This dashboard presents the findings from a comprehensive analysis of **6,977 banking records** across **36 Indian states** and **717 districts**, featuring:

- ✅ Detailed Exploratory Data Analysis (EDA)
- ✅ 18 Machine Learning Models (99.76% best accuracy!)
- ✅ SHAP-based Model Interpretability
- ✅ Geographic Insights & Regional Analysis
- ✅ Clustering Analysis (4 distinct segments)
- ✅ Interactive Prediction Tool
- ✅ Business Insights & Recommendations

## 🎯 Key Achievements

- **Best Model:** Extra Trees Regressor with **R² = 0.9976**
- **RMSE:** ₹1,402.87
- **Total Deposits Analyzed:** ₹58.8 Billion
- **Data Quality:** 50.3% cleaning performed, zero missing values

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /path/to/DS_Project_Himanshu/streamlit_app
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure data files exist:**
   Make sure the following directory structure exists in the parent directory:
   ```
   DS_Project_Himanshu/
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
   │   ├── figures/
   │   └── model_results/
   │       ├── model_comparison.csv
   │       ├── project_summary.json
   │       └── data_storytelling_insights.txt
   └── streamlit_app/
       ├── app.py
       ├── requirements.txt
       └── ...
   ```

### Running the Dashboard

```bash
streamlit run app.py
```

The dashboard will automatically open in your default browser at `http://localhost:8501`

## 📱 Dashboard Features

### 🏠 Homepage
- Project overview and key metrics
- Quick navigation guide
- Highlighted achievements

### 📈 EDA (Exploratory Data Analysis)
- Interactive filters (population group, region, state)
- Summary statistics and data preview
- Distribution plots and correlation analysis
- Regional and population group comparisons
- Top states and district analysis

### 🤖 ML Models
- Comparison of 18 machine learning models
- Interactive performance metrics table
- Visualization of R², RMSE, and training time
- Best model showcase with detailed explanation

### 🎯 Predictions
- Interactive prediction tool
- Input infrastructure and location details
- Get instant deposit predictions
- Scenario comparison (compare 2-4 scenarios)
- Reference statistics and insights

### 💡 Insights & Recommendations
- Executive summary of findings
- Key insights across 4 dimensions
- Actionable recommendations for banks and policy makers
- Practical use cases and ROI analysis

### 🗺️ Geographic Insights
- Regional performance analysis
- State-level comparisons
- District finder tool
- Infrastructure efficiency by geography
- Top/bottom performers

### 🔬 Model Interpretability
- Feature importance rankings
- Feature impact direction analysis
- Sample prediction explanations (waterfall charts)
- Feature interaction heatmap
- Practical applications for stakeholders

### 📊 Clustering Analysis
- 4 clustering algorithms compared
- 2D/3D cluster visualizations
- Detailed cluster profiles
- Multi-dimensional comparison
- Business applications and strategies

### 📁 Downloads Center
- Download all datasets (cleaned, featured)
- Download trained models (.pkl files)
- Download visualizations (PNG files)
- Download analysis reports (CSV, JSON, TXT)
- Complete project ZIP archive

## 📂 Project Structure

```
streamlit_app/
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── utils/
│   ├── data_loader.py             # Data loading utilities
│   └── visualizations.py          # Plotly chart functions
└── pages/
    ├── 1_📈_EDA.py                # Exploratory Data Analysis
    ├── 2_🤖_Models.py             # ML Models Comparison
    ├── 3_🎯_Predictions.py        # Interactive Prediction Tool
    ├── 4_💡_Insights.py           # Insights & Recommendations
    ├── 5_🗺️_Geographic.py         # Geographic Analysis
    ├── 6_🔬_Interpretability.py   # Model Interpretability
    ├── 7_📊_Clustering.py         # Clustering Analysis
    └── 8_📁_Downloads.py          # Downloads Center
```

## 🔧 Technology Stack

- **Framework:** Streamlit 1.31.0
- **Data Processing:** Pandas 2.2.3, NumPy 1.26.4
- **Visualization:** Plotly 5.18.0
- **Machine Learning:** Scikit-learn 1.2.2
- **Model Serialization:** Joblib 1.3.2

## 📊 Dataset Information

- **Source:** Population Group-wise Deposits in India
- **Original Records:** 14,037
- **Cleaned Records:** 6,977 (after removing 50.3% zero-deposit records)
- **Features:** 21 (including 6 engineered features)
- **Geographic Coverage:** 36 states, 717 districts
- **Total Deposits:** ₹58.8 Billion

## 🎨 Features Highlights

### Interactive Elements
- 🔍 Dynamic filters and search
- 📊 Real-time data updates
- 🎯 Scenario comparison tools
- 📈 Sortable and filterable tables
- 🗺️ Interactive 2D/3D visualizations

### Data Visualizations
- Distribution plots and histograms
- Correlation heatmaps
- Bar charts and pie charts
- Box plots and scatter plots
- Waterfall charts
- Parallel coordinates
- 3D cluster visualizations

### Download Capabilities
- CSV exports for all data tables
- Model files (.pkl) for deployment
- Visualization images (PNG)
- Analysis reports (CSV, JSON, TXT)
- Complete project archive (ZIP)

## 🤝 Usage Examples

### For Bank Managers
- Identify which factors drive deposits in branches
- Benchmark performance against model patterns
- Plan strategic expansion using predictions
- Segment markets using cluster analysis

### For Data Scientists
- Understand feature engineering approaches
- Explore model comparison methodology
- Learn interpretability techniques
- Reproduce analysis pipeline

### For Policy Makers
- Assess regional banking disparities
- Design targeted financial inclusion programs
- Monitor infrastructure development needs
- Track performance against KPIs

## 📈 Model Performance Summary

| Model                  | R² Score | RMSE (₹)  | MAE (₹) | Time (s) |
|------------------------|----------|-----------|---------|----------|
| Extra Trees            | 0.9976   | 1,402.87  | 444.56  | 0.29     |
| Gradient Boosting      | 0.9936   | 2,290.71  | 1,234.89| 1.45     |
| Decision Tree          | 0.9892   | 2,987.45  | 1,567.23| 0.12     |
| XGBoost (GPU)          | 0.9887   | 3,045.12  | 1,678.34| 0.34     |
| Random Forest          | 0.9876   | 3,198.56  | 1,789.45| 0.67     |

*Top 5 of 18 models trained*

## 🔐 Data Privacy

All data used in this project is aggregated banking statistics. No personal or sensitive information is included.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Dataset: Population Group-wise Deposits in India
- Built with Streamlit, Plotly, and Scikit-learn
- Analysis conducted in Kaggle environment with GPU acceleration

## 📞 Support

For questions or issues:
1. Check the Downloads page for project documentation
2. Review the main.ipynb notebook for detailed analysis
3. Refer to individual page documentation

## 🚀 Future Enhancements

- [ ] Real-time data integration
- [ ] Advanced prediction scenarios
- [ ] Export to PDF reports
- [ ] Mobile-responsive optimizations
- [ ] Additional clustering algorithms
- [ ] Time-series forecasting

---

**Built with ❤️ using Streamlit | Powered by Machine Learning**

*Last Updated: November 2025*
