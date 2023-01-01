-- Azure Data Analytics Platform - Database Schema Creation
-- This script creates the necessary schemas and tables for the analytics platform

-- Create schemas for different data sources
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'salesforce')
    EXEC('CREATE SCHEMA salesforce')
GO

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'sfmc')
    EXEC('CREATE SCHEMA sfmc')
GO

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'netsuite')
    EXEC('CREATE SCHEMA netsuite')
GO

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'analytics')
    EXEC('CREATE SCHEMA analytics')
GO

-- Salesforce Account table
CREATE TABLE salesforce.Account (
    Id NVARCHAR(18) PRIMARY KEY,
    Name NVARCHAR(255) NOT NULL,
    Type NVARCHAR(50),
    Industry NVARCHAR(100),
    AnnualRevenue DECIMAL(18,2),
    NumberOfEmployees INT,
    BillingStreet NVARCHAR(255),
    BillingCity NVARCHAR(100),
    BillingState NVARCHAR(100),
    BillingPostalCode NVARCHAR(20),
    BillingCountry NVARCHAR(100),
    Phone NVARCHAR(50),
    Website NVARCHAR(255),
    CreatedDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    OwnerId NVARCHAR(18),
    IsDeleted BIT DEFAULT 0,
    LoadDate DATETIME2 DEFAULT GETUTCDATE(),
    SourceSystem NVARCHAR(50) DEFAULT 'Salesforce'
)
GO

-- Salesforce Opportunity table
CREATE TABLE salesforce.Opportunity (
    Id NVARCHAR(18) PRIMARY KEY,
    Name NVARCHAR(255) NOT NULL,
    AccountId NVARCHAR(18),
    StageName NVARCHAR(100) NOT NULL,
    Amount DECIMAL(18,2),
    Probability INT,
    CloseDate DATE NOT NULL,
    Type NVARCHAR(100),
    LeadSource NVARCHAR(100),
    CreatedDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    OwnerId NVARCHAR(18),
    IsWon BIT DEFAULT 0,
    IsClosed BIT DEFAULT 0,
    LoadDate DATETIME2 DEFAULT GETUTCDATE(),
    SourceSystem NVARCHAR(50) DEFAULT 'Salesforce',
    FOREIGN KEY (AccountId) REFERENCES salesforce.Account(Id)
)
GO

-- Salesforce Marketing Cloud Email Events table
CREATE TABLE sfmc.EmailEvent (
    JobID INT NOT NULL,
    ListID INT,
    BatchID INT,
    SubscriberID BIGINT NOT NULL,
    SubscriberKey NVARCHAR(254),
    EmailAddress NVARCHAR(254),
    EventDate DATETIME2 NOT NULL,
    EventType NVARCHAR(50) NOT NULL,
    SendID INT,
    Subject NVARCHAR(1000),
    FromName NVARCHAR(255),
    FromEmail NVARCHAR(254),
    TriggererSendDefinitionObjectID NVARCHAR(36),
    IsUnique BIT,
    URL NVARCHAR(4000),
    LinkName NVARCHAR(255),
    LinkContent NVARCHAR(4000),
    LoadDate DATETIME2 DEFAULT GETUTCDATE(),
    SourceSystem NVARCHAR(50) DEFAULT 'SFMC',
    PRIMARY KEY (JobID, SubscriberID, EventDate, EventType)
)
GO

-- NetSuite Transaction table
CREATE TABLE netsuite.Transaction (
    InternalId INT PRIMARY KEY,
    TransactionNumber NVARCHAR(50) NOT NULL,
    Type NVARCHAR(100) NOT NULL,
    Status NVARCHAR(100),
    Entity NVARCHAR(255),
    EntityId INT,
    TranDate DATE NOT NULL,
    DueDate DATE,
    Amount DECIMAL(18,2),
    Currency NVARCHAR(10),
    ExchangeRate DECIMAL(10,4),
    Subsidiary NVARCHAR(255),
    Department NVARCHAR(255),
    Location NVARCHAR(255),
    CreatedDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    CreatedBy NVARCHAR(255),
    Memo NVARCHAR(4000),
    LoadDate DATETIME2 DEFAULT GETUTCDATE(),
    SourceSystem NVARCHAR(50) DEFAULT 'NetSuite'
)
GO

