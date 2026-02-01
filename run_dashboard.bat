@echo off
echo Installing required packages...
pip install -r dashboard_requirements.txt

echo.
echo Starting Streamlit Dashboard...
echo Dashboard will open in your browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the dashboard
echo.

streamlit run streamlit_dashboard.py