"""
Dashboard Configuration Settings
Customize colors, titles, and other dashboard settings here
"""

# Dashboard Settings
DASHBOARD_TITLE = "🏢 Business Intelligence Dashboard"
PAGE_ICON = "📊"
LAYOUT = "wide"

# Color Schemes
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e', 
    'success': '#2ca02c',
    'warning': '#d62728',
    'info': '#17becf',
    'light': '#f8f9fa',
    'dark': '#343a40'
}

# Chart Color Palettes
CHART_COLORS = {
    'revenue': 'Blues',
    'opportunities': 'Set3',
    'geographic': 'Viridis',
    'marketing': 'Oranges',
    'financial': 'Greens',
    'status': 'Pastel'
}

# KPI Settings
KPI_CONFIG = {
    'show_delta': True,
    'delta_color': 'normal',
    'number_format': '{:,.0f}',
    'currency_format': '${:,.0f}'
}

# Chart Settings
CHART_CONFIG = {
    'height': 400,
    'show_legend': True,
    'responsive': True,
    'animation': True
}

# Data Settings
DATA_CONFIG = {
    'max_records_display': 100,
    'cache_ttl': 3600,  # 1 hour in seconds
    'date_format': '%Y-%m-%d',
    'datetime_format': '%Y-%m-%d %H:%M:%S'
}

# Filter Settings
FILTER_CONFIG = {
    'default_date_range': 'all',  # 'all', 'last_30_days', 'last_90_days', 'last_year'
    'default_industry': 'All',
    'default_account_type': 'All'
}

# Section Visibility
SECTIONS = {
    'kpis': True,
    'business_analytics': True,
    'advanced_analytics': True,
    'marketing_analytics': True,
    'financial_analytics': True,
    'data_explorer': True
}

# Custom CSS
CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: {primary_color};
        text-align: center;
        margin-bottom: 2rem;
    }
    .kpi-container {
        background-color: {light_color};
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid {primary_color};
        margin: 0.5rem 0;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: {primary_color};
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 2px solid {primary_color};
        padding-bottom: 0.5rem;
    }
</style>
""".format(
    primary_color=COLORS['primary'],
    light_color=COLORS['light']
)

# Data File Paths
DATA_PATHS = {
    'salesforce_accounts': 'rawdata/salesforce_data_20260201_121814.csv',
    'salesforce_opportunities': 'rawdata/salesforce_opportunities_data_20260201_121929.json',
    'sfmc_data': 'rawdata/sfmc_data_20260201_121958.json',
    'netsuite_data': 'rawdata/netsuite_data_20260201_122021.parquet'
}

# Chart Titles
CHART_TITLES = {
    'revenue_by_industry': '💰 Revenue by Industry',
    'opportunities_by_stage': '🎯 Opportunities by Stage',
    'account_creation_trends': '📈 Account Creation Trends',
    'geographic_distribution': '🌍 Geographic Distribution',
    'employee_vs_revenue': '💼 Employee Size vs Revenue',
    'account_type_distribution': '📊 Account Type Distribution',
    'email_events': '📈 Email Event Types',
    'email_timeline': '📅 Email Activity Timeline',
    'transaction_types': '💳 Transaction Types',
    'transaction_status': '📊 Transaction Status'
}

# Export Settings
EXPORT_CONFIG = {
    'enable_csv_export': True,
    'enable_excel_export': True,
    'enable_pdf_export': False,  # Requires additional dependencies
    'max_export_records': 10000
}