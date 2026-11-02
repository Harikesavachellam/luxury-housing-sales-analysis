# Open and verify the Power BI project

The report definitions are prepared. Native Power BI Desktop verification is
the remaining step. This folder is a real editable `.pbip` project, not a `.pbix`
binary or a screenshot of Power BI.

## Open

1. Install a current Power BI Desktop release from Microsoft.
2. Open `LuxuryHousing.pbip`, keeping the adjacent Report and SemanticModel
   folders together. Use a version supporting Power BI project files and PBIR.
   If your version asks, enable the relevant Power BI project preview options.
3. Follow the MySQL connector's current dependency instructions if prompted
   (the native connector commonly requires MySQL Connector/NET).
4. In **Transform data > Manage parameters**, set `MySQLServer` and
   `MySQLDatabase`. Defaults are `127.0.0.1:33307` and `luxury_housing`.
5. Enter SQL database credentials when prompted. No password is saved in the
   project. The preparation computer's local read-only credentials are stored
   separately outside the public submission folder.
6. Refresh the report. It imports the four SQL tables.

To use your own normal MySQL instance, restore `luxury_housing_database.sql` into
a fresh empty database, then change `MySQLServer` to your server and port,
commonly `localhost:3306`. Use credentials that have SELECT access to the four
tables. Restore is a one-time setup; refresh is read-only.

## Model

`housing_sales` contains 100,000 property records. The three dimensions are
`dim_builder` (11 rows), `dim_market` (16 rows), and `dim_quarter` (8 rows).
The dimensions filter the housing table through one-to-many, single-direction
relationships on Builder, Micro_Market, and Purchase_Quarter.

Fiscal-quarter labels sort by `Fiscal_Quarter_Sort`; calendar-quarter labels
sort by the actual quarter-end date. The model contains 22 measures, copied in
`power_bi_measures.dax` at the project root.

## Pages

1. **Market overview:** builder/market/quarter slicers, cards, quarter trends,
   configuration donut, top-five builder chart, and builder performance table.
2. **Markets and buyers:** locality map and fallback table, possession/buyer
   composition, and sales-channel volume.
3. **Pricing and quality:** missing-data cards, observed amenity/price scatter,
   quarterly builder matrix, keyword comment labels, and feedback details.
4. **Booking data limits:** source limitation, known outcome count, unavailable
   booking measures, and market coverage table.

All pages have builder, market, and fiscal-quarter slicers. Each page is
1280 by 1000 with visual containers inside its bounds.

## Check after refreshing

With slicers clear, verify:

| Measure | Expected value |
|---|---:|
| Total Records | 100,000 |
| Recorded Ticket Value Cr | 1,145,825.59 |
| Average Ticket Price Cr | 12.72 |
| Priced Records | 90,082 |
| Price Coverage | 90.082% |
| Missing Price Records | 9,918 |
| Missing Size Records | 10,457 |
| Filled Amenity Records | 10,000 |
| Price Outlier Records | 1,552 |
| Known Booking Outcomes | 0 |
| Booking Count / Conversion / Booked Ticket Value | Blank / unavailable |

Select a builder, locality, and fiscal quarter and confirm that all relevant
charts and cards change. Review the scatter's category, X, Y, and Size field
roles and the matrix's rows/columns/values if your Desktop release adjusts them.

Check that locality addresses resolve within Bengaluru. The source has no
coordinates; geocoding is unverified. If map visuals are disabled by your
organization or a locality resolves incorrectly, retain the locality table and
document the limitation. No real coordinates have been fabricated.

The amenity scatter uses market averages of observed scores and prices. It
does not measure booking conversion. The written EDA separately calculates
correlation on individual complete observed pairs.

After checks pass, capture screenshots of every report page and save
`LuxuryHousing.pbix` using **File > Save As** if required. Add the screenshots to
the documentation and update the verification checklist with what was actually
checked.

## Connection limitation

The native MySQL connector supports Import, not DirectQuery. Refresh updates
the imported data. Confirm with the instructor whether that satisfies the brief's
"live connection" wording. If true DirectQuery is mandatory, a supported SQL
Server setup and different source expressions will be necessary.

## Verification evidence included

`definition_validation.json` records Microsoft schema validation and field/bounds
checks. `model_validation.json` records successful deserialization through
Microsoft's Tabular Object Model. These checks do not execute DAX, connect from
Desktop, or confirm native visual rendering. The project has not been marked
fully verified on the strength of those checks alone.
