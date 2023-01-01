# Azure Data Analytics Platform - Deployment Guide

## Prerequisites

### Azure Subscription Requirements
- Active Azure subscription with sufficient credits
- Contributor or Owner role on the subscription
- Resource quotas for the following services:
  - Azure Data Factory
  - Azure SQL Database
  - Azure Storage Account
  - Azure Key Vault

### Development Environment
- Azure CLI 2.50+ or Azure PowerShell 9.0+
- Power BI Desktop (latest version)
- SQL Server Management Studio or Azure Data Studio
- Git for version control
- Python 3.8+ (for data generator)

### Service Principal Setup
Create a service principal for automated deployments:
```bash
az ad sp create-for-rbac --name "azure-data-analytics-sp" --role contributor --scopes /subscriptions/{subscription-id}
```

## Deployment Steps

### Step 1: Clone Repository
```bash
git clone https://github.com/your-org/azure-data-analytics-platform.git
cd azure-data-analytics-platform
```

### Step 2: Configure Environment Variables
Create a `.env` file in the root directory:
```bash
# Azure Configuration
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret

# Resource Configuration
RESOURCE_GROUP_NAME=azure-data-analytics-rg
LOCATION=eastus
ENVIRONMENT=dev
PROJECT_NAME=azuredataanalytics

# SQL Configuration
SQL_ADMIN_LOGIN=sqladmin
SQL_ADMIN_PASSWORD=YourSecurePassword123!

# Source System Configuration
SALESFORCE_USERNAME=your-sf-username
SALESFORCE_PASSWORD=your-sf-password
SALESFORCE_SECURITY_TOKEN=your-sf-token
SFMC_CLIENT_ID=your-sfmc-client-id
SFMC_CLIENT_SECRET=your-sfmc-client-secret
NETSUITE_ACCOUNT_ID=your-ns-account-id
NETSUITE_CONSUMER_KEY=your-ns-consumer-key
NETSUITE_CONSUMER_SECRET=your-ns-consumer-secret
```

### Step 3: Deploy Infrastructure

#### Option A: Using Bicep
```powershell
# Navigate to Bicep directory
cd infrastructure/bicep

# Login to Azure
Connect-AzAccount

# Run deployment script
./deploy.ps1 -ResourceGroupName "azure-data-analytics-rg" -Location "eastus" -SqlAdminLogin "sqladmin" -SqlAdminPassword (ConvertTo-SecureString "YourSecurePassword123!" -AsPlainText -Force)
```

#### Option B: Using Terraform
```bash
# Navigate to Terraform directory
cd infrastructure/terraform

# Initialize Terraform
terraform init

# Copy and configure variables
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# Plan deployment
terraform plan

# Apply deployment
terraform apply
```

### Step 4: Configure Data Factory

#### Create Linked Services
1. **Salesforce Linked Service**
```json
{
    "name": "Salesforce_LinkedService",
    "type": "Microsoft.DataFactory/factories/linkedservices",
    "properties": {
        "type": "Salesforce",
        "typeProperties": {
            "environmentUrl": "https://login.salesforce.com",
            "username": "@{linkedService().username}",
            "password": {
                "type": "AzureKeyVaultSecret",
                "store": {
                    "referenceName": "KeyVault_LinkedService",
                    "type": "LinkedServiceReference"
                },
                "secretName": "salesforce-password"
            },
            "securityToken": {
                "type": "AzureKeyVaultSecret",
                "store": {
                    "referenceName": "KeyVault_LinkedService",
                    "type": "LinkedServiceReference"
                },
                "secretName": "salesforce-security-token"
            }
        }
    }
}
```

2. **Azure SQL Database Linked Service**
```json
{
    "name": "AzureSQL_LinkedService",
    "type": "Microsoft.DataFactory/factories/linkedservices",
    "properties": {
        "type": "AzureSqlDatabase",
        "typeProperties": {
            "connectionString": {
                "type": "AzureKeyVaultSecret",
                "store": {
                    "referenceName": "KeyVault_LinkedService",
                    "type": "LinkedServiceReference"
                },
                "secretName": "sql-connection-string"
            }
        }
    }
}
```

#### Deploy Pipelines
```bash
# Use Azure CLI to deploy pipelines
az datafactory pipeline create --factory-name "your-adf-name" --resource-group "your-rg" --name "Salesforce_Ingestion_Pipeline" --pipeline @pipelines/adf-templates/salesforce-ingestion-pipeline.json
```

### Step 5: Initialize Database Schema
```bash
# Connect to Azure SQL Database and run schema scripts
sqlcmd -S your-sql-server.database.windows.net -d your-database -U sqladmin -P YourSecurePassword123! -i data-models/sql-schemas/01-create-schemas.sql
sqlcmd -S your-sql-server.database.windows.net -d your-database -U sqladmin -P YourSecurePassword123! -i data-models/sql-schemas/02-populate-date-dimension.sql
```

### Step 6: Configure Data Generator (Optional)
```bash
# Navigate to data generator directory
cd data-generator

# Install Python dependencies
pip install -r requirements.txt

# Run the Flask application
python app.py
```
Access the data generator at `http://localhost:5000`

### Step 7: Set Up Monitoring and Alerting

#### Configure Azure Monitor
```bash
# Create action group for notifications
az monitor action-group create --name "DataPlatformAlerts" --resource-group "azure-data-analytics-rg" --short-name "DataAlerts"

# Create alert rules
az monitor metrics alert create --name "ADF Pipeline Failure" --resource-group "azure-data-analytics-rg" --scopes "/subscriptions/{subscription-id}/resourceGroups/azure-data-analytics-rg/providers/Microsoft.DataFactory/factories/your-adf-name" --condition "count Microsoft.DataFactory/factories/PipelineFailedRuns > 0" --action "/subscriptions/{subscription-id}/resourceGroups/azure-data-analytics-rg/providers/microsoft.insights/actionGroups/DataPlatformAlerts"
```

### Step 8: Configure Power BI

#### Create Power BI Workspace
1. Log in to Power BI Service
2. Create new workspace: "Azure Data Analytics"
3. Configure workspace settings for collaboration

#### Deploy Data Models
1. Open Power BI Desktop
2. Connect to Azure SQL Database
3. Import data model from `powerbi/` directory
4. Publish to Power BI Service

#### Configure Scheduled Refresh
1. In Power BI Service, go to dataset settings
2. Configure data source credentials
3. Set up scheduled refresh (daily at 7 AM)

## Post-Deployment Configuration

### Security Configuration

#### Configure Row-Level Security
```sql
-- Create security roles in Power BI
CREATE ROLE "Sales Team"
CREATE ROLE "Marketing Team"
CREATE ROLE "Executive Team"

-- Configure RLS filters
[AccountOwner] = USERNAME()
[Department] = LOOKUPVALUE(Users[Department], Users[Email], USERNAME())
```

#### Set Up Key Vault Secrets
```bash
# Store sensitive configuration in Key Vault
az keyvault secret set --vault-name "your-keyvault-name" --name "salesforce-username" --value "your-sf-username"
az keyvault secret set --vault-name "your-keyvault-name" --name "salesforce-password" --value "your-sf-password"
az keyvault secret set --vault-name "your-keyvault-name" --name "salesforce-security-token" --value "your-sf-token"
```

### Performance Optimization

#### Configure Auto-Scaling
```bash
# Enable auto-scaling for SQL Database
az sql db update --resource-group "azure-data-analytics-rg" --server "your-sql-server" --name "your-database" --service-objective "S2" --auto-pause-delay 60
```

#### Set Up Data Retention Policies
```sql
-- Configure data retention policies
ALTER TABLE salesforce.Account SET (SYSTEM_VERSIONING = ON (HISTORY_RETENTION_PERIOD = 2 YEARS))
```

## Testing and Validation

### Data Pipeline Testing
```bash
# Trigger test pipeline run
az datafactory pipeline create-run --factory-name "your-adf-name" --resource-group "your-rg" --name "Salesforce_Ingestion_Pipeline"

# Monitor pipeline execution
az datafactory pipeline-run show --factory-name "your-adf-name" --resource-group "your-rg" --run-id "your-run-id"
```

### Data Quality Validation
```sql
-- Validate data quality
SELECT 
    COUNT(*) as TotalRecords,
    COUNT(CASE WHEN Name IS NULL THEN 1 END) as MissingNames,
    COUNT(CASE WHEN CreatedDate IS NULL THEN 1 END) as MissingDates
FROM salesforce.Account
WHERE LoadDate >= DATEADD(day, -1, GETUTCDATE())
```

### Power BI Report Testing
1. Verify data refresh functionality
2. Test report performance with sample data
3. Validate security roles and permissions
4. Test mobile responsiveness

## Troubleshooting

### Common Issues

#### Pipeline Failures
```bash
# Check pipeline run details
az datafactory pipeline-run query-by-factory --factory-name "your-adf-name" --resource-group "your-rg" --last-updated-after "2024-01-01" --last-updated-before "2024-12-31"
```

#### Connection Issues
- Verify firewall rules for Azure SQL Database
- Check Key Vault access policies
- Validate service principal permissions

#### Performance Issues
- Monitor SQL Database DTU usage
- Check Data Factory integration runtime performance
- Analyze Power BI query performance

### Monitoring Commands
```bash
# Check resource health
az resource list --resource-group "azure-data-analytics-rg" --query "[].{Name:name, Type:type, Location:location, Status:properties.provisioningState}"

# Monitor costs
az consumption usage list --start-date "2024-01-01" --end-date "2024-01-31"
```

## Maintenance Tasks

### Daily Tasks
- Monitor pipeline execution status
- Check data quality metrics
- Review error logs and alerts

### Weekly Tasks
- Analyze performance metrics
- Review cost optimization opportunities
- Update documentation as needed

### Monthly Tasks
- Security review and access audit
- Performance optimization review
- Backup and disaster recovery testing

## Support and Documentation

### Additional Resources
- [Azure Data Factory Documentation](https://docs.microsoft.com/en-us/azure/data-factory/)
- [Power BI Documentation](https://docs.microsoft.com/en-us/power-bi/)
- [Azure SQL Database Documentation](https://docs.microsoft.com/en-us/azure/azure-sql/)

### Getting Help
- Azure Support Portal for infrastructure issues
- Power BI Community for reporting questions
- Internal documentation wiki for platform-specific guidance

## Conclusion
This deployment guide provides step-by-step instructions for setting up the Azure Data Analytics Platform. Follow the procedures carefully and refer to the troubleshooting section for common issues. Regular maintenance and monitoring will ensure optimal platform performance.