"""Beginner-friendly EDA: summaries, comparisons, correlations, and charts."""

from pathlib import Path
import json

import matplotlib.pyplot as plt
import pandas as pd


def run_eda(data, output_folder):
    """Save descriptive tables and six charts for the cleaned dataset."""
    output_folder = Path(output_folder)
    table_folder = output_folder / "eda_tables"
    chart_folder = output_folder / "charts"
    table_folder.mkdir(parents=True, exist_ok=True)
    chart_folder.mkdir(parents=True, exist_ok=True)

    # Basic structure, missing values, and numerical distributions.
    data.dtypes.astype(str).to_csv(table_folder / "column_types.csv")
    data.isna().sum().to_csv(table_folder / "missing_values.csv")
    data.describe().round(4).to_csv(table_folder / "numeric_statistics.csv")

    # Compare builders, markets, fiscal quarters, and other categories.
    categories = [
        "Builder", "Micro_Market", "Fiscal_Quarter", "Configuration",
        "Sales_Channel", "Buyer_Type", "Possession_Status", "Comment_Sentiment",
    ]
    for category in categories:
        summary = data.groupby(category).agg(
            Record_Count=("Property_ID", "size"),
            Priced_Records=("Ticket_Price_Cr", "count"),
            Recorded_Ticket_Value_Cr=("Ticket_Price_Cr", "sum"),
            Average_Ticket_Price_Cr=("Ticket_Price_Cr", "mean"),
            Median_Price_Per_Sqft=("Price_per_Sqft", "median"),
        )
        summary.round(4).to_csv(table_folder / f"summary_{category}.csv")

    # Cross-tabulations show how categories occur together.
    pd.crosstab(data["Possession_Status"], data["Buyer_Type"]).to_csv(
        table_folder / "possession_by_buyer_type.csv"
    )
    pd.crosstab(data["Sales_Channel"], data["Comment_Sentiment"]).to_csv(
        table_folder / "channel_by_comment_sentiment.csv"
    )
    pd.crosstab(data["Builder"], data["Fiscal_Quarter"]).to_csv(
        table_folder / "builder_by_fiscal_quarter.csv"
    )
    data.groupby(["Builder", "Fiscal_Quarter"])["Ticket_Price_Cr"].sum().unstack().to_csv(
        table_folder / "builder_value_by_fiscal_quarter.csv"
    )

    # Review price outliers. A high price is a review flag, not proof of an error.
    outliers = data[data["Ticket_Price_Outlier"] == 1]
    outliers.to_csv(table_folder / "price_outliers_for_review.csv", index=False)
    observed = data[data["Amenity_Score_Was_Missing"] == 0]
    correlation_columns = [
        "Ticket_Price_Cr", "Unit_Size_Sqft", "Amenity_Score",
        "Connectivity_Score", "Locality_Infra_Score", "Avg_Traffic_Time_Min",
    ]
    correlations = observed[correlation_columns].corr()
    correlations.round(4).to_csv(table_folder / "observed_score_correlations.csv")

    # Chart 1: histogram of available ticket prices.
    figure, axis = plt.subplots(figsize=(9, 5))
    axis.hist(data["Ticket_Price_Cr"].dropna(), bins=45, color="#2563eb")
    axis.set_title("Ticket price distribution | positive observed prices")
    axis.set_xlabel("Ticket price (INR crore)")
    axis.set_ylabel("Number of records")
    save_chart(figure, chart_folder / "price_distribution.png")

    # Chart 2: boxplots compare observed prices across builders.
    builders = sorted(data["Builder"].unique())
    prices = [data.loc[data["Builder"] == builder, "Ticket_Price_Cr"].dropna()
              for builder in builders]
    figure, axis = plt.subplots(figsize=(12, 6))
    axis.boxplot(prices, tick_labels=builders, orientation="horizontal")
    axis.set_title("Price spread by builder | outliers retained")
    axis.set_xlabel("Ticket price (INR crore)")
    save_chart(figure, chart_folder / "builder_price_boxplot.png")

    # Chart 3: sample only complete, observed price/amenity pairs for readability.
    pairs = observed.dropna(subset=["Ticket_Price_Cr", "Amenity_Score"])
    sample = pairs.sample(n=min(2000, len(pairs)), random_state=42)
    figure, axis = plt.subplots(figsize=(9, 5))
    axis.scatter(sample["Amenity_Score"], sample["Ticket_Price_Cr"], alpha=0.25, s=12)
    axis.set_title("Amenity score and price | sample of observed pairs")
    axis.set_xlabel("Amenity score (0-10)")
    axis.set_ylabel("Ticket price (INR crore)")
    save_chart(figure, chart_folder / "amenity_vs_price.png")

    # Chart 4: fiscal quarter record counts, ordered by the numerical sort column.
    quarter_counts = data.groupby(["Fiscal_Quarter_Sort", "Fiscal_Quarter"]).size()
    quarter_counts = quarter_counts.sort_index()
    figure, axis = plt.subplots(figsize=(11, 5))
    axis.plot(quarter_counts.index.get_level_values("Fiscal_Quarter"),
              quarter_counts.values, marker="o", color="#0f766e")
    axis.set_ylim(0, quarter_counts.max() * 1.2)
    axis.tick_params(axis="x", labelrotation=25)
    axis.set_title("Property record activity by Indian fiscal quarter")
    axis.set_xlabel("Fiscal quarter (financial year starts in April)")
    axis.set_ylabel("Number of records")
    save_chart(figure, chart_folder / "fiscal_quarter_activity.png")

    # Chart 5: buyer comments classified using the documented keyword rules.
    sentiment_counts = data["Comment_Sentiment"].value_counts()
    figure, axis = plt.subplots(figsize=(9, 5))
    bars = axis.bar(sentiment_counts.index, sentiment_counts.values, color="#7c3aed")
    axis.bar_label(bars, padding=3)
    axis.set_ylim(0, sentiment_counts.max() * 1.15)
    axis.set_title("Buyer comment labels | simple keyword rules")
    axis.set_ylabel("Number of records")
    save_chart(figure, chart_folder / "buyer_comment_labels.png")

    # Chart 6: correlation is a relationship measure, not evidence of causation.
    figure, axis = plt.subplots(figsize=(10, 7))
    image = axis.imshow(correlations, vmin=-1, vmax=1, cmap="coolwarm")
    axis.set_xticks(range(len(correlation_columns)), correlation_columns, rotation=35, ha="right")
    axis.set_yticks(range(len(correlation_columns)), correlation_columns)
    for row in range(len(correlation_columns)):
        for column in range(len(correlation_columns)):
            axis.text(column, row, f"{correlations.iloc[row, column]:.2f}", ha="center", va="center")
    figure.colorbar(image, ax=axis, label="Pearson correlation")
    axis.set_title("Numerical relationships | records with observed amenity scores")
    save_chart(figure, chart_folder / "correlation_heatmap.png")

    result = {
        "records": len(data), "builders": int(data.Builder.nunique()),
        "markets": int(data.Micro_Market.nunique()),
        "missing_prices": int(data.Ticket_Price_Cr.isna().sum()),
        "missing_sizes": int(data.Unit_Size_Sqft.isna().sum()),
        "price_per_sqft_available": int(data.Price_per_Sqft.notna().sum()),
        "filled_amenity_scores": int(data.Amenity_Score_Was_Missing.sum()),
        "price_outlier_records": len(outliers),
        "observed_amenity_price_pairs": len(pairs),
        "amenity_price_correlation": float(pairs.Amenity_Score.corr(pairs.Ticket_Price_Cr)),
        "average_ticket_price_cr": float(data.Ticket_Price_Cr.mean()),
        "median_ticket_price_cr": float(data.Ticket_Price_Cr.median()),
        "recorded_ticket_value_cr": float(data.Ticket_Price_Cr.sum()),
        "booking_status_available": bool(data.Booking_Flag.notna().any()),
    }
    (table_folder / "eda_summary.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    return result


def save_chart(figure, path):
    """Save a chart and close it so repeated runs use less memory."""
    figure.tight_layout()
    figure.savefig(path, dpi=150)
    plt.close(figure)


if __name__ == "__main__":
    csv_path = input("Cleaned CSV path: ").strip().strip('"')
    output_folder = input("Folder for EDA results: ").strip().strip('"')
    run_eda(pd.read_csv(csv_path), output_folder)
