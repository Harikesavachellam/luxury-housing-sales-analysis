# Luxury Housing Sales Analysis - Bengaluru

A beginner-friendly Python, MySQL, EDA, and Power BI project using the CSV linked
in the course brief. The Python uses small functions, direct pandas operations,
and comments explaining each step.

## Current verification status

The Python pipeline ran on the supplied dataset. MySQL 8.4.3 loaded all 100,000
cleaned records; SQL results matched Python. The complete database export was
restored and verified. EDA tables, charts, and written findings are included.

The editable Power BI project has four pages, 48 visual containers, 22 DAX
measures, four tables, and three relationships. Report definitions pass Microsoft
JSON-schema checks; the semantic model deserializes through Microsoft's Tabular
Object Model. **Power BI Desktop is not installed on the preparation computer.
Native report rendering, DAX execution, and refresh have not been verified.**
No `.pbix` file is included. Open and verify the `.pbip` project, then save a
`.pbix` before final submission if your evaluator requires that format.

The source has no booking outcomes. Those measures correctly remain unavailable.
Instructor acceptance of the dataset limitation and the MySQL Import connection
is still required. GitHub publication and course submission have not been done.

## Files to start with

| File or folder | Purpose |
|---|---|
| `luxury_housing_analysis.py` | Cleaning, feature creation, and MySQL loading |
| `housing_eda.py` | Descriptive statistics, comparisons, correlations, and six EDA charts |
| `housing_visualizations.py` | Simple four-chart dashboard |
| `luxury_housing_notebook.ipynb` | Explainable notebook version of the workflow |
| `data/luxury_housing_cleaned.csv` | Cleaned data with all generated features |
| `housing_schema.sql` | Explicit schema for the four database tables |
| `housing_dimensions.sql` | Creates dimensions after a fresh Python load |
| `housing_queries.sql` | Seventeen SQL validation/analysis queries |
| `luxury_housing_database.sql` | Tested full schema-and-data export |
| `sql_results/` | Actual SQL query outputs and validation evidence |
| `eda_tables/` | EDA statistics, cross-tabs, correlation table, and outlier review records |
| `charts/` and `housing_dashboard.png` | Charts from the supplied dataset |
| `PowerBI/LuxuryHousing.pbip` | Editable Power BI report project |
| `power_bi_measures.dax` | All 22 measures in a readable file |
| `power_bi_guide.md` | Opening, refreshing, checking, and saving the report |
| `FINAL_REPORT.md` | Pipeline explanation, findings, and requirement coverage |
| `EVALUATION_GUIDE.md` | Beginner explanations and sample evaluation answers |
| `SUBMISSION_CHECKLIST.md` | Final checks and remaining submission actions |

## Dataset and important limitations

Brief: https://docs.google.com/document/d/1MBye-iAOpiKecfwVoSItegwqMNi0A5O8Srq9v2ck3PY/edit

CSV source: https://drive.google.com/file/d/1nLi3uMk3MPj5TnBZ1hO5_30_-MGVq_Vm/view

The raw file has 101,000 rows and 18 columns. It contains 1,000 exact duplicates.
Cleaning retains 100,000 distinct property records across 11 builders, 16
micro-markets, and eight quarters from April 2023 to March 2025.

`Developer_Name` is renamed to `Builder`. `Property_ID` is the row identifier.
`Project_Name` is retained because the actual file has no `Project_ID`.
Names alone do not guarantee unique projects across developers or localities.

There is **no Booking_Status column**. The pipeline adds `Unknown` status and
empty `Booking_Flag` values. `Primary`/`Secondary` transaction type is not used
to invent bookings. Totals are called recorded ticket values, not verified revenue.

## Install Python libraries

Open a terminal in this project folder:

```powershell
python -m pip install -r requirements.txt
```

For the optional notebook, also install JupyterLab:

```powershell
python -m pip install jupyterlab
python -m jupyter lab
```

## Run the Python workflow

Download the raw source CSV, then run:

