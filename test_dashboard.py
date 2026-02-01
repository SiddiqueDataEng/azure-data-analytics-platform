#!/usr/bin/env python3
"""
Test script to verify dashboard data loading and basic functionality
"""

import pandas as pd
import json
import sys
from pathlib import Path

def test_data_loading():
    """Test if all data files can be loaded successfully"""
    print("🧪 Testing Dashboard Data Loading...")
    print("=" * 50)
    
    errors = []
    
    # Test Salesforce Accounts CSV
    try:
        sf_accounts = pd.read_csv('rawdata/salesforce_data_20260201_121814.csv')
        print(f"✅ Salesforce Accounts: {len(sf_accounts)} records loaded")
        print(f"   Columns: {list(sf_accounts.columns)}")
        print(f"   Date range: {sf_accounts['CreatedDate'].min()} to {sf_accounts['CreatedDate'].max()}")
    except Exception as e:
        errors.append(f"❌ Salesforce Accounts: {str(e)}")
    
    # Test Salesforce Opportunities JSON
    try:
        with open('rawdata/salesforce_opportunities_data_20260201_121929.json', 'r') as f:
            sf_opportunities = pd.DataFrame(json.load(f))
        print(f"✅ Salesforce Opportunities: {len(sf_opportunities)} records loaded")
        print(f"   Columns: {list(sf_opportunities.columns)}")
    except Exception as e:
        errors.append(f"❌ Salesforce Opportunities: {str(e)}")
    
    # Test SFMC JSON
    try:
        with open('rawdata/sfmc_data_20260201_121958.json', 'r') as f:
            sfmc_data = pd.DataFrame(json.load(f))
        print(f"✅ SFMC Data: {len(sfmc_data)} records loaded")
        print(f"   Event types: {sfmc_data['EventType'].unique()}")
    except Exception as e:
        errors.append(f"❌ SFMC Data: {str(e)}")
    
    # Test NetSuite Parquet
    try:
        netsuite_data = pd.read_parquet('rawdata/netsuite_data_20260201_122021.parquet')
        print(f"✅ NetSuite Data: {len(netsuite_data)} records loaded")
        print(f"   Transaction types: {netsuite_data['Type'].unique()}")
        print(f"   Amount range: ${netsuite_data['Amount'].min():,.2f} to ${netsuite_data['Amount'].max():,.2f}")
    except Exception as e:
        errors.append(f"❌ NetSuite Data: {str(e)}")
    
    print("\n" + "=" * 50)
    
    if errors:
        print("❌ ERRORS FOUND:")
        for error in errors:
            print(f"   {error}")
        return False
    else:
        print("✅ ALL DATA SOURCES LOADED SUCCESSFULLY!")
        print("\n🚀 Ready to run the dashboard:")
        print("   python -m streamlit run streamlit_dashboard.py")
        print("   or")
        print("   run_dashboard.bat")
        return True

def check_requirements():
    """Check if required packages are available"""
    print("\n📦 Checking Required Packages...")
    print("=" * 50)
    
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'plotly', 'pyarrow'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - NOT INSTALLED")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("💡 Install with: pip install -r dashboard_requirements.txt")
        return False
    else:
        print("\n✅ All required packages are installed!")
        return True

if __name__ == "__main__":
    print("🧪 Dashboard Test Suite")
    print("=" * 50)
    
    # Check if rawdata directory exists
    if not Path('rawdata').exists():
        print("❌ rawdata directory not found!")
        print("💡 Make sure you're running this from the project root directory")
        sys.exit(1)
    
    # Run tests
    packages_ok = check_requirements()
    data_ok = test_data_loading()
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    if packages_ok and data_ok:
        print("✅ ALL TESTS PASSED!")
        print("🚀 Dashboard is ready to run!")
        print("\nNext steps:")
        print("1. Run: run_dashboard.bat")
        print("2. Open browser to: http://localhost:8501")
        print("3. Explore your data!")
    else:
        print("❌ SOME TESTS FAILED")
        print("💡 Please fix the issues above before running the dashboard")
        sys.exit(1)