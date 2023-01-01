# Azure Data Analytics - Data Generator

A Flask web application for generating realistic mock data from Salesforce, Salesforce Marketing Cloud (SFMC), and NetSuite systems.

## Features

- 🎯 **Realistic Data Generation**: Creates authentic-looking data with proper relationships
- 📊 **Multiple Data Sources**: Supports Salesforce CRM, SFMC, and NetSuite
- 📅 **Configurable Date Ranges**: Generate data between any two dates (2022-2025 supported)
- 🔢 **Flexible Record Counts**: Set minimum and maximum record counts for random generation
- 📁 **Multiple Export Formats**: JSON, CSV, and Parquet formats
- 🌐 **Web Interface**: Easy-to-use web UI for configuration and download

## Quick Start

### Prerequisites

1. **UV Package Installer** (Recommended - faster than pip)
   ```bash
   # Install UV using PowerShell (Windows)
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or using Scoop
   scoop install uv
   
   # Or using Chocolatey
   choco install uv
   ```

2. **Python 3.8+** (UV will handle this if not available)

### Option 1: Automated Setup (Recommended)

Simply run the setup script:
```bash
setup-and-run.bat
```

This will:
- ✅ Check for UV installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Start the Flask application

### Option 2: Manual Setup

1. **Create Virtual Environment**
   ```bash
   uv venv venv
   venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Run Application**
   ```bash
   python app.py
   ```

### Option 3: Quick Start (Environment Already Set Up)

If you've already set up the environment:
```bash
start.bat
```

## Usage

1. **Access the Web Interface**
   - Open your browser to `http://localhost:5000`

2. **Select Data Source**
   - Salesforce CRM (Accounts, Contacts, Leads)
   - Salesforce Opportunities (Sales Pipeline)
   - Salesforce Marketing Cloud (Email Events)
   - NetSuite ERP (Financial Transactions)

3. **Configure Parameters**
   - **Date Range**: Start and end dates for data generation
   - **Record Count**: Minimum and maximum number of records
   - **Output Format**: JSON, CSV, or Parquet

4. **Generate and Download**
   - Click "Generate Data" button
   - Download the generated file

## Data Types Generated

### Salesforce CRM Data
- **Accounts**: Company information, billing details, industry classification
- **Fields**: Id, Name, Type, Industry, AnnualRevenue, NumberOfEmployees, Address, Phone, Website

### Salesforce Opportunities
- **Sales Pipeline**: Opportunity stages, amounts, probabilities, close dates
- **Fields**: Id, Name, AccountId, StageName, Amount, Probability, CloseDate, Type, LeadSource

### Salesforce Marketing Cloud (SFMC)
- **Email Events**: Send, Open, Click, Bounce, Unsubscribe events
- **Fields**: JobID, SubscriberKey, EmailAddress, EventDate, EventType, Subject, URL

### NetSuite ERP
- **Transactions**: Sales orders, invoices, purchase orders, financial data
- **Fields**: InternalId, TransactionNumber, Type, Status, Amount, Currency, Department

## File Structure

```
data-generator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── setup-and-run.bat     # Automated setup script
├── start.bat             # Quick start script
├── run.bat               # Alternative run script
├── templates/
│   └── index.html        # Web interface template
├── temp/                 # Generated files directory
└── README.md             # This file
```

## Configuration

### Environment Variables (Optional)
```bash
# Flask configuration
FLASK_ENV=development
FLASK_DEBUG=1

# Application settings
DATA_GENERATOR_HOST=0.0.0.0
DATA_GENERATOR_PORT=5000
```

### Customizing Data Generation

Edit `app.py` to modify data generation logic:

```python
# Modify data patterns in DataGenerator class
def generate_salesforce_data(self, start_date, end_date, min_records, max_records):
    # Customize field generation logic here
    pass
```

## API Endpoints

### Web Interface
- `GET /` - Main web interface

### Data Generation API
- `POST /generate` - Generate data
  ```json
  {
    "system": "salesforce|salesforce_opportunities|sfmc|netsuite",
    "startDate": "2022-01-01",
    "endDate": "2025-12-31",
    "minRecords": 1000,
    "maxRecords": 10000,
    "format": "json|csv|parquet"
  }
  ```

### File Download
- `GET /download/<filename>` - Download generated file

## Troubleshooting

### Common Issues

1. **UV Not Found**
   ```
   ERROR: UV package installer not found!
   ```
   **Solution**: Install UV using one of the methods in Prerequisites

2. **Virtual Environment Issues**
   ```
   ERROR: Failed to create virtual environment
   ```
   **Solution**: Delete existing `venv` folder and run setup script again

3. **Port Already in Use**
   ```
   Address already in use
   ```
   **Solution**: Change port in `app.py` or kill existing Flask processes

4. **Permission Errors**
   ```
   Permission denied
   ```
   **Solution**: Run command prompt as Administrator

### Performance Tips

- **Large Datasets**: For >100K records, use Parquet format for better performance
- **Memory Usage**: Close browser tabs when generating large datasets
- **Storage**: Generated files are stored in `temp/` directory

### Logs and Debugging

Enable debug mode by setting:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Integration with Azure Data Platform

Generated data can be used to:
- Test Azure Data Factory pipelines
- Validate Power BI reports
- Load test Azure SQL Database
- Simulate real-world data scenarios

### Upload to Azure Data Lake

```bash
# Example: Upload to Azure Data Lake using Azure CLI
az storage blob upload --account-name mystorageaccount --container-name raw --name salesforce/accounts.parquet --file temp/salesforce_data_20240101_120000.parquet
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

This project is part of the Azure Data Analytics Platform solution.

## Support

For issues and questions:
- Check troubleshooting section above
- Review application logs
- Contact platform team

---

**Happy Data Generating! 🚀**