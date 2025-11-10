#!/usr/bin/env python3
"""
🚀 STREAMLIT DASHBOARD - GETTING STARTED 🚀

This script helps you verify your setup and launch the dashboard.
Run this first to check if everything is ready!
"""

import sys
import os
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("\n" + "="*60)
    print("   📊 POPULATION DEPOSITS ANALYSIS DASHBOARD 📊")
    print("="*60 + "\n")

def check_python_version():
    """Check Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Too old!")
        print("   ⚠️  Please install Python 3.8 or higher")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking dependencies...")
    
    required = {
        'streamlit': '1.31.0',
        'pandas': '2.0.0',
        'numpy': '1.20.0',
        'plotly': '5.0.0',
        'sklearn': '1.0.0'
    }
    
    missing = []
    
    for package, min_version in required.items():
        try:
            if package == 'sklearn':
                import sklearn
                print(f"   ✅ scikit-learn {sklearn.__version__}")
            else:
                module = __import__(package)
                version = getattr(module, '__version__', 'unknown')
                print(f"   ✅ {package} {version}")
        except ImportError:
            print(f"   ❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n   ⚠️  Missing packages: {', '.join(missing)}")
        print("   💡 Run: pip install -r requirements.txt")
        return False
    
    return True

def check_file_structure():
    """Check if required data files exist"""
    print("\n🔍 Checking file structure...")
    
    base_path = Path(__file__).parent.parent
    
    required_files = [
        ('data/processed/cleaned_data.csv', 'Cleaned dataset', True),
        ('data/processed/featured_data.csv', 'Featured dataset', True),
        ('models/saved_models/extra_trees.pkl', 'Extra Trees model', True),
        ('models/saved_models/gradient_boosting.pkl', 'Gradient Boosting model', True),
        ('models/saved_models/decision_tree.pkl', 'Decision Tree model', True),
        ('reports/model_results/model_comparison.csv', 'Model comparison', True),
        ('reports/model_results/project_summary.json', 'Project summary', False),
        ('reports/model_results/data_storytelling_insights.txt', 'Insights narrative', False),
    ]
    
    all_ok = True
    
    for file_path, description, required in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            size = full_path.stat().st_size / 1024  # KB
            print(f"   ✅ {description}: {size:.1f} KB")
        else:
            if required:
                print(f"   ❌ {description}: NOT FOUND (Required)")
                all_ok = False
            else:
                print(f"   ⚠️  {description}: NOT FOUND (Optional)")
    
    return all_ok

def check_streamlit_app():
    """Check if Streamlit app files exist"""
    print("\n🔍 Checking Streamlit app files...")
    
    app_files = [
        'app.py',
        'utils/data_loader.py',
        'utils/visualizations.py',
        'pages/1_📈_EDA.py',
        'pages/2_🤖_Models.py',
        'pages/3_🎯_Predictions.py',
        'pages/4_💡_Insights.py',
        'pages/5_🗺️_Geographic.py',
        'pages/6_🔬_Interpretability.py',
        'pages/7_📊_Clustering.py',
        'pages/8_📁_Downloads.py',
    ]
    
    all_ok = True
    count = 0
    
    for file_path in app_files:
        if Path(file_path).exists():
            count += 1
        else:
            print(f"   ❌ {file_path}: NOT FOUND")
            all_ok = False
    
    if all_ok:
        print(f"   ✅ All {count} app files found")
    
    return all_ok

def print_summary(python_ok, deps_ok, files_ok, app_ok):
    """Print summary and next steps"""
    print("\n" + "="*60)
    print("   📋 SETUP SUMMARY")
    print("="*60)
    
    print(f"\n   Python Version:  {'✅ OK' if python_ok else '❌ FAILED'}")
    print(f"   Dependencies:    {'✅ OK' if deps_ok else '❌ FAILED'}")
    print(f"   Data Files:      {'✅ OK' if files_ok else '❌ FAILED'}")
    print(f"   App Files:       {'✅ OK' if app_ok else '❌ FAILED'}")
    
    all_ok = python_ok and deps_ok and files_ok and app_ok
    
    if all_ok:
        print("\n" + "="*60)
        print("   🎉 ALL CHECKS PASSED! YOU'RE READY TO GO! 🎉")
        print("="*60)
        print("\n   🚀 To launch the dashboard, run:\n")
        print("      streamlit run app.py")
        print("\n   Or use the convenience scripts:")
        print("      • Linux/Mac: ./start_dashboard.sh")
        print("      • Windows:   start_dashboard.bat")
        print("\n   📖 For more help, see:")
        print("      • README.md - Complete documentation")
        print("      • QUICK_START.md - Quick start guide")
        print("\n" + "="*60 + "\n")
    else:
        print("\n" + "="*60)
        print("   ⚠️  SETUP INCOMPLETE - PLEASE FIX ISSUES ABOVE")
        print("="*60)
        print("\n   💡 Quick fixes:\n")
        
        if not python_ok:
            print("      1. Install Python 3.8+: https://www.python.org/downloads/")
        
        if not deps_ok:
            print("      2. Install dependencies: pip install -r requirements.txt")
        
        if not files_ok:
            print("      3. Ensure data files are in the correct locations")
            print("         See BUILD_SUMMARY.md for required file structure")
        
        if not app_ok:
            print("      4. Verify all app files exist in streamlit_app/")
        
        print("\n   📖 For detailed help, see README.md or QUICK_START.md")
        print("\n" + "="*60 + "\n")
        
        return False
    
    return True

def main():
    """Main function"""
    print_banner()
    
    # Run checks
    python_ok = check_python_version()
    deps_ok = check_dependencies() if python_ok else False
    files_ok = check_file_structure()
    app_ok = check_streamlit_app()
    
    # Print summary
    ready = print_summary(python_ok, deps_ok, files_ok, app_ok)
    
    # Return exit code
    sys.exit(0 if ready else 1)

if __name__ == "__main__":
    main()
