import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Business Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Power BI-like styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .kpi-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
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
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load all data sources"""
    try:
        # Load Salesforce Accounts
        sf_accounts = pd.read_csv('rawdata/salesforce_data_20260201_121814.csv')
        sf_accounts['CreatedDate'] = pd.to_datetime(sf_accounts['CreatedDate'])
        sf_accounts['LastModifiedDate'] = pd.to_datetime(sf_accounts['LastModifiedDate'])
        
        # Load Salesforce Opportunities
        with open('rawdata/salesforce_opportunities_data_20260201_121929.json', 'r') as f:
            sf_opportunities = pd.DataFrame(json.load(f))
        sf_opportunities['CreatedDate'] = pd.to_datetime(sf_opportunities['CreatedDate'])
        sf_opportunities['CloseDate'] = pd.to_datetime(sf_opportunities['CloseDate'])
        sf_opportunities['LastModifiedDate'] = pd.to_datetime(sf_opportunities['LastModifiedDate'])
        
        # Load SFMC Data
        with open('rawdata/sfmc_data_20260201_121958.json', 'r') as f:
            sfmc_data = pd.DataFrame(json.load(f))
        sfmc_data['EventDate'] = pd.to_datetime(sfmc_data['EventDate'])
        
        # Load NetSuite Data
        netsuite_data = pd.read_parquet('rawdata/netsuite_data_20260201_122021.parquet')
        netsuite_data['TranDate'] = pd.to_datetime(netsuite_data['TranDate'])
        netsuite_data['CreatedDate'] = pd.to_datetime(netsuite_data['CreatedDate'])
        netsuite_data['DueDate'] = pd.to_datetime(netsuite_data['DueDate'])
        
        return sf_accounts, sf_opportunities, sfmc_data, netsuite_data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None, None

def create_kpi_card(title, value, delta=None, delta_color="normal"):
    """Create a KPI card"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{title}</div>
        </div>
        """, unsafe_allow_html=True)
    
    if delta:
        with col2:
            st.metric("", "", delta, delta_color=delta_color)

def main():
    # Header
    st.markdown('<h1 class="main-header">🏢 Business Intelligence Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    sf_accounts, sf_opportunities, sfmc_data, netsuite_data = load_data()
    
    if sf_accounts is None:
        st.error("Failed to load data. Please check if all data files exist in the rawdata folder.")
        return
    
    # Sidebar filters
    st.sidebar.header("📊 Dashboard Filters")
    
    # Date range filter
    min_date = min(sf_accounts['CreatedDate'].min(), sf_opportunities['CreatedDate'].min())
    max_date = max(sf_accounts['CreatedDate'].max(), sf_opportunities['CreatedDate'].max())
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date.date(), max_date.date()),
        min_value=min_date.date(),
        max_value=max_date.date()
    )
    
    # Industry filter
    industries = ['All'] + sorted(sf_accounts['Industry'].dropna().unique().tolist())
    selected_industry = st.sidebar.selectbox("Select Industry", industries)
    
    # Account type filter
    account_types = ['All'] + sorted(sf_accounts['Type'].dropna().unique().tolist())
    selected_type = st.sidebar.selectbox("Select Account Type", account_types)
    
    # Apply filters
    filtered_accounts = sf_accounts.copy()
    filtered_opportunities = sf_opportunities.copy()
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_accounts = filtered_accounts[
            (filtered_accounts['CreatedDate'].dt.date >= start_date) &
            (filtered_accounts['CreatedDate'].dt.date <= end_date)
        ]
        filtered_opportunities = filtered_opportunities[
            (filtered_opportunities['CreatedDate'].dt.date >= start_date) &
            (filtered_opportunities['CreatedDate'].dt.date <= end_date)
        ]
    
    if selected_industry != 'All':
        filtered_accounts = filtered_accounts[filtered_accounts['Industry'] == selected_industry]
    
    if selected_type != 'All':
        filtered_accounts = filtered_accounts[filtered_accounts['Type'] == selected_type]
    
    # KPI Section
    st.markdown('<div class="section-header">📈 Key Performance Indicators</div>', unsafe_allow_html=True)
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        total_accounts = len(filtered_accounts)
        create_kpi_card("Total Accounts", f"{total_accounts:,}")
    
    with kpi_col2:
        total_revenue = filtered_accounts['AnnualRevenue'].sum()
        create_kpi_card("Total Annual Revenue", f"${total_revenue:,.0f}")
    
    with kpi_col3:
        total_opportunities = len(filtered_opportunities)
        create_kpi_card("Active Opportunities", f"{total_opportunities:,}")
    
    with kpi_col4:
        total_opp_value = filtered_opportunities['Amount'].sum()
        create_kpi_card("Pipeline Value", f"${total_opp_value:,.0f}")
    
    # Charts Section
    st.markdown('<div class="section-header">📊 Business Analytics</div>', unsafe_allow_html=True)
    
    # Row 1: Revenue and Opportunities Analysis
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("💰 Revenue by Industry")
        industry_revenue = filtered_accounts.groupby('Industry')['AnnualRevenue'].sum().sort_values(ascending=False)
        fig_industry = px.bar(
            x=industry_revenue.values,
            y=industry_revenue.index,
            orientation='h',
            title="Annual Revenue by Industry",
            labels={'x': 'Annual Revenue ($)', 'y': 'Industry'},
            color=industry_revenue.values,
            color_continuous_scale='Blues'
        )
        fig_industry.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_industry, use_container_width=True)
    
    with chart_col2:
        st.subheader("🎯 Opportunities by Stage")
        stage_counts = filtered_opportunities['StageName'].value_counts()
        fig_stage = px.pie(
            values=stage_counts.values,
            names=stage_counts.index,
            title="Opportunities Distribution by Stage",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_stage.update_layout(height=400)
        st.plotly_chart(fig_stage, use_container_width=True)
    
    # Row 2: Trends and Geographic Analysis
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        st.subheader("📈 Account Creation Trends")
        # Monthly account creation trend
        filtered_accounts['YearMonth'] = filtered_accounts['CreatedDate'].dt.to_period('M')
        monthly_accounts = filtered_accounts.groupby('YearMonth').size()
        
        fig_trend = px.line(
            x=monthly_accounts.index.astype(str),
            y=monthly_accounts.values,
            title="Monthly Account Creation Trend",
            labels={'x': 'Month', 'y': 'Number of Accounts'}
        )
        fig_trend.update_layout(height=400)
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with chart_col4:
        st.subheader("🌍 Geographic Distribution")
        state_counts = filtered_accounts['BillingState'].value_counts().head(10)
        fig_geo = px.bar(
            x=state_counts.index,
            y=state_counts.values,
            title="Top 10 States by Account Count",
            labels={'x': 'State', 'y': 'Number of Accounts'},
            color=state_counts.values,
            color_continuous_scale='Viridis'
        )
        fig_geo.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_geo, use_container_width=True)
    
    # Row 3: Advanced Analytics
    st.markdown('<div class="section-header">🔍 Advanced Analytics</div>', unsafe_allow_html=True)
    
    adv_col1, adv_col2 = st.columns(2)
    
    with adv_col1:
        st.subheader("💼 Employee Size vs Revenue")
        fig_scatter = px.scatter(
            filtered_accounts,
            x='NumberOfEmployees',
            y='AnnualRevenue',
            color='Industry',
            size='AnnualRevenue',
            hover_data=['Name', 'Type'],
            title="Employee Count vs Annual Revenue",
            labels={'NumberOfEmployees': 'Number of Employees', 'AnnualRevenue': 'Annual Revenue ($)'}
        )
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with adv_col2:
        st.subheader("📊 Account Type Distribution")
        type_revenue = filtered_accounts.groupby('Type')['AnnualRevenue'].agg(['count', 'sum']).reset_index()
        type_revenue.columns = ['Type', 'Count', 'Total_Revenue']
        
        fig_type = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_type.add_trace(
            go.Bar(x=type_revenue['Type'], y=type_revenue['Count'], name="Account Count"),
            secondary_y=False,
        )
        
        fig_type.add_trace(
            go.Scatter(x=type_revenue['Type'], y=type_revenue['Total_Revenue'], 
                      mode='lines+markers', name="Total Revenue", line=dict(color='red')),
            secondary_y=True,
        )
        
        fig_type.update_xaxes(title_text="Account Type")
        fig_type.update_yaxes(title_text="Number of Accounts", secondary_y=False)
        fig_type.update_yaxes(title_text="Total Revenue ($)", secondary_y=True)
        fig_type.update_layout(title_text="Account Count vs Revenue by Type", height=400)
        
        st.plotly_chart(fig_type, use_container_width=True)
    
    # Marketing Analytics Section
    st.markdown('<div class="section-header">📧 Marketing Analytics (SFMC)</div>', unsafe_allow_html=True)
    
    marketing_col1, marketing_col2 = st.columns(2)
    
    with marketing_col1:
        st.subheader("📈 Email Event Types")
        event_counts = sfmc_data['EventType'].value_counts()
        fig_events = px.bar(
            x=event_counts.index,
            y=event_counts.values,
            title="Email Event Distribution",
            labels={'x': 'Event Type', 'y': 'Count'},
            color=event_counts.values,
            color_continuous_scale='Oranges'
        )
        fig_events.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_events, use_container_width=True)
    
    with marketing_col2:
        st.subheader("📅 Email Activity Timeline")
        sfmc_data['EventMonth'] = sfmc_data['EventDate'].dt.to_period('M')
        monthly_events = sfmc_data.groupby(['EventMonth', 'EventType']).size().reset_index(name='Count')
        monthly_events['EventMonth'] = monthly_events['EventMonth'].astype(str)
        
        fig_timeline = px.line(
            monthly_events,
            x='EventMonth',
            y='Count',
            color='EventType',
            title="Email Events Over Time",
            labels={'EventMonth': 'Month', 'Count': 'Number of Events'}
        )
        fig_timeline.update_layout(height=400)
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    # NetSuite Financial Analytics
    st.markdown('<div class="section-header">💰 Financial Analytics (NetSuite)</div>', unsafe_allow_html=True)
    
    finance_col1, finance_col2 = st.columns(2)
    
    with finance_col1:
        st.subheader("💳 Transaction Types")
        transaction_summary = netsuite_data.groupby('Type').agg({
            'Amount': ['count', 'sum', 'mean']
        }).round(2)
        transaction_summary.columns = ['Count', 'Total_Amount', 'Avg_Amount']
        transaction_summary = transaction_summary.reset_index()
        
        fig_trans = px.bar(
            transaction_summary,
            x='Type',
            y='Total_Amount',
            title="Total Amount by Transaction Type",
            labels={'Type': 'Transaction Type', 'Total_Amount': 'Total Amount ($)'},
            color='Total_Amount',
            color_continuous_scale='Greens'
        )
        fig_trans.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_trans, use_container_width=True)
    
    with finance_col2:
        st.subheader("📊 Transaction Status")
        status_counts = netsuite_data['Status'].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Transaction Status Distribution",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_status.update_layout(height=400)
        st.plotly_chart(fig_status, use_container_width=True)
    
    # Data Tables Section
    st.markdown('<div class="section-header">📋 Data Explorer</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Accounts", "🎯 Opportunities", "📧 Marketing", "💰 Transactions"])
    
    with tab1:
        st.subheader("Salesforce Accounts")
        st.dataframe(
            filtered_accounts[['Name', 'Type', 'Industry', 'AnnualRevenue', 'NumberOfEmployees', 
                             'BillingState', 'CreatedDate']].head(100),
            use_container_width=True
        )
    
    with tab2:
        st.subheader("Sales Opportunities")
        st.dataframe(
            filtered_opportunities[['Name', 'StageName', 'Amount', 'Probability', 
                                  'CloseDate', 'Type', 'LeadSource']].head(100),
            use_container_width=True
        )
    
    with tab3:
        st.subheader("Marketing Events (SFMC)")
        st.dataframe(
            sfmc_data[['EmailAddress', 'EventType', 'EventDate', 'Subject', 
                      'FromName', 'SendID']].head(100),
            use_container_width=True
        )
    
    with tab4:
        st.subheader("Financial Transactions (NetSuite)")
        st.dataframe(
            netsuite_data[['TransactionNumber', 'Type', 'Status', 'Amount', 
                          'TranDate', 'Entity', 'Subsidiary']].head(100),
            use_container_width=True
        )
    
    # Footer
    st.markdown("---")
    st.markdown("**📊 Business Intelligence Dashboard** | Data refreshed: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main()