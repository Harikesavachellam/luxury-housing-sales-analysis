# Beginner explanation for evaluation

## A short project introduction

"My project analyses the supplied Bengaluru luxury housing dataset. I clean it
with pandas, load it into MySQL, and use Power BI definitions to compare prices,
builders, markets, configurations, channels, and buyer groups. I removed 1,000
exact duplicates, leaving 100,000 property records. The source has no booking
status, so I report that limitation rather than assuming successful bookings."

Only say that the Power BI dashboard was refreshed and verified after you have
actually completed those steps in Desktop.

## Explain the Python functions

`clean_data()` receives a DataFrame, which is a table in Python. It makes a copy,
removes repeated rows, standardizes labels, converts prices and dates, handles
missing data, and creates new columns.

`label_comment()` checks a short list of words. "Excellent" or "great" produces
Positive. "Too far", "poor", or "not responsive" produces Negative. Both produces
Mixed. Other feedback is Neutral; absent feedback is No comment.

`load_to_mysql()` asks for connection details. `write_to_mysql()` creates the
table and sends rows to MySQL. Separating input from loading lets the same loading
function be checked automatically.

`run_eda()` produces statistics, category summaries, cross-tabs, correlations,
and six charts. `create_charts()` creates the simple four-chart dashboard.

## Common questions and clear answers

**Why remove duplicates?** An exact repeated row would inflate counts and price
totals. Different properties in the same project are retained.

**Why use the median for missing amenity scores?** The median is the middle
observed score and is less sensitive to extreme values than the mean. I keep a
flag showing which scores were filled and exclude them from observed-score
correlations.

**Why not fill missing prices?** Estimated prices would alter ticket totals.
Missing prices and sizes remain missing; price coverage is reported separately.

**How do you clean a price such as `₹9.82 Cr`?** Remove the currency symbol and
crore label, then convert `9.82` to a number. The column is interpreted in crores.
Arbitrary lakh or rupee formats would need extra unit-conversion logic.

**How is price per square foot calculated?** For 2 crore and 4,000 square feet,
`2 * 10000000 / 4000 = 5000` rupees per square foot.

**What is an outlier?** A value outside the lower/upper limits based on 1.5 times
the interquartile range. It is flagged for investigation and is not automatically
deleted.

**What is the difference between a calendar and fiscal quarter?** Calendar Q1
is January-March. In the Indian April-March financial year, January-March is Q4.
For example, March 2024 is `2024Q1` and `FY2023-24 Q4`.

**What does GROUP BY do?** It combines rows into groups so COUNT, SUM, and AVG
can summarize builders, localities, quarters, or other categories.

**Why a primary key?** `Property_ID` uniquely identifies a property record.
An index on builders, markets, and fiscal quarters supports common filters.

**What are dimensions?** Small lookup tables for builders, markets, and quarters.
The housing table contains the property records. Power BI uses the lookup tables
to filter the records through one-to-many relationships.

**How was SQL loading verified?** MySQL contained 100,000 rows. SQL missing-value
counts and the ticket total matched pandas, the three joins had no orphan keys,
and a full database export was restored into a second database and checked.

**What does a DAX measure do?** It calculates a result for the current filters.
`Total Records = COUNTROWS(housing_sales)` changes when a slicer selects a builder,
market, or quarter.

**Why use DIVIDE?** It handles a zero denominator safely. Booking conversion
stays blank when there are no known outcomes.

**What does correlation mean here?** Pearson correlation measures a linear
association. Amenity score and ticket price have correlation about 0.002 among
81,084 complete observed pairs, giving little evidence of a linear relationship.
This does not establish cause and effect or booking behavior.

**What are the main findings?** Prestige has the largest recorded ticket total;
Sobha has the highest average observed ticket price. Configuration and channel
counts are close to evenly distributed. Booking success cannot be assessed.

**Is this an ML project?** No model training is required by this brief. This is
an EDA, data preparation, SQL, and Power BI analytics project. The keyword comment
labels are transparent rules.

**What are the main limitations?** Missing booking status, incomplete prices and
unit sizes, imputed amenity scores, possibly repeated project names, and locality
names without verified coordinates. The dataset's representativeness has not
been established, so findings describe this source rather than Bengaluru's whole market.

## Suggested 12-minute explanation

Spend about two minutes on the problem and source, three on cleaning and
features, two on SQL and validation, three on the verified Power BI visuals,
and two on findings and limitations. Use the actual local results and avoid
claiming verification that has not been performed.
