-- Run only in a new empty database.
CREATE DATABASE IF NOT EXISTS luxury_housing CHARACTER SET utf8mb4;
USE luxury_housing;

CREATE TABLE `housing_sales` (
  `Property_ID` varchar(255) NOT NULL,
  `Micro_Market` varchar(255) DEFAULT NULL,
  `Project_Name` varchar(255) DEFAULT NULL,
  `Builder` varchar(255) DEFAULT NULL,
  `Unit_Size_Sqft` double DEFAULT NULL,
  `Configuration` varchar(255) DEFAULT NULL,
  `Ticket_Price_Cr` double DEFAULT NULL,
  `Transaction_Type` varchar(255) DEFAULT NULL,
  `Buyer_Type` varchar(255) DEFAULT NULL,
  `Purchase_Quarter` date DEFAULT NULL,
  `Connectivity_Score` double DEFAULT NULL,
  `Amenity_Score` double DEFAULT NULL,
  `Possession_Status` varchar(255) DEFAULT NULL,
  `Sales_Channel` varchar(255) DEFAULT NULL,
  `NRI_Buyer` varchar(255) DEFAULT NULL,
  `Locality_Infra_Score` double DEFAULT NULL,
  `Avg_Traffic_Time_Min` int DEFAULT NULL,
  `Buyer_Comments` text,
  `Amenity_Score_Was_Missing` int DEFAULT NULL,
  `Price_per_Sqft` double DEFAULT NULL,
  `Purchase_Year` int DEFAULT NULL,
  `Quarter_Number` int DEFAULT NULL,
  `Quarter` varchar(255) DEFAULT NULL,
  `Fiscal_Year` varchar(255) DEFAULT NULL,
  `Fiscal_Quarter_Number` int DEFAULT NULL,
  `Fiscal_Quarter` varchar(255) DEFAULT NULL,
  `Fiscal_Quarter_Sort` int DEFAULT NULL,
  `Ticket_Price_Outlier` int DEFAULT NULL,
  `Comment_Sentiment` varchar(255) DEFAULT NULL,
  `Market_Location` varchar(255) DEFAULT NULL,
  `Booking_Status` varchar(255) DEFAULT NULL,
  `Booking_Flag` int DEFAULT NULL,
  PRIMARY KEY (`Property_ID`),
  KEY `idx_builder` (`Builder`),
  KEY `idx_market` (`Micro_Market`),
  KEY `idx_fiscal_quarter` (`Fiscal_Quarter`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `dim_quarter` (
  `Purchase_Quarter` date NOT NULL,
  `Purchase_Year` int DEFAULT NULL,
  `Quarter_Number` int DEFAULT NULL,
  `Quarter` varchar(255) DEFAULT NULL,
  `Fiscal_Year` varchar(255) DEFAULT NULL,
  `Fiscal_Quarter_Number` int DEFAULT NULL,
  `Fiscal_Quarter` varchar(255) DEFAULT NULL,
  `Fiscal_Quarter_Sort` int DEFAULT NULL,
  PRIMARY KEY (`Purchase_Quarter`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `dim_market` (
  `Micro_Market` varchar(255) NOT NULL,
  `Market_Location` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Micro_Market`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `dim_builder` (
  `Builder` varchar(255) NOT NULL,
  PRIMARY KEY (`Builder`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
