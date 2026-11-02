-- Run after the Python loader has created and filled housing_sales.
-- Run once per fresh database.
CREATE TABLE dim_builder AS
SELECT DISTINCT Builder FROM housing_sales;
ALTER TABLE dim_builder ADD PRIMARY KEY (Builder);

CREATE TABLE dim_market AS
SELECT DISTINCT Micro_Market, Market_Location FROM housing_sales;
ALTER TABLE dim_market ADD PRIMARY KEY (Micro_Market);

CREATE TABLE dim_quarter AS
SELECT DISTINCT Purchase_Quarter, Purchase_Year, Quarter_Number, Quarter,
    Fiscal_Year, Fiscal_Quarter_Number, Fiscal_Quarter, Fiscal_Quarter_Sort
FROM housing_sales WHERE Purchase_Quarter IS NOT NULL;
ALTER TABLE dim_quarter ADD PRIMARY KEY (Purchase_Quarter);