-- Analytics dimension tables
CREATE TABLE analytics.DimDate (
    DateKey INT PRIMARY KEY,
    Date DATE NOT NULL,
    Year INT NOT NULL,
    Quarter INT NOT NULL,
    Month INT NOT NULL,
    MonthName NVARCHAR(20) NOT NULL,
    Day INT NOT NULL,
    DayOfWeek INT NOT NULL,
    DayName NVARCHAR(20) NOT NULL,
    IsWeekend BIT NOT NULL,
    IsHoliday BIT DEFAULT 0,
    FiscalYear INT,
    FiscalQuarter INT,
    FiscalMonth INT
)
GO

CREATE TABLE analytics.DimAccount (
    AccountKey INT IDENTITY(1,1) PRIMARY KEY,
    AccountId NVARCHAR(18) NOT NULL,
    AccountName NVARCHAR(255) NOT NULL,
    AccountType NVARCHAR(50),
    Industry NVARCHAR(100),
    AnnualRevenue DECIMAL(18,2),
    NumberOfEmployees INT,
    City NVARCHAR(100),
    State NVARCHAR(100),
    Country NVARCHAR(100),
    CreatedDate DATETIME2,
    IsActive BIT DEFAULT 1,
    EffectiveDate DATETIME2 DEFAULT GETUTCDATE(),
    ExpiryDate DATETIME2 DEFAULT '9999-12-31',
    IsCurrent BIT DEFAULT 1
)
GO

-- Analytics fact tables
CREATE TABLE analytics.FactSales (
    SalesKey INT IDENTITY(1,1) PRIMARY KEY,
    DateKey INT NOT NULL,
    AccountKey INT NOT NULL,
    OpportunityId NVARCHAR(18),
    SalesAmount DECIMAL(18,2),
    Probability INT,
    Stage NVARCHAR(100),
    IsWon BIT,
    IsClosed BIT,
    DaysToClose INT,
    LoadDate DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (DateKey) REFERENCES analytics.DimDate(DateKey),
    FOREIGN KEY (AccountKey) REFERENCES analytics.DimAccount(AccountKey)
)
GO

CREATE TABLE analytics.FactMarketing (
    MarketingKey INT IDENTITY(1,1) PRIMARY KEY,
    DateKey INT NOT NULL,
    JobID INT,
    SubscriberKey NVARCHAR(254),
    EmailAddress NVARCHAR(254),
    EventType NVARCHAR(50),
    EmailsSent INT DEFAULT 0,
    EmailsOpened INT DEFAULT 0,
    EmailsClicked INT DEFAULT 0,
    EmailsBounced INT DEFAULT 0,
    Unsubscribes INT DEFAULT 0,
    LoadDate DATETIME2 DEFAULT GETUTCDATE(),
    FOREIGN KEY (DateKey) REFERENCES analytics.DimDate(DateKey)
)
GO

-- Create indexes for performance
CREATE NONCLUSTERED INDEX IX_Account_Name ON salesforce.Account(Name)
CREATE NONCLUSTERED INDEX IX_Account_Industry ON salesforce.Account(Industry)
CREATE NONCLUSTERED INDEX IX_Account_CreatedDate ON salesforce.Account(CreatedDate)

CREATE NONCLUSTERED INDEX IX_Opportunity_AccountId ON salesforce.Opportunity(AccountId)
CREATE NONCLUSTERED INDEX IX_Opportunity_CloseDate ON salesforce.Opportunity(CloseDate)
CREATE NONCLUSTERED INDEX IX_Opportunity_Stage ON salesforce.Opportunity(StageName)

CREATE NONCLUSTERED INDEX IX_EmailEvent_EventDate ON sfmc.EmailEvent(EventDate)
CREATE NONCLUSTERED INDEX IX_EmailEvent_EventType ON sfmc.EmailEvent(EventType)
CREATE NONCLUSTERED INDEX IX_EmailEvent_SubscriberKey ON sfmc.EmailEvent(SubscriberKey)

CREATE NONCLUSTERED INDEX IX_Transaction_TranDate ON netsuite.Transaction(TranDate)
CREATE NONCLUSTERED INDEX IX_Transaction_Type ON netsuite.Transaction(Type)
CREATE NONCLUSTERED INDEX IX_Transaction_Entity ON netsuite.Transaction(Entity)

CREATE NONCLUSTERED INDEX IX_FactSales_DateKey ON analytics.FactSales(DateKey)
CREATE NONCLUSTERED INDEX IX_FactSales_AccountKey ON analytics.FactSales(AccountKey)

CREATE NONCLUSTERED INDEX IX_FactMarketing_DateKey ON analytics.FactMarketing(DateKey)
CREATE NONCLUSTERED INDEX IX_FactMarketing_EventType ON analytics.FactMarketing(EventType)

PRINT 'Database schema creation completed successfully!'