# Azure Data Analytics Platform

A comprehensive data analytics solution integrating Salesforce, Salesforce Marketing Cloud (SFMC), and NetSuite data into Azure for Power BI consumption.

## Project Structure

```
├── data-generator/          # Flask app for generating mock data
├── infrastructure/          # Azure infrastructure templates
│   ├── bicep/              # Bicep templates
│   └── terraform/          # Terraform templates
├── pipelines/              # Azure Data Factory pipelines
├── data-models/            # Data modeling and schemas
├── powerbi/               # Power BI templates and documentation
└── docs/                  # Architecture and documentation
```

## Components

### 1. Data Generator
- Flask web UI for generating realistic mock data
- Supports Salesforce, SFMC, and NetSuite data formats
- Configurable date ranges and record counts
- Multiple export formats (JSON, CSV, Parquet)

### 2. Azure Infrastructure
- Azure Data Factory for data ingestion
- Azure Data Lake Gen2 for data storage
- Azure SQL Database for analytics
- Azure Key Vault for secrets management
- Azure Monitor for logging and alerting

### 3. Data Pipelines
- Incremental data loads
- Error handling and retry logic
- Data quality validation
- Monitoring and alerting

### 4. Power BI Integration
- Optimized data models
- Refresh patterns
- Performance optimization

## Quick Start

1. Deploy infrastructure: `cd infrastructure/bicep && az deployment group create...`
2. Run data generator: `cd data-generator && python app.py`
3. Configure ADF pipelines
4. Connect Power BI

## Documentation

See `/docs` folder for detailed architecture, setup guides, and operational procedures.