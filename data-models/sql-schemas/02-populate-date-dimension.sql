-- Populate Date Dimension Table
-- This script populates the DimDate table with dates from 2020 to 2030

DECLARE @StartDate DATE = '2020-01-01'
DECLARE @EndDate DATE = '2030-12-31'
DECLARE @CurrentDate DATE = @StartDate

WHILE @CurrentDate <= @EndDate
BEGIN
    DECLARE @DateKey INT = CAST(FORMAT(@CurrentDate, 'yyyyMMdd') AS INT)
    DECLARE @Year INT = YEAR(@CurrentDate)
    DECLARE @Quarter INT = DATEPART(QUARTER, @CurrentDate)
    DECLARE @Month INT = MONTH(@CurrentDate)
    DECLARE @MonthName NVARCHAR(20) = DATENAME(MONTH, @CurrentDate)
    DECLARE @Day INT = DAY(@CurrentDate)
    DECLARE @DayOfWeek INT = DATEPART(WEEKDAY, @CurrentDate)
    DECLARE @DayName NVARCHAR(20) = DATENAME(WEEKDAY, @CurrentDate)
    DECLARE @IsWeekend BIT = CASE WHEN @DayOfWeek IN (1, 7) THEN 1 ELSE 0 END
    
    -- Calculate fiscal year (assuming fiscal year starts in April)
    DECLARE @FiscalYear INT = CASE 
        WHEN @Month >= 4 THEN @Year 
        ELSE @Year - 1 
    END
    
    DECLARE @FiscalQuarter INT = CASE 
        WHEN @Month IN (4, 5, 6) THEN 1
        WHEN @Month IN (7, 8, 9) THEN 2
        WHEN @Month IN (10, 11, 12) THEN 3
        ELSE 4
    END
    
    DECLARE @FiscalMonth INT = CASE 
        WHEN @Month >= 4 THEN @Month - 3
        ELSE @Month + 9
    END

    INSERT INTO analytics.DimDate (
        DateKey, Date, Year, Quarter, Month, MonthName, Day, DayOfWeek, DayName, 
        IsWeekend, IsHoliday, FiscalYear, FiscalQuarter, FiscalMonth
    )
    VALUES (
        @DateKey, @CurrentDate, @Year, @Quarter, @Month, @MonthName, @Day, 
        @DayOfWeek, @DayName, @IsWeekend, 0, @FiscalYear, @FiscalQuarter, @FiscalMonth
    )

    SET @CurrentDate = DATEADD(DAY, 1, @CurrentDate)
END

-- Mark common holidays (US holidays as example)
UPDATE analytics.DimDate SET IsHoliday = 1 
WHERE (Month = 1 AND Day = 1) -- New Year's Day
   OR (Month = 7 AND Day = 4) -- Independence Day
   OR (Month = 12 AND Day = 25) -- Christmas Day
   OR (Month = 11 AND DayOfWeek = 5 AND Day BETWEEN 22 AND 28) -- Thanksgiving (4th Thursday in November)

PRINT 'Date dimension populated successfully!'
PRINT 'Total records: ' + CAST((SELECT COUNT(*) FROM analytics.DimDate) AS NVARCHAR(10))