# Power BI Dashboard Guide
## E-Commerce Sales & Customer Analytics

---

## Dashboard Architecture

```
ecommerce_dashboard.pbix
├── Page 1: Executive Overview (KPI Cards)
├── Page 2: Sales Trend Analysis
├── Page 3: Profit & Category Analysis
├── Page 4: Customer & RFM Insights
└── Page 5: Product Performance
```

---

## Step 1 — Connect Data Source

1. Open Power BI Desktop
2. **Home → Get Data → Text/CSV** → Select `superstore_clean.csv`
3. In Power Query Editor:
   - Set `Order Date` and `Ship Date` → **Date** type
   - Set `Sales`, `Profit`, `Discount` → **Decimal Number**
   - Set `Quantity` → **Whole Number**
4. Click **Close & Apply**

---

## Step 2 — Create a Date Table (Mark as Date Table)

```dax
Date Table =
CALENDAR(
    MIN(superstore_sales[Order Date]),
    MAX(superstore_sales[Order Date])
)
```

Add columns to the Date Table:

```dax
Year         = YEAR([Date])
Month Number = MONTH([Date])
Month Name   = FORMAT([Date], "MMM")
Quarter      = "Q" & QUARTER([Date])
Week Number  = WEEKNUM([Date])
Day Name     = FORMAT([Date], "ddd")
Year-Month   = FORMAT([Date], "YYYY-MMM")
```

Create relationship:
`Date Table[Date]` → `superstore_sales[Order Date]` (Many-to-One)

---

## Step 3 — DAX Measures

### KPI Measures

```dax
-- ── Core Revenue ──────────────────────────────
Total Revenue =
    SUM(superstore_sales[Sales])

Total Profit =
    SUM(superstore_sales[Profit])

Total Orders =
    DISTINCTCOUNT(superstore_sales[Order ID])

Total Customers =
    DISTINCTCOUNT(superstore_sales[Customer ID])

Total Units Sold =
    SUM(superstore_sales[Quantity])

-- ── Derived KPIs ─────────────────────────────
Profit Margin % =
    DIVIDE([Total Profit], [Total Revenue], 0) * 100

Avg Order Value =
    DIVIDE([Total Revenue], [Total Orders], 0)

Avg Profit Per Order =
    DIVIDE([Total Profit], [Total Orders], 0)

Avg Shipping Days =
    AVERAGEX(
        superstore_sales,
        DATEDIFF(superstore_sales[Order Date], superstore_sales[Ship Date], DAY)
    )

-- ── Growth Metrics ────────────────────────────
Revenue LY =
    CALCULATE(
        [Total Revenue],
        SAMEPERIODLASTYEAR('Date Table'[Date])
    )

YoY Revenue Growth % =
    DIVIDE([Total Revenue] - [Revenue LY], [Revenue LY], BLANK()) * 100

Revenue MTD =
    TOTALMTD([Total Revenue], 'Date Table'[Date])

Revenue QTD =
    TOTALQTD([Total Revenue], 'Date Table'[Date])

Revenue YTD =
    TOTALYTD([Total Revenue], 'Date Table'[Date])

-- ── Customer Metrics ─────────────────────────
Repeat Customers =
    CALCULATE(
        DISTINCTCOUNT(superstore_sales[Customer ID]),
        FILTER(
            VALUES(superstore_sales[Customer ID]),
            CALCULATE(DISTINCTCOUNT(superstore_sales[Order ID])) > 1
        )
    )

Repeat Customer Rate % =
    DIVIDE([Repeat Customers], [Total Customers], 0) * 100

Customer Lifetime Value =
    DIVIDE([Total Revenue], [Total Customers], 0)

-- ── Running Totals ────────────────────────────
Cumulative Revenue =
    CALCULATE(
        [Total Revenue],
        FILTER(
            ALL('Date Table'),
            'Date Table'[Date] <= MAX('Date Table'[Date])
        )
    )

-- ── Profitability Flags ───────────────────────
Loss-Making Orders =
    CALCULATE(
        DISTINCTCOUNT(superstore_sales[Order ID]),
        superstore_sales[Profit] < 0
    )

Loss Rate % =
    DIVIDE([Loss-Making Orders], [Total Orders], 0) * 100
```

---

## Step 4 — Dashboard Pages

---

### PAGE 1 — Executive Overview

**Layout:** 4 KPI Cards (top) + 2 charts (bottom)

**KPI Cards (use Card visual):**

| Card Title        | Measure             | Format   |
|-------------------|---------------------|----------|
| Total Revenue     | `[Total Revenue]`   | $#,##0   |
| Total Profit      | `[Total Profit]`    | $#,##0   |
| Profit Margin     | `[Profit Margin %]` | #0.00%   |
| Total Orders      | `[Total Orders]`    | #,##0    |
| Total Customers   | `[Total Customers]` | #,##0    |
| Avg Order Value   | `[Avg Order Value]` | $#,##0   |

**Bottom Row:**
- **Clustered Bar Chart**: Revenue & Profit by Category
- **Donut Chart**: Revenue share by Region (4 slices)

**Conditional formatting on KPI Cards:**
- Green if YoY growth > 0, Red if negative

---

### PAGE 2 — Sales Trend Analysis

**Visuals:**

1. **Line Chart** — Monthly Revenue Trend
   - X-axis: `Date Table[Year-Month]`
   - Y-axis: `[Total Revenue]`, `[Revenue LY]`
   - Legend: shows current vs prior year lines

2. **Clustered Column Chart** — Quarterly Revenue
   - X-axis: `Date Table[Quarter]`
   - Y-axis: `[Total Revenue]`
   - Small multiples: `Date Table[Year]`

3. **Area Chart** — Cumulative Revenue YTD
   - X-axis: `Date Table[Month Name]`
   - Y-axis: `[Revenue YTD]`

4. **Matrix** — Revenue by Year × Month
   - Rows: Year
   - Columns: Month Name
   - Values: `[Total Revenue]`
   - Conditional formatting: Green-White-Red color scale

**Slicers (top):** Year, Region, Category, Segment

---

### PAGE 3 — Profit & Category Analysis

**Visuals:**

1. **Waterfall Chart** — Profit breakdown by Sub-Category
   - Category: Sub-Category
   - Y: `[Total Profit]`
   - Color: Green for positive, Red for negative

2. **Scatter Chart** — Sales vs Profit by Product
   - X: `[Total Revenue]`
   - Y: `[Total Profit]`
   - Size: `[Total Units Sold]`
   - Legend: Category

3. **100% Stacked Bar** — Revenue mix by Region & Category
   - Y-axis: Region
   - X-axis: `[Total Revenue]`
   - Legend: Category

4. **Gauge Chart** — Overall Profit Margin
   - Value: `[Profit Margin %]`
   - Target: 15% (industry benchmark)
   - Min: 0, Max: 40

5. **Table** — Sub-Category Performance
   - Columns: Sub-Category, Revenue, Profit, Margin %, Avg Discount
   - Conditional formatting on Profit column

---

### PAGE 4 — Customer Insights

**Visuals:**

1. **Funnel Chart** — Customer Segments (RFM)
   - Champions → Loyal → Potential → At-Risk → Lost

2. **Bar Chart** — Top 10 Customers by Revenue
   - Y-axis: Customer Name
   - X-axis: `[Total Revenue]`
   - Data labels: ON

3. **Clustered Bar** — Revenue by Segment × Region
   - Small multiples: Region

4. **KPI Cards Row:**
   - Repeat Customer Rate: `[Repeat Customer Rate %]`
   - Avg Customer Lifetime Value: `[Customer Lifetime Value]`
   - Loss-Making Order Rate: `[Loss Rate %]`

5. **Decomposition Tree** — Revenue breakdown
   - Analyse: `[Total Revenue]`
   - Explain by: Region → Category → Segment → Ship Mode

---

### PAGE 5 — Product Performance

**Visuals:**

1. **Horizontal Bar** — Top 15 Products by Revenue
2. **Horizontal Bar** — Top 15 Products by Profit
3. **Matrix** — Category × Sub-Category Heatmap
   - Values: `[Total Revenue]` with color scale
4. **Slicer** — Category, Sub-Category filter

---

## Step 5 — Filters & Slicers

**Global slicers (sync across all pages):**

| Slicer        | Field                          | Type         |
|---------------|--------------------------------|--------------|
| Date Range    | `Date Table[Date]`             | Between      |
| Year          | `Date Table[Year]`             | Dropdown     |
| Region        | `superstore_sales[Region]`     | Tile buttons |
| Category      | `superstore_sales[Category]`   | Dropdown     |
| Segment       | `superstore_sales[Segment]`    | Dropdown     |
| Ship Mode     | `superstore_sales[Ship Mode]`  | Checkboxes   |

**To sync slicers across pages:**
- View → Sync Slicers → check all pages for each slicer

---

## Step 6 — Formatting & Branding

**Theme Colors:**
```
Primary:    #2E86AB  (Blue)
Profit:     #2A9D8F  (Teal)
Loss/Alert: #E63946  (Red)
Accent:     #F4A261  (Orange)
Background: #F8F9FA  (Light Grey)
Text:       #1D1D1D  (Dark)
```

**Import custom theme:**
1. View → Themes → Browse for themes
2. Upload `dashboard_theme.json` (create with the colors above)

**Report-level settings:**
- Canvas size: 16:9 (1280 × 720)
- Background: #F8F9FA
- Font: Segoe UI

---

## Step 7 — Publish

1. **File → Publish → Publish to Power BI**
2. Select your workspace
3. In Power BI Service:
   - Set **scheduled refresh** (daily)
   - Create a **Dashboard** from pinned report tiles
   - Share with **View** access for stakeholders
   - Enable **Row Level Security (RLS)** if multi-region access needed

---

## DAX Quick Reference

```dax
-- Dynamic title with filter context
Page Title =
"Sales Analysis — "
& IF(ISFILTERED(superstore_sales[Region]),
     SELECTEDVALUE(superstore_sales[Region], "All Regions"),
     "All Regions")

-- Rank products by revenue
Product Revenue Rank =
RANKX(
    ALL(superstore_sales[Product Name]),
    [Total Revenue],
    ,
    DESC,
    DENSE
)

-- Top N filter for bar charts
Is Top 10 Product =
[Product Revenue Rank] <= 10
```
