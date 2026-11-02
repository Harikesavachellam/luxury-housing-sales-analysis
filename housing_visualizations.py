"""Create four simple charts from the cleaned housing CSV."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def create_charts(data, output_folder):
    """Group the data, draw four charts, and save one dashboard image."""

    # Count how many property records belong to each calendar quarter.
    quarterly_records = data.groupby("Quarter").size().sort_index()

    # Add the available ticket prices for each builder and keep the top five.
    builder_values = data.groupby("Builder")["Ticket_Price_Cr"].sum(min_count=1)
    top_builders = builder_values.dropna().nlargest(5).sort_values()

    # Count the different housing configurations and micro-markets.
    configurations = data["Configuration"].value_counts()
    top_markets = data["Micro_Market"].value_counts().head(8).sort_values()

    # Create four chart areas: two rows and two columns.
    figure, axes = plt.subplots(2, 2, figsize=(16, 10))
    figure.suptitle(
        f"Bengaluru Luxury Housing | {len(data):,} Cleaned Records",
        fontsize=20,
    )

    # Chart 1: a line chart shows changes over time.
    axes[0, 0].plot(
        quarterly_records.index, quarterly_records.values,
        marker="o", color="#2563eb", linewidth=2,
    )
    axes[0, 0].set_title("Property records by calendar quarter")
    axes[0, 0].set_xlabel("Calendar quarter")
    axes[0, 0].set_ylabel("Number of records")
    axes[0, 0].set_ylim(0, quarterly_records.max() * 1.25)
    axes[0, 0].tick_params(axis="x", labelrotation=30)
    axes[0, 0].grid(axis="y", alpha=0.2)

    # Chart 2: horizontal bars make long builder names easy to read.
    bars = axes[0, 1].barh(top_builders.index, top_builders.values, color="#0f766e")
    axes[0, 1].bar_label(bars, fmt="%.0f", padding=4)
    axes[0, 1].set_title("Top 5 builders by recorded ticket value")
    axes[0, 1].set_xlabel("Recorded ticket value (INR crore)")
    axes[0, 1].set_xlim(0, top_builders.max() * 1.18)

    # Chart 3: compare the number of records for each configuration.
    bars = axes[1, 0].bar(
        configurations.index, configurations.values, color="#7c3aed"
    )
    axes[1, 0].bar_label(bars, padding=4)
    axes[1, 0].set_title("Housing configuration distribution")
    axes[1, 0].set_xlabel("Configuration")
    axes[1, 0].set_ylabel("Number of records")
    axes[1, 0].set_ylim(0, configurations.max() * 1.18)

    # Chart 4: show the eight micro-markets with the most property records.
    bars = axes[1, 1].barh(top_markets.index, top_markets.values, color="#d97706")
    axes[1, 1].bar_label(bars, padding=4)
    axes[1, 1].set_title("Top 8 micro-markets by property records")
    axes[1, 1].set_xlabel("Number of records")
    axes[1, 1].set_xlim(0, top_markets.max() * 1.18)

    figure.text(
        0.5, 0.02,
        "Record counts are not booking counts. Ticket totals exclude missing "
        "prices and are not confirmed revenue.",
        ha="center", fontsize=10,
    )
    figure.tight_layout(rect=[0, 0.05, 1, 0.94])
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    output_path = output_folder / "housing_dashboard.png"
    figure.savefig(output_path, dpi=150)
    print("Dashboard saved to:", output_path.resolve())
    return figure


def main():
    csv_path = input("Cleaned CSV file path: ").strip().strip('"')
    output_folder = input("Folder for the chart image: ").strip().strip('"')
    data = pd.read_csv(csv_path)
    create_charts(data, output_folder)
    plt.show()


if __name__ == "__main__":
    main()
