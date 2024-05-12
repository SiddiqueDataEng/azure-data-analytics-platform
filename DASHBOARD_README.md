# 📊 Business Intelligence Dashboard

A comprehensive Streamlit dashboard that analyzes your business data to provide Power BI-like insights and visualizations.

## 🚀 Features

### Key Performance Indicators (KPIs)
- **Total Accounts**: Count of all customer accounts
- **Total Annual Revenue**: Sum of all account revenues
- **Active Opportunities**: Number of sales opportunities
- **Pipeline Value**: Total value of sales pipeline

### 📈 Analytics & Visualizations

#### Business Analytics
- **Revenue by Industry**: Horizontal bar chart showing revenue distribution across industries
- **Opportunities by Stage**: Pie chart of sales pipeline stages
- **Account Creation Trends**: Time series showing monthly account creation patterns
- **Geographic Distribution**: Top 10 states by account count

#### Advanced Analytics
- **Employee Size vs Revenue**: Scatter plot correlation analysis
- **Account Type Distribution**: Dual-axis chart showing count vs revenue by account type

#### Marketing Analytics (SFMC)
- **Email Event Types**: Distribution of email marketing events
- **Email Activity Timeline**: Time series of email events by type

#### Financial Analytics (NetSuite)
- **Transaction Types**: Revenue breakdown by transaction type
- **Transaction Status**: Distribution of transaction statuses

### 🔍 Interactive Features
- **Date Range Filter**: Filter data by creation date
- **Industry Filter**: Focus on specific industries
- **Account Type Filter**: Filter by customer, partner, competitor, etc.
- **Data Explorer**: Tabbed view of raw data from all sources

## 📁 Data Sources

The dashboard analyzes data from four main sources:

1. **Salesforce Accounts** (`salesforce_data_*.csv`)
   - Account information, revenue, industry, location
   
2. **Salesforce Opportunities** (`salesforce_opportunities_data_*.json`)
   - Sales pipeline, stages, amounts, probabilities
   
3. **Salesforce Marketing Cloud** (`sfmc_data_*.json`)
   - Email marketing events, campaigns, subscriber activity
   
4. **NetSuite Transactions** (`netsuite_data_*.parquet`)
   - Financial transactions, amounts, types, statuses

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start
1. **Run the dashboard**:
   ```bash
   run_dashboard.bat
   ```
   This will automatically install dependencies and start the dashboard.

### Manual Installation
1. **Install dependencies**:
   ```bash
   pip install -r dashboard_requirements.txt
   ```

2. **Run the dashboard**:
   ```bash
   streamlit run streamlit_dashboard.py
   ```

3. **Open your browser** to `http://localhost:8501`

## 📊 Dashboard Sections

### 1. KPI Overview
Four key metrics displayed prominently at the top:
- Total accounts and revenue figures
- Sales pipeline metrics
- Real-time calculations based on filtered data

### 2. Business Analytics
Core business insights with interactive charts:
- Industry performance analysis
- Sales pipeline visualization
- Growth trends over time
- Geographic distribution

### 3. Advanced Analytics
Deeper insights and correlations:
- Employee count vs revenue analysis
- Account type performance comparison
- Multi-dimensional data exploration

### 4. Marketing Analytics
Email marketing performance from SFMC:
- Event type distribution
- Campaign timeline analysis
- Subscriber engagement metrics

### 5. Financial Analytics
NetSuite transaction analysis:
- Transaction type breakdown
- Status distribution
- Financial performance metrics

### 6. Data Explorer
Raw data access with filtering:
- Searchable and sortable tables
- Export capabilities
- Detailed record inspection

## 🎨 Design Features

### Power BI-Inspired Styling
- Clean, professional layout
- Consistent color scheme
- Interactive filters and controls
- Responsive design for different screen sizes

### User Experience
- Intuitive navigation
- Real-time filtering
- Hover tooltips and details
- Export and sharing capabilities

## 🔧 Customization

### Adding New Visualizations
1. Load your data in the `load_data()` function
2. Add new chart sections in the main dashboard
3. Use Plotly for interactive visualizations

### Modifying Filters
- Edit the sidebar section to add new filter options
- Update the filtering logic in the main function
- Ensure all visualizations respect the new filters

### Styling Changes
- Modify the CSS in the `st.markdown()` section
- Update color schemes in Plotly charts
- Adjust layout columns and spacing

## 📈 Performance Considerations

- **Data Caching**: Uses `@st.cache_data` for efficient data loading
- **Lazy Loading**: Charts render only when needed
- **Memory Management**: Optimized for large datasets
- **Responsive Design**: Adapts to different screen sizes

## 🐛 Troubleshooting

### Common Issues

1. **Data Loading Errors**
   - Ensure all data files exist in the `rawdata/` folder
   - Check file formats match expected schemas
   - Verify file permissions

2. **Package Installation Issues**
   - Update pip: `python -m pip install --upgrade pip`
   - Use virtual environment for clean installation
   - Check Python version compatibility

3. **Performance Issues**
   - Reduce date range for large datasets
   - Clear Streamlit cache: `streamlit cache clear`
   - Close other browser tabs to free memory

### Getting Help
- Check the Streamlit documentation: https://docs.streamlit.io/
- Plotly documentation: https://plotly.com/python/
- Review error messages in the terminal

## 🚀 Future Enhancements

Potential improvements and additions:
- Real-time data connections
- Advanced ML predictions
- Custom report generation
- Mobile-responsive design
- User authentication
- Data export functionality
- Automated refresh scheduling

---

**Dashboard Version**: 1.0  
**Last Updated**: February 2026  
**Compatible with**: Streamlit 1.28+, Python 3.8+