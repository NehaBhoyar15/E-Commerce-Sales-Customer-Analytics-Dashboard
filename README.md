# 📊 E-Commerce Sales \& Customer Analytics Dashboard

!\[Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
!\[Pandas](https://img.shields.io/badge/Pandas-2.0-purple?logo=pandas)
!\[SQL](https://img.shields.io/badge/SQL-MySQL-orange?logo=mysql)
!\[Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?logo=powerbi)
!\[License](https://img.shields.io/badge/License-MIT-green)
!\[Status](https://img.shields.io/badge/Status-Complete-brightgreen)

> \*\*End-to-end data analytics project\*\* on a Superstore e-commerce dataset — covering data cleaning, EDA, SQL analysis, and an interactive Power BI dashboard with RFM customer segmentation and business insights.

\---

## 📌 Project Overview

This project simulates a real-world business intelligence engagement for an e-commerce company. A data analyst was tasked with uncovering revenue drivers, identifying unprofitable product lines, understanding customer behaviour, and building an executive-facing dashboard for strategic decision-making.

**Business Questions Answered:**

* Which product categories and regions drive the most revenue and profit?
* What is the impact of discounting on profitability?
* Who are our most valuable customers (RFM segmentation)?
* What are the monthly and quarterly sales growth trends?
* How does shipping mode affect customer satisfaction and margins?

\---

## 🛠️ Tech Stack

|Layer|Tools|
|-|-|
|**Language**|Python 3.9+|
|**Data Wrangling**|Pandas, NumPy|
|**Visualisation**|Matplotlib, Seaborn|
|**Database**|MySQL / SQLite (via pandas + sqlalchemy)|
|**BI Dashboard**|Microsoft Power BI Desktop|
|**Version Control**|Git / GitHub|
|**IDE**|Jupyter Notebook / VS Code|

\---

## 📁 Folder Structure

```
ecommerce\_analytics/
├── 📂 data/
│   ├── superstore\_raw.csv          # Original dataset
│   └── superstore\_clean.csv        # Cleaned \& feature-engineered dataset
│
├── 📂 scripts/
│   ├── data\_cleaning.py            # Data cleaning pipeline
│   └── eda\_analysis.py             # EDA + visualisations
│
├── 📂 notebooks/
│   └── ecommerce\_analytics.ipynb   # Full Jupyter notebook (end-to-end)
│
├── 📂 sql/
│   └── sql\_queries.sql             # 17 business SQL queries
│
├── 📂 dashboard/
│   ├── ecommerce\_dashboard.pbix    # Power BI dashboard file
│   ├── powerbi\_guide.md            # DAX measures + setup guide
│   └── 📂 plots/                   # Auto-generated EDA charts
│       ├── 01\_monthly\_sales\_trend.png
│       ├── 02\_profit\_analysis.png
│       ├── 03\_top\_products.png
│       ├── 04\_region\_analysis.png
│       ├── 05\_category\_performance.png
│       ├── 06\_customer\_segmentation.png
│       ├── 07\_correlation\_analysis.png
│       ├── 08\_shipping\_segment\_analysis.png
│       └── 09\_quarterly\_trend.png
│
├── 📂 docs/
│   ├── business\_insights.md        # Documented business findings
│   └── interview\_qa.md             # Interview Q\&A for this project
│
├── requirements.txt
└── README.md
```

\---

## ✨ Features

### 🧹 Data Cleaning (Python)

* Missing value imputation (median/mode strategies)
* Duplicate detection and removal
* Date parsing and formatting
* Data type enforcement
* IQR-based outlier flagging

### 🔧 Feature Engineering

* Order Year / Month / Quarter extraction
* Shipping lead time calculation
* Profit Margin % per transaction
* Revenue per Unit metric
* RFM scoring (Recency, Frequency, Monetary)
* Customer repeat-purchase classification
* Sales bucketing by value tier

### 📈 Exploratory Data Analysis

* Monthly \& quarterly sales trend analysis
* Year-over-Year revenue comparisons
* Category and sub-category profit heatmap
* Top 15 products by revenue and profit
* Region-wise sales and market share
* Correlation matrix (discount vs profit)
* RFM-based customer segmentation (5 segments)
* Shipping mode performance analysis

### 🗄️ SQL Analysis (17 Queries)

* KPI summary dashboard query
* Top customers by CLV and revenue
* Monthly revenue with MoM growth rate
* Quarterly revenue with running YTD total
* Discount band impact on profitability
* Loss-making product identification
* Customer purchase frequency distribution
* Repeat vs new customer revenue split
* State-level performance ranking

### 📊 Power BI Dashboard (5 Pages)

* **Page 1:** Executive KPI Overview
* **Page 2:** Sales Trend Analysis (Line, Area, Matrix)
* **Page 3:** Profit \& Category Analysis (Waterfall, Scatter, Gauge)
* **Page 4:** Customer Insights (RFM Funnel, Decomposition Tree)
* **Page 5:** Product Performance (Top N charts, Heatmap)
* Cross-page slicers: Date, Region, Category, Segment, Ship Mode
* DAX measures: YoY growth, MTD/QTD/YTD, Cumulative Revenue, CLV

\---

## 📸 Dashboard Screenshots

> \_Screenshots of the Power BI dashboard pages (add after building the .pbix file)\_

|Page|Preview|
|-|-|
|Executive Overview|`docs/screenshots/page1\_overview.png`|
|Sales Trend|`docs/screenshots/page2\_sales\_trend.png`|
|Profit Analysis|`docs/screenshots/page3\_profit.png`|
|Customer Insights|`docs/screenshots/page4\_customers.png`|
|Product Performance|`docs/screenshots/page5\_products.png`|

\---

## 🚀 How to Run the Project

### Prerequisites

```bash
Python 3.9+
pip install pandas numpy matplotlib seaborn sqlalchemy jupyter
```

Or install all dependencies at once:

```bash
pip install -r requirements.txt
```

### Step 1 — Get the Dataset

Download the **Sample Superstore** dataset from:

* [Kaggle — Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
* Save as `data/superstore\_raw.csv`

### Step 2 — Run Data Cleaning

```bash
cd scripts
python data\_cleaning.py
# Output: ../data/superstore\_clean.csv
```

### Step 3 — Run EDA

```bash
python eda\_analysis.py
# Output: ../dashboard/plots/\*.png
```

### Step 4 — Run Jupyter Notebook (optional)

```bash
cd ..
jupyter notebook notebooks/ecommerce\_analytics.ipynb
```

### Step 5 — SQL Analysis

Load `superstore\_clean.csv` into MySQL or SQLite:

```python
import pandas as pd
import sqlalchemy

engine = sqlalchemy.create\_engine("sqlite:///ecommerce.db")
df = pd.read\_csv("data/superstore\_clean.csv")
df.to\_sql("superstore\_sales", engine, if\_exists="replace", index=False)
```

Then run `sql/sql\_queries.sql` in your SQL client.

### Step 6 — Power BI Dashboard

1. Open `dashboard/ecommerce\_dashboard.pbix` in Power BI Desktop
2. Update the data source path to your `superstore\_clean.csv`
3. Click **Refresh** → explore all 5 pages
4. See `dashboard/powerbi\_guide.md` for full setup and DAX reference

\---

## 💡 Key Business Insights

1. **Technology** is the highest-revenue category ($836K), but **Office Supplies** has the best profit margin (17.4%).
2. **Discounts above 20% consistently produce losses** — the correlation between discount rate and profit is −0.22.
3. The **West region** leads in revenue (31.6% share), while the **Central region** has the lowest profit margin.
4. **23% of customers are "Champions"** (RFM) and contribute **47% of total revenue**.
5. **Tables and Bookcases** are the top loss-making sub-categories despite healthy sales volume.
6. **Q4 consistently peaks** — averaging 35% higher revenue than Q1, driven by holiday purchasing.
7. **Standard Class shipping** is used for 60% of orders but has the longest lead time (5 days avg).

\---

## 📋 Dataset

* **Source:** Tableau Sample Superstore / Kaggle
* **Rows:** \~9,994 order line items
* **Columns:** 21 (Order ID, Customer Name, Region, Category, Sub-Category, Product Name, Sales, Profit, Quantity, Discount, Ship Mode, Segment, State, City, etc.)
* **Time Range:** 2019–2022 (4 years)

\---

## 👤 Author

**\[NEHA BHOYAR**
Data Analyst Intern | Python · SQL · Power BI
📧 bhoyarneha815@gmail.com

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

\---

*⭐ If you found this project useful, please star the repo!*

