"""Beginner-friendly housing data cleaning and optional MySQL loading."""

from pathlib import Path
from getpass import getpass

import pandas as pd


def clean_data(data):
    """Clean a DataFrame and add columns needed for analysis."""
    data = data.copy()
    data.columns = data.columns.str.strip()

    # The actual dataset uses Developer_Name instead of Builder.
    if "Builder" not in data.columns:
        data = data.rename(columns={"Developer_Name": "Builder"})

    required_columns = [
        "Micro_Market", "Builder", "Unit_Size_Sqft",
        "Ticket_Price_Cr", "Amenity_Score", "Purchase_Quarter",
    ]
    for column in required_columns:
        if column not in data.columns:
            raise ValueError(f"Required column is missing: {column}")

    # Remove repeated rows. Do not remove different properties in one project.
    original_count = len(data)
    data = data.drop_duplicates().copy()
    print("Duplicate rows removed:", original_count - len(data))

    # Trim spaces in text columns and treat empty strings as missing values.
    text_columns = data.select_dtypes(include=["object", "string"]).columns
    for column in text_columns:
        data[column] = data[column].astype("string").str.strip()
        data[column] = data[column].replace("", pd.NA)

    # Normalize locality names. Preserve builder names such as RMZ and SNN Raj.
    data["Micro_Market"] = data["Micro_Market"].str.title()
    data["Micro_Market"] = data["Micro_Market"].replace({
        "Jp Nagar": "JP Nagar", "Mg Road": "MG Road",
    })
    data["Builder"] = data["Builder"].str.upper()

    if "Configuration" in data.columns:
        data["Configuration"] = data["Configuration"].str.upper()
        data["Configuration"] = data["Configuration"].str.replace(
            " ", "", regex=False
        )

    # Example: "Rs. 9.82 Cr" or "₹9.82 Cr" becomes the number 9.82.
    prices = data["Ticket_Price_Cr"].astype("string").str.lower()
    for word in ["₹", "rs.", "rs", "inr", "crores", "crore", "cr", ",", " "]:
        prices = prices.str.replace(word, "", regex=False)
    data["Ticket_Price_Cr"] = pd.to_numeric(prices, errors="coerce")

    numeric_columns = [
        "Unit_Size_Sqft", "Amenity_Score", "Connectivity_Score",
        "Locality_Infra_Score", "Avg_Traffic_Time_Min",
    ]
    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors="coerce")

    # Non-positive prices or areas are invalid. Keep missing values as missing.
    data.loc[data["Ticket_Price_Cr"] <= 0, "Ticket_Price_Cr"] = float("nan")
    data.loc[data["Unit_Size_Sqft"] <= 0, "Unit_Size_Sqft"] = float("nan")

    # Remember which amenity values were missing before filling them.
    data["Amenity_Score_Was_Missing"] = data["Amenity_Score"].isna().astype(int)
    median_score = data["Amenity_Score"].median()
    data["Amenity_Score"] = data["Amenity_Score"].fillna(median_score)

    category_columns = [
        "Micro_Market", "Builder", "Configuration", "Transaction_Type",
        "Buyer_Type", "Possession_Status", "Sales_Channel", "NRI_Buyer",
    ]
    for column in category_columns:
        if column in data.columns:
            data[column] = data[column].fillna("Unknown")

    if "Buyer_Comments" in data.columns:
        data["Buyer_Comments"] = data["Buyer_Comments"].fillna("No comment")

    # One crore equals 10,000,000 rupees. Missing price/area gives missing output.
    data["Price_per_Sqft"] = (
        data["Ticket_Price_Cr"] * 10000000 / data["Unit_Size_Sqft"]
    ).round(2)

    # The supplied dates are calendar quarter end dates, e.g. 2024-06-30.
    dates = pd.to_datetime(data["Purchase_Quarter"], errors="coerce")
    data["Purchase_Quarter"] = dates
    data["Purchase_Year"] = dates.dt.year.astype("Int64")
    data["Quarter_Number"] = dates.dt.quarter.astype("Int64")
    data["Quarter"] = dates.dt.to_period("Q").astype("string")
    data.loc[dates.isna(), "Quarter"] = pd.NA

    # India's financial year starts in April. April-June is fiscal Q1.
    fiscal_start = dates.dt.year.where(dates.dt.month >= 4, dates.dt.year - 1)
    fiscal_start = fiscal_start.astype("Int64")
    fiscal_quarter = ((dates.dt.month - 4) % 12 // 3 + 1).astype("Int64")
    fiscal_end = ((fiscal_start + 1) % 100).astype("string").str.zfill(2)
    data["Fiscal_Year"] = "FY" + fiscal_start.astype("string") + "-" + fiscal_end
    data["Fiscal_Quarter_Number"] = fiscal_quarter
    data["Fiscal_Quarter"] = (
        data["Fiscal_Year"] + " Q" + fiscal_quarter.astype("string")
    )
    data["Fiscal_Quarter_Sort"] = fiscal_start * 10 + fiscal_quarter

    # Flag unusually high/low prices for review, without deleting those rows.
    first_quartile = data["Ticket_Price_Cr"].quantile(0.25)
    third_quartile = data["Ticket_Price_Cr"].quantile(0.75)
    spread = third_quartile - first_quartile
    lower_limit = first_quartile - 1.5 * spread
    upper_limit = third_quartile + 1.5 * spread
    data["Ticket_Price_Outlier"] = (
        (data["Ticket_Price_Cr"] < lower_limit)
        | (data["Ticket_Price_Cr"] > upper_limit)
    ).fillna(False).astype(int)

    # A simple keyword rule gives an explainable comment label, not an ML model.
    if "Buyer_Comments" in data.columns:
        data["Comment_Sentiment"] = data["Buyer_Comments"].apply(label_comment)
    data["Market_Location"] = data["Micro_Market"] + ", Bengaluru, Karnataka, India"

    # The linked dataset has no booking status. Never invent booking outcomes.
    if "Booking_Status" not in data.columns:
        print("Booking_Status is absent. Booking analysis is unavailable.")
        data["Booking_Status"] = "Unknown"
    else:
        data["Booking_Status"] = data["Booking_Status"].astype("string")
        data["Booking_Status"] = data["Booking_Status"].str.strip().str.title()
        data["Booking_Status"] = data["Booking_Status"].fillna("Unknown")

    # Only these two explicit labels are classified; all other labels stay null.
    data["Booking_Flag"] = data["Booking_Status"].map({
        "Booked": 1, "Not Booked": 0,
    }).astype("Int64")

    print("Cleaned rows:", len(data))
    print("Rows with missing ticket price:", data["Ticket_Price_Cr"].isna().sum())
    print("Rows with missing unit size:", data["Unit_Size_Sqft"].isna().sum())
    return data


def label_comment(comment):
    """Label comments using a small, visible list of positive/negative words."""
    comment = str(comment).lower()
    if comment == "no comment":
        return "No comment"
    positive = any(word in comment for word in [
        "loved", "excellent", "great", "underpriced",
    ])
    negative = any(word in comment for word in [
        "not responsive", "too far", "poor",
    ])
    if positive and negative:
        return "Mixed"
    if positive:
        return "Positive"
    if negative:
        return "Negative"
    return "Neutral"


def load_to_mysql(data):
    """Ask for connection details and create a new MySQL table."""
    from sqlalchemy.engine import URL

    host = input("MySQL host [localhost]: ").strip() or "localhost"
    port = int(input("MySQL port [3306]: ").strip() or "3306")
    database = input("Existing MySQL database name: ").strip()
    username = input("MySQL username: ").strip()
    password = getpass("MySQL password (hidden): ")

    # URL.create safely handles passwords containing characters such as @.
    connection_url = URL.create(
        "mysql+pymysql", username=username, password=password,
        host=host, port=port, database=database,
        query={"charset": "utf8mb4"},
    )
    write_to_mysql(data, connection_url)


def write_to_mysql(data, connection_url):
    """Create a new table and load it; also used for automated verification."""
    from sqlalchemy import create_engine, text, types

    if "Property_ID" in data.columns:
        if data["Property_ID"].isna().any() or data["Property_ID"].duplicated().any():
            raise ValueError("Property_ID must be present and unique for each row.")
    engine = create_engine(connection_url)

    # Choose SQL types that also work when a whole column contains nulls.
    column_types = {}
    for column in data.columns:
        if pd.api.types.is_integer_dtype(data[column]):
            column_types[column] = types.Integer()
        elif pd.api.types.is_numeric_dtype(data[column]):
            column_types[column] = types.Double()
        elif pd.api.types.is_datetime64_any_dtype(data[column]):
            column_types[column] = types.Date()
        else:
            column_types[column] = types.VARCHAR(255)
    if "Buyer_Comments" in data.columns:
        column_types["Buyer_Comments"] = types.Text()

    # 'fail' protects an existing table from replacement or duplicate loading.
    try:
        with engine.begin() as connection:
            data.to_sql(
                "housing_sales", connection, if_exists="fail", index=False,
                dtype=column_types, chunksize=1000,
            )
            if "Property_ID" in data.columns:
                connection.execute(text(
                    "ALTER TABLE housing_sales ADD PRIMARY KEY (Property_ID)"
                ))
            connection.execute(text(
                "CREATE INDEX idx_builder ON housing_sales (Builder)"
            ))
            connection.execute(text(
                "CREATE INDEX idx_market ON housing_sales (Micro_Market)"
            ))
            connection.execute(text(
                "CREATE INDEX idx_fiscal_quarter ON housing_sales (Fiscal_Quarter)"
            ))
        print("Data loaded into the housing_sales table.")
    finally:
        engine.dispose()


def main():
    # Input paths let you run the script on another computer without editing it.
    csv_path = Path(input("Raw CSV file path: ").strip().strip('"'))
    output_folder = Path(input("Folder for the cleaned CSV: ").strip().strip('"'))
    output_folder.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(csv_path)
    cleaned_data = clean_data(data)
    output_path = output_folder / "luxury_housing_cleaned.csv"
    if output_path.resolve() == csv_path.resolve():
        raise ValueError("Choose another output folder to preserve the raw CSV.")
    cleaned_data.to_csv(output_path, index=False)
    print("Cleaned CSV saved to:", output_path.resolve())

    answer = input("Load the cleaned data into MySQL? (yes/no): ").strip().lower()
    if answer == "yes":
        load_to_mysql(cleaned_data)


if __name__ == "__main__":
    main()