```powershell
python luxury_housing_analysis.py
```

Enter its path and an output folder. Paths containing spaces and quoted paths
are supported. Choose `no` for cleaning only or `yes` for MySQL loading.

For a fresh SQL load, create an empty database in MySQL Workbench first:

```sql
CREATE DATABASE luxury_housing CHARACTER SET utf8mb4;
```

The Python script asks for connection details and a hidden password. It creates
`housing_sales`, adds the property primary key and analysis indexes, and inserts
1,000 rows per batch. An existing table causes loading to stop, protecting it from
replacement or duplicate insertion. MySQL DDL is not fully transactional; inspect
an empty/partial table after any interrupted load and use a fresh database for a
clean rerun.

After a successful fresh Python load, select the database and run
`housing_dimensions.sql`. Then run `housing_queries.sql`.

For a faster setup, use the tested export instead of rerunning the loader:

```powershell
mysql -u YOUR_USER -p < luxury_housing_database.sql
```

The `<` redirection example is for Command Prompt or a compatible shell;
PowerShell users can instead open the SQL export in MySQL Workbench and execute
it. Restore only into a new empty database. The export creates all four tables
and inserts their data. Do not run the schema or dimension scripts again after
restoring the complete export.

`housing_schema.sql` is the separately reviewable schema. It is not a prerequisite
for the Python loader, which creates its own table. Choose one creation path.

Run the charts and EDA with the cleaned CSV:

```powershell
python housing_visualizations.py
python housing_eda.py
```

Each asks for a CSV path and output folder. Existing output files with the same
names are regenerated. Keep the original raw CSV in another folder.

## Power BI

Read `power_bi_guide.md`. Open `PowerBI/LuxuryHousing.pbip` in a current Power BI
Desktop version. The project points to `127.0.0.1:33307`, database `luxury_housing`,
matching the isolated database used during preparation. Change the two Power
Query parameters for your own server. A standard local installation usually
uses port 3306.

Credentials are not embedded in the report or submission ZIP. Enter your own
database credentials in Power BI. On the preparation computer, a separate
`LOCAL_DATABASE_ACCESS.txt` file outside the submission folder gives the local
read-only account. The test server is not registered as a Windows service and
does not start automatically after a reboot.

MySQL is an **Import** source for the native Power BI connector. Use Refresh for
updates. Confirm this meets the brief's "live connection" wording with the
instructor. There is no claim of MySQL DirectQuery.

## Beginner explanation of the features

- `Price_per_Sqft`: crore price multiplied by 10,000,000, divided by unit size.
- `Quarter`: calendar year and quarter, e.g. `2024Q1`.
- `Fiscal_Year`: India's April-March financial year, e.g. `FY2023-24`.
- `Fiscal_Quarter`: April-June is Q1; January-March is Q4.
- `Amenity_Score_Was_Missing`: 1 means that the original score was absent.
- `Ticket_Price_Outlier`: 1 flags a price outside the 1.5-IQR review limits.
- `Comment_Sentiment`: documented keyword labels; this is not machine learning.
- `Booking_Flag`: 1 for explicit Booked, 0 for explicit Not Booked, empty otherwise.
- `Market_Location`: source locality plus Bengaluru, Karnataka, India; no invented coordinates.

Prices and sizes that are missing or non-positive stay missing. Amenity scores
use the median, and the original-missing flag preserves that distinction.
Correlations and amenity comparisons use observed scores, not imputed values.
High positive prices remain in the dataset and are flagged for review.

## GitHub and submission

The packaged project can be uploaded to your chosen GitHub repository. Do not
upload local database credentials, runtime binaries, or Python environment folders.
The `.gitignore` excludes those. A local Git repository was prepared separately;
the ZIP contains project files rather than `.git` internals.

Read `SUBMISSION_CHECKLIST.md` before submitting. Final desktop verification,
instructor clarification, repository publication, and portal submission remain
human/external steps; the documentation does not claim they have occurred.
