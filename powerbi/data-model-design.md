# Power BI Data Model Design

## Overview
This document outlines the data model design for the Azure Data Analytics Platform Power BI reports, optimized for performance and usability.

## Data Model Architecture

### Star Schema Design
The data model follows a star schema pattern with:
- **Fact Tables**: FactSales, FactMarketing
- **Dimension Tables**: DimDate, DimAccount, DimProduct, DimCustomer

### Key Design Principles
1. **Minimize Data Model Size**: Use only necessary columns
2. **Optimize Relationships**: Use single-direction relationships where possible
3. **Leverage Calculated Columns**: For complex business logic
4. **Implement Row-Level Security**: For data governance

## Tables and Relationships

### Fact Tables

#### FactSales
- **Purpose**: Sales performance metrics
- **Grain**: One row per opportunity per date
- **Key Measures**:
  - Total Sales Amount
  - Average Deal Size
  - Win Rate
  - Sales Velocity

```dax
Total Sales = SUM(FactSales[SalesAmount])
Win Rate = DIVIDE(
    CALCULATE(COUNT(FactSales[OpportunityId]), FactSales[IsWon] = TRUE),
    COUNT(FactSales[OpportunityId])
)
```

#### FactMarketing
- **Purpose**: Marketing campaign performance
- **Grain**: One row per email event per date
- **Key Measures**:
  - Email Open Rate
  - Click-Through Rate
  - Conversion Rate

```dax
Open Rate = DIVIDE(
    SUM(FactMarketing[EmailsOpened]),
    SUM(FactMarketing[EmailsSent])
)
```

### Dimension Tables

#### DimDate
- **Purpose**: Time intelligence
- **Attributes**: Date, Year, Quarter, Month, FiscalYear, IsWeekend
- **Relationships**: Related to all fact tables

#### DimAccount
- **Purpose**: Customer/Account information
- **Type**: Slowly Changing Dimension (SCD Type 2)
- **Attributes**: AccountName, Industry, Revenue, EmployeeCount

## Performance Optimization

### Data Refresh Strategy
1. **Incremental Refresh**: Configure for fact tables
2. **Full Refresh**: For dimension tables (smaller size)
3. **Refresh Schedule**: Daily at 6 AM UTC

### Query Performance
1. **Aggregations**: Pre-calculate common metrics
2. **Composite Models**: For large datasets
3. **DirectQuery**: For real-time requirements

### DAX Optimization
```dax
-- Optimized measure using CALCULATE
Sales This Year = 
CALCULATE(
    [Total Sales],
    DATESYTD(DimDate[Date])
)

-- Use variables for complex calculations
Sales Growth = 
VAR CurrentPeriodSales = [Total Sales]
VAR PreviousPeriodSales = 
    CALCULATE(
        [Total Sales],
        DATEADD(DimDate[Date], -1, YEAR)
    )
RETURN
    DIVIDE(
        CurrentPeriodSales - PreviousPeriodSales,
        PreviousPeriodSales
    )
```

## Security Implementation

### Row-Level Security (RLS)
```dax
-- Sales team can only see their accounts
[AccountOwner] = USERNAME()

-- Regional managers see their region
[Region] = LOOKUPVALUE(
    Users[Region],
    Users[Email],
    USERNAME()
)
```

### Column-Level Security
- Sensitive financial data restricted to finance team
- Personal information masked for non-HR users

## Data Quality Measures

### Data Validation
```dax
-- Flag incomplete records
Data Quality Flag = 
IF(
    OR(
        ISBLANK(DimAccount[AccountName]),
        ISBLANK(FactSales[SalesAmount])
    ),
    "Incomplete",
    "Complete"
)
```

### Freshness Indicators
```dax
Data Freshness = 
VAR LastRefresh = MAX(FactSales[LoadDate])
VAR HoursOld = DATEDIFF(LastRefresh, NOW(), HOUR)
RETURN
    SWITCH(
        TRUE(),
        HoursOld <= 2, "Fresh",
        HoursOld <= 24, "Recent",
        "Stale"
    )
```

## Report Design Guidelines

### Visual Best Practices
1. **Consistent Color Scheme**: Use corporate colors
2. **Clear Hierarchies**: Logical drill-down paths
3. **Mobile Optimization**: Responsive design
4. **Accessibility**: High contrast, screen reader friendly

### Key Performance Indicators (KPIs)
- Sales Revenue (Monthly, Quarterly, Annual)
- Pipeline Health (Opportunity stages)
- Marketing ROI (Campaign effectiveness)
- Customer Acquisition Cost
- Customer Lifetime Value

### Report Structure
1. **Executive Dashboard**: High-level KPIs
2. **Sales Performance**: Detailed sales analytics
3. **Marketing Analytics**: Campaign performance
4. **Financial Reports**: Revenue and profitability
5. **Operational Reports**: Data quality and system health

## Deployment Strategy

### Development Lifecycle
1. **Development**: Power BI Desktop
2. **Testing**: Dedicated workspace
3. **UAT**: User acceptance testing
4. **Production**: Live workspace with scheduled refresh

### Version Control
- Power BI templates (.pbit files) in source control
- Dataset definitions documented
- Change log maintained

## Monitoring and Maintenance

### Performance Monitoring
- Query performance metrics
- Refresh duration tracking
- User adoption analytics

### Regular Maintenance
- Monthly performance review
- Quarterly data model optimization
- Annual security audit

## Troubleshooting Guide

### Common Issues
1. **Slow Refresh**: Check data source performance
2. **Memory Errors**: Optimize DAX calculations
3. **Relationship Issues**: Verify cardinality settings

### Performance Tuning
1. Remove unused columns and tables
2. Optimize DAX measures
3. Configure appropriate aggregations
4. Use composite models for large datasets