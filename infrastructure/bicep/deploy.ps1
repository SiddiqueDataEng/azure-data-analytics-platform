# Azure Data Analytics Platform Deployment Script
param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName,
    
    [Parameter(Mandatory=$true)]
    [string]$Location,
    
    [Parameter(Mandatory=$false)]
    [string]$Environment = "dev",
    
    [Parameter(Mandatory=$false)]
    [string]$ProjectName = "azuredataanalytics",
    
    [Parameter(Mandatory=$true)]
    [string]$SqlAdminLogin,
    
    [Parameter(Mandatory=$true)]
    [SecureString]$SqlAdminPassword
)

# Set error action preference
$ErrorActionPreference = "Stop"

Write-Host "Starting Azure Data Analytics Platform deployment..." -ForegroundColor Green

# Check if logged in to Azure
try {
    $context = Get-AzContext
    if (!$context) {
        throw "Not logged in"
    }
    Write-Host "Using Azure subscription: $($context.Subscription.Name)" -ForegroundColor Yellow
}
catch {
    Write-Host "Please login to Azure first using Connect-AzAccount" -ForegroundColor Red
    exit 1
}

# Create resource group if it doesn't exist
try {
    $rg = Get-AzResourceGroup -Name $ResourceGroupName -ErrorAction SilentlyContinue
    if (!$rg) {
        Write-Host "Creating resource group: $ResourceGroupName" -ForegroundColor Yellow
        New-AzResourceGroup -Name $ResourceGroupName -Location $Location
    } else {
        Write-Host "Using existing resource group: $ResourceGroupName" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "Error creating resource group: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Deploy Bicep template
try {
    Write-Host "Deploying Bicep template..." -ForegroundColor Yellow
    
    $deploymentName = "azure-data-analytics-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    
    $deployment = New-AzResourceGroupDeployment `
        -ResourceGroupName $ResourceGroupName `
        -Name $deploymentName `
        -TemplateFile "main.bicep" `
        -location $Location `
        -environment $Environment `
        -projectName $ProjectName `
        -sqlAdminLogin $SqlAdminLogin `
        -sqlAdminPassword $SqlAdminPassword `
        -Verbose
    
    if ($deployment.ProvisioningState -eq "Succeeded") {
        Write-Host "Deployment completed successfully!" -ForegroundColor Green
        
        # Display outputs
        Write-Host "`nDeployment Outputs:" -ForegroundColor Cyan
        Write-Host "Storage Account: $($deployment.Outputs.storageAccountName.Value)" -ForegroundColor White
        Write-Host "Data Factory: $($deployment.Outputs.dataFactoryName.Value)" -ForegroundColor White
        Write-Host "SQL Server: $($deployment.Outputs.sqlServerName.Value)" -ForegroundColor White
        Write-Host "SQL Database: $($deployment.Outputs.sqlDatabaseName.Value)" -ForegroundColor White
        Write-Host "Key Vault: $($deployment.Outputs.keyVaultName.Value)" -ForegroundColor White
        
        # Save outputs to file
        $outputs = @{
            storageAccountName = $deployment.Outputs.storageAccountName.Value
            dataFactoryName = $deployment.Outputs.dataFactoryName.Value
            sqlServerName = $deployment.Outputs.sqlServerName.Value
            sqlDatabaseName = $deployment.Outputs.sqlDatabaseName.Value
            keyVaultName = $deployment.Outputs.keyVaultName.Value
            resourceGroupName = $deployment.Outputs.resourceGroupName.Value
        }
        
        $outputs | ConvertTo-Json | Out-File -FilePath "deployment-outputs.json" -Encoding UTF8
        Write-Host "`nDeployment outputs saved to deployment-outputs.json" -ForegroundColor Green
        
    } else {
        Write-Host "Deployment failed with state: $($deployment.ProvisioningState)" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "Error during deployment: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Configure Data Factory pipelines" -ForegroundColor White
Write-Host "2. Set up source system connections" -ForegroundColor White
Write-Host "3. Deploy database schemas" -ForegroundColor White
Write-Host "4. Configure Power BI datasets" -ForegroundColor White