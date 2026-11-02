-- Run these queries after the Python script loads housing_sales into MySQL.
-- First select your database in MySQL Workbench.

-- 1. Validate the number of records (100000 for the supplied dataset).
SELECT COUNT(*) AS total_records FROM housing_sales;

-- 2. Show how much data is missing.
SELECT
    COUNT(*) - COUNT(Ticket_Price_Cr) AS missing_prices,
    COUNT(*) - COUNT(Unit_Size_Sqft) AS missing_unit_sizes,
    SUM(Amenity_Score_Was_Missing) AS filled_amenity_scores,
    COUNT(Booking_Flag) AS records_with_known_booking_outcomes
FROM housing_sales;

-- 3. Average ticket price and recorded ticket value by builder.
-- SUM ignores missing prices. Recorded ticket value is not confirmed revenue.
SELECT Builder, COUNT(*) AS record_count,
    COUNT(Ticket_Price_Cr) AS priced_records,
    ROUND(SUM(Ticket_Price_Cr), 2) AS recorded_ticket_value_cr,
    ROUND(AVG(Ticket_Price_Cr), 2) AS average_ticket_price_cr
FROM housing_sales
GROUP BY Builder
ORDER BY recorded_ticket_value_cr DESC;

-- 4. Calendar quarter trends by micro-market; these counts are not bookings.
SELECT Quarter, Micro_Market, COUNT(*) AS record_count
FROM housing_sales
WHERE Quarter IS NOT NULL
GROUP BY Quarter, Micro_Market
ORDER BY Quarter, Micro_Market;

-- 5. Configuration distribution.
SELECT Configuration, COUNT(*) AS record_count
FROM housing_sales
GROUP BY Configuration
ORDER BY record_count DESC;

-- 6. Sales channel distribution.
SELECT Sales_Channel, COUNT(*) AS record_count,
    ROUND(AVG(Ticket_Price_Cr), 2) AS average_ticket_price_cr
FROM housing_sales
GROUP BY Sales_Channel
ORDER BY record_count DESC;

-- 7. Builder contribution by calendar quarter.
SELECT Builder, Quarter,
    ROUND(SUM(Ticket_Price_Cr), 2) AS recorded_ticket_value_cr
FROM housing_sales
WHERE Quarter IS NOT NULL
GROUP BY Builder, Quarter
ORDER BY Quarter, recorded_ticket_value_cr DESC;

-- 8. Possession status and buyer type.
SELECT Possession_Status, Buyer_Type, COUNT(*) AS record_count
FROM housing_sales
GROUP BY Possession_Status, Buyer_Type
ORDER BY record_count DESC;

-- 9. Locality concentration. Project_Name is used because Project_ID is absent.
SELECT Micro_Market, COUNT(*) AS property_records,
    COUNT(DISTINCT Project_Name) AS project_name_count
FROM housing_sales
GROUP BY Micro_Market
ORDER BY property_records DESC;

-- 10. Top five builders by recorded ticket value.
SELECT Builder, ROUND(SUM(Ticket_Price_Cr), 2) AS recorded_ticket_value_cr
FROM housing_sales
GROUP BY Builder
ORDER BY recorded_ticket_value_cr DESC
LIMIT 5;

-- 11. Booking labels. The supplied file will show only Unknown.
SELECT Booking_Status, COUNT(*) AS record_count
FROM housing_sales
GROUP BY Booking_Status;

-- 12. Conversion uses only recognized Booked / Not Booked outcomes.
-- Returns NULL for every market in the supplied dataset, not a false 0%.
SELECT Micro_Market, COUNT(Booking_Flag) AS known_outcomes,
    SUM(Booking_Flag) AS bookings,
    ROUND(100.0 * SUM(Booking_Flag) / NULLIF(COUNT(Booking_Flag), 0), 2)
        AS booking_conversion_percent
FROM housing_sales
GROUP BY Micro_Market;

-- 13. Amenity and booking analysis, only if real booking labels become available.
-- Exclude filled amenity values to avoid treating estimates as observations.
SELECT FLOOR(Amenity_Score) AS amenity_score_group,
    COUNT(*) AS records_with_observed_scores,
    ROUND(100.0 * AVG(Booking_Flag), 2) AS booking_conversion_percent
FROM housing_sales
WHERE Amenity_Score_Was_Missing = 0 AND Booking_Flag IS NOT NULL
GROUP BY FLOOR(Amenity_Score)
ORDER BY amenity_score_group;

-- 14. Indian fiscal quarter activity. Fiscal Q1 is April-June.
SELECT Fiscal_Quarter, Fiscal_Quarter_Sort, COUNT(*) AS record_count,
    ROUND(SUM(Ticket_Price_Cr), 2) AS recorded_ticket_value_cr
FROM housing_sales
GROUP BY Fiscal_Quarter, Fiscal_Quarter_Sort
ORDER BY Fiscal_Quarter_Sort;

-- 15. Simple keyword comment labels, not a trained sentiment model.
SELECT Comment_Sentiment, COUNT(*) AS record_count
FROM housing_sales
GROUP BY Comment_Sentiment
ORDER BY record_count DESC;

-- 16. Outlier and missing-price coverage by builder.
SELECT Builder, COUNT(*) AS record_count,
    COUNT(Ticket_Price_Cr) AS priced_records,
    SUM(Ticket_Price_Outlier) AS price_outlier_records
FROM housing_sales
GROUP BY Builder
ORDER BY price_outlier_records DESC;

-- 17. Validate the three dimension relationships.
SELECT COUNT(*) AS orphan_records
FROM housing_sales h
LEFT JOIN dim_builder b ON h.Builder = b.Builder
LEFT JOIN dim_market m ON h.Micro_Market = m.Micro_Market
LEFT JOIN dim_quarter q ON h.Purchase_Quarter = q.Purchase_Quarter
WHERE b.Builder IS NULL OR m.Micro_Market IS NULL OR q.Purchase_Quarter IS NULL;
