"""
========================================================
  E-Commerce Sales & Customer Analytics Dashboard
  Script 2: Exploratory Data Analysis (EDA)
  Author  : Data Analyst Intern
  Tools   : Pandas, NumPy, Matplotlib, Seaborn
========================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

# ── Global plot style ──────────────────────────────────
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams.update({
    "figure.dpi":       150,
    "axes.titlesize":   13,
    "axes.labelsize":   11,
    "xtick.labelsize":  9,
    "ytick.labelsize":  9,
    "legend.fontsize":  9,
    "figure.facecolor": "#F8F9FA",
    "axes.facecolor":   "#FFFFFF",
})
PALETTE    = sns.color_palette("Set2")
OUTPUT_DIR = "../dashboard/plots/"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ─────────────────────────────────────────────
# HELPER: save & show
# ─────────────────────────────────────────────
def save_fig(filename: str) -> None:
    path = os.path.join(OUTPUT_DIR, filename)
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.show()
    print(f"  📊 Saved → {path}")


# ─────────────────────────────────────────────
# 0. LOAD DATA
# ─────────────────────────────────────────────
def load_clean_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, parse_dates=["Order Date", "Ship Date"])
    print(f"✅ Clean data loaded: {df.shape}")
    return df


# ─────────────────────────────────────────────
# 1. KPI SUMMARY
# ─────────────────────────────────────────────
def kpi_summary(df: pd.DataFrame) -> dict:
    kpis = {
        "Total Revenue ($)":         round(df["Sales"].sum(), 2),
        "Total Profit ($)":          round(df["Profit"].sum(), 2),
        "Overall Profit Margin (%)": round((df["Profit"].sum() / df["Sales"].sum()) * 100, 2),
        "Total Orders":              df["Order ID"].nunique(),
        "Total Customers":           df["Customer Name"].nunique(),
        "Total Products":            df["Product Name"].nunique(),
        "Avg Order Value ($)":       round(df.groupby("Order ID")["Sales"].sum().mean(), 2),
        "Avg Shipping Days":         round(df["Shipping Days"].mean(), 1),
        "Repeat Customer Rate (%)":  round(
            (df[df["Is Repeat Customer"] == "Repeat"]["Customer Name"].nunique()
             / df["Customer Name"].nunique()) * 100, 2
        ),
    }
    print("\n" + "=" * 55)
    print("  📌  KEY PERFORMANCE INDICATORS")
    print("=" * 55)
    for k, v in kpis.items():
        print(f"  {k:<35}: {v:>12,}")
    print("=" * 55)
    return kpis


# ─────────────────────────────────────────────
# 2. MONTHLY SALES TREND
# ─────────────────────────────────────────────
def monthly_sales_trend(df: pd.DataFrame) -> None:
    monthly = (
        df.groupby(["Order Year", "Order Month"])["Sales"]
        .sum()
        .reset_index()
        .rename(columns={"Sales": "Monthly Sales"})
    )
    monthly["Period"] = pd.to_datetime(
        monthly["Order Year"].astype(str) + "-" + monthly["Order Month"].astype(str).str.zfill(2)
    )
    monthly.sort_values("Period", inplace=True)

    fig, axes = plt.subplots(2, 1, figsize=(14, 9))
    fig.suptitle("Monthly Sales Trend Analysis", fontsize=15, fontweight="bold", y=1.01)

    # ── Line chart: overall trend ──────────────
    ax1 = axes[0]
    ax1.plot(monthly["Period"], monthly["Monthly Sales"],
             color="#2E86AB", linewidth=2.2, marker="o", markersize=4, label="Monthly Sales")
    ax1.fill_between(monthly["Period"], monthly["Monthly Sales"],
                     alpha=0.15, color="#2E86AB")
    ax1.set_title("Overall Monthly Revenue ($)")
    ax1.set_ylabel("Revenue ($)")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax1.tick_params(axis="x", rotation=45)

    # ── Bar chart: year-over-year by month ──────
    ax2 = axes[1]
    pivot = monthly.pivot_table(index="Order Month", columns="Order Year",
                                values="Monthly Sales", aggfunc="sum")
    pivot.plot(kind="bar", ax=ax2, colormap="Set2", edgecolor="white", linewidth=0.5)
    ax2.set_title("Year-over-Year Monthly Comparison")
    ax2.set_ylabel("Revenue ($)")
    ax2.set_xlabel("Month")
    ax2.set_xticklabels(
        ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
        rotation=0
    )
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax2.legend(title="Year")

    save_fig("01_monthly_sales_trend.png")


# ─────────────────────────────────────────────
# 3. PROFIT ANALYSIS
# ─────────────────────────────────────────────
def profit_analysis(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle("Profit Analysis", fontsize=15, fontweight="bold")

    # ── Profit by category ────────────────────
    cat_profit = df.groupby("Category")["Profit"].sum().sort_values()
    colors = ["#E63946" if v < 0 else "#2A9D8F" for v in cat_profit]
    cat_profit.plot(kind="barh", ax=axes[0], color=colors, edgecolor="white")
    axes[0].set_title("Profit by Category")
    axes[0].set_xlabel("Profit ($)")
    axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    # ── Profit vs Sales scatter ───────────────
    axes[1].scatter(df["Sales"], df["Profit"],
                    c=df["Profit"].apply(lambda x: "#2A9D8F" if x > 0 else "#E63946"),
                    alpha=0.35, s=18, edgecolors="none")
    axes[1].axhline(0, color="grey", linewidth=1, linestyle="--")
    axes[1].set_title("Sales vs Profit Scatter")
    axes[1].set_xlabel("Sales ($)")
    axes[1].set_ylabel("Profit ($)")
    axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    # ── Profit margin distribution ────────────
    axes[2].hist(df["Profit Margin (%)"].clip(-100, 100), bins=40,
                 color="#457B9D", edgecolor="white", linewidth=0.5)
    axes[2].axvline(df["Profit Margin (%)"].median(), color="#E63946",
                    linestyle="--", linewidth=1.5, label=f"Median: {df['Profit Margin (%)'].median():.1f}%")
    axes[2].set_title("Profit Margin Distribution")
    axes[2].set_xlabel("Profit Margin (%)")
    axes[2].set_ylabel("Frequency")
    axes[2].legend()

    save_fig("02_profit_analysis.png")


# ─────────────────────────────────────────────
# 4. TOP-SELLING PRODUCTS
# ─────────────────────────────────────────────
def top_products(df: pd.DataFrame, n: int = 15) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(18, 7))
    fig.suptitle(f"Top {n} Products", fontsize=15, fontweight="bold")

    # ── By revenue ────────────────────────────
    top_rev = (df.groupby("Product Name")["Sales"]
               .sum().nlargest(n).sort_values())
    top_rev.plot(kind="barh", ax=axes[0], color="#2E86AB", edgecolor="white")
    axes[0].set_title(f"Top {n} Products by Revenue")
    axes[0].set_xlabel("Revenue ($)")
    axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    # ── By profit ─────────────────────────────
    top_prof = (df.groupby("Product Name")["Profit"]
                .sum().nlargest(n).sort_values())
    top_prof.plot(kind="barh", ax=axes[1], color="#2A9D8F", edgecolor="white")
    axes[1].set_title(f"Top {n} Products by Profit")
    axes[1].set_xlabel("Profit ($)")
    axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    save_fig("03_top_products.png")


# ─────────────────────────────────────────────
# 5. REGION-WISE SALES
# ─────────────────────────────────────────────
def region_analysis(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle("Region-Wise Analysis", fontsize=15, fontweight="bold")

    region_metrics = df.groupby("Region").agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    ).reset_index()

    # ── Revenue bar ───────────────────────────
    sns.barplot(data=region_metrics, x="Region", y="Revenue",
                palette="Set2", ax=axes[0], edgecolor="white")
    axes[0].set_title("Revenue by Region")
    axes[0].set_ylabel("Revenue ($)")
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    axes[0].bar_label(axes[0].containers[0],
                      labels=[f"${v:,.0f}" for v in region_metrics["Revenue"]],
                      padding=4, fontsize=8)

    # ── Profit bar ────────────────────────────
    colors = ["#E63946" if v < 0 else "#2A9D8F" for v in region_metrics["Profit"]]
    axes[1].bar(region_metrics["Region"], region_metrics["Profit"],
                color=colors, edgecolor="white")
    axes[1].set_title("Profit by Region")
    axes[1].set_ylabel("Profit ($)")
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    # ── Pie: orders share ─────────────────────
    axes[2].pie(region_metrics["Orders"], labels=region_metrics["Region"],
                autopct="%1.1f%%", startangle=90,
                colors=sns.color_palette("Set2", len(region_metrics)),
                wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    axes[2].set_title("Order Share by Region")

    save_fig("04_region_analysis.png")


# ─────────────────────────────────────────────
# 6. CATEGORY PERFORMANCE
# ─────────────────────────────────────────────
def category_performance(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Category & Sub-Category Performance", fontsize=15, fontweight="bold")

    # ── Sales by category ─────────────────────
    cat = df.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
    x = np.arange(len(cat))
    w = 0.35
    axes[0, 0].bar(x - w/2, cat["Sales"],   width=w, label="Sales",  color="#2E86AB", edgecolor="white")
    axes[0, 0].bar(x + w/2, cat["Profit"],  width=w, label="Profit", color="#2A9D8F", edgecolor="white")
    axes[0, 0].set_xticks(x)
    axes[0, 0].set_xticklabels(cat["Category"])
    axes[0, 0].set_title("Sales vs Profit by Category")
    axes[0, 0].set_ylabel("Amount ($)")
    axes[0, 0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    axes[0, 0].legend()

    # ── Sub-category revenue heatmap ──────────
    sub_cat = (df.groupby(["Category", "Sub-Category"])["Sales"]
               .sum().unstack(fill_value=0))
    sns.heatmap(sub_cat / 1000, annot=True, fmt=".1f", cmap="YlGnBu",
                ax=axes[0, 1], linewidths=0.5, cbar_kws={"label": "Revenue ($K)"})
    axes[0, 1].set_title("Revenue Heatmap (Category × Sub-Category, $K)")

    # ── Quantity sold by sub-category ─────────
    qty = (df.groupby("Sub-Category")["Quantity"]
           .sum().sort_values(ascending=False))
    colors_qty = sns.color_palette("husl", len(qty))
    qty.plot(kind="bar", ax=axes[1, 0], color=colors_qty, edgecolor="white")
    axes[1, 0].set_title("Quantity Sold by Sub-Category")
    axes[1, 0].set_ylabel("Units Sold")
    axes[1, 0].tick_params(axis="x", rotation=45)

    # ── Discount vs Profit by category ────────
    sns.boxplot(data=df, x="Category", y="Discount",
                palette="Set2", ax=axes[1, 1], linewidth=1)
    axes[1, 1].set_title("Discount Distribution by Category")
    axes[1, 1].set_ylabel("Discount Rate")

    save_fig("05_category_performance.png")


# ─────────────────────────────────────────────
# 7. CUSTOMER SEGMENTATION
# ─────────────────────────────────────────────
def customer_segmentation(df: pd.DataFrame) -> None:
    # RFM: Recency, Frequency, Monetary
    snapshot_date = df["Order Date"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("Customer Name").agg(
        Recency  = ("Order Date",   lambda x: (snapshot_date - x.max()).days),
        Frequency= ("Order ID",     "nunique"),
        Monetary = ("Sales",        "sum"),
    ).reset_index()

    # Score each dimension (1=worst, 4=best)
    rfm["R_Score"] = pd.qcut(rfm["Recency"],   q=4, labels=[4, 3, 2, 1])
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), q=4, labels=[1, 2, 3, 4])
    rfm["M_Score"] = pd.qcut(rfm["Monetary"],  q=4, labels=[1, 2, 3, 4])
    rfm["RFM_Score"] = (
        rfm["R_Score"].astype(int) +
        rfm["F_Score"].astype(int) +
        rfm["M_Score"].astype(int)
    )

    def segment(score):
        if score >= 10: return "Champions"
        elif score >= 8: return "Loyal Customers"
        elif score >= 6: return "Potential Loyalists"
        elif score >= 4: return "At-Risk Customers"
        else: return "Lost Customers"

    rfm["Segment"] = rfm["RFM_Score"].apply(segment)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle("Customer Segmentation — RFM Analysis", fontsize=15, fontweight="bold")

    # ── Segment distribution ──────────────────
    seg_counts = rfm["Segment"].value_counts()
    colors_seg = sns.color_palette("Set2", len(seg_counts))
    axes[0].pie(seg_counts.values, labels=seg_counts.index,
                autopct="%1.1f%%", startangle=90,
                colors=colors_seg, wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    axes[0].set_title("Customer Segment Distribution")

    # ── Avg monetary by segment ───────────────
    seg_money = rfm.groupby("Segment")["Monetary"].mean().sort_values(ascending=False)
    sns.barplot(x=seg_money.index, y=seg_money.values,
                palette="Set2", ax=axes[1], edgecolor="white")
    axes[1].set_title("Avg Revenue by Segment")
    axes[1].set_ylabel("Avg Revenue ($)")
    axes[1].tick_params(axis="x", rotation=30)
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    # ── RFM scatter: Frequency vs Monetary ────
    palette_map = {
        "Champions": "#2A9D8F",
        "Loyal Customers": "#457B9D",
        "Potential Loyalists": "#E9C46A",
        "At-Risk Customers": "#F4A261",
        "Lost Customers": "#E63946",
    }
    for seg, grp in rfm.groupby("Segment"):
        axes[2].scatter(grp["Frequency"], grp["Monetary"],
                        label=seg, alpha=0.65, s=30,
                        color=palette_map.get(seg, "grey"), edgecolors="none")
    axes[2].set_title("Frequency vs Monetary Value")
    axes[2].set_xlabel("Order Frequency")
    axes[2].set_ylabel("Total Revenue ($)")
    axes[2].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    axes[2].legend(fontsize=7, loc="upper left")

    save_fig("06_customer_segmentation.png")
    print(f"\n  RFM Segments:\n{rfm['Segment'].value_counts().to_string()}")
    return rfm


# ─────────────────────────────────────────────
# 8. CORRELATION ANALYSIS
# ─────────────────────────────────────────────
def correlation_analysis(df: pd.DataFrame) -> None:
    numeric_cols = ["Sales", "Profit", "Quantity", "Discount",
                    "Shipping Days", "Profit Margin (%)", "Revenue per Unit"]
    corr = df[numeric_cols].corr()

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle("Correlation Analysis", fontsize=15, fontweight="bold")

    # ── Heatmap ───────────────────────────────
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f",
                cmap="RdYlGn", center=0, linewidths=0.5,
                ax=axes[0], cbar_kws={"shrink": 0.8})
    axes[0].set_title("Correlation Heatmap")

    # ── Discount vs Profit scatter ────────────
    axes[1].scatter(df["Discount"], df["Profit"],
                    alpha=0.25, s=15, color="#457B9D", edgecolors="none")
    m, b = np.polyfit(df["Discount"], df["Profit"], 1)
    x_line = np.linspace(df["Discount"].min(), df["Discount"].max(), 100)
    axes[1].plot(x_line, m * x_line + b,
                 color="#E63946", linewidth=2, label=f"Trend (slope={m:.1f})")
    axes[1].axhline(0, color="grey", linewidth=1, linestyle="--")
    axes[1].set_title("Discount Rate vs Profit")
    axes[1].set_xlabel("Discount Rate")
    axes[1].set_ylabel("Profit ($)")
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    axes[1].legend()

    save_fig("07_correlation_analysis.png")
    print(f"\n  Key Correlations with Profit:\n{corr['Profit'].drop('Profit').sort_values().to_string()}")


# ─────────────────────────────────────────────
# 9. SHIPPING & SEGMENT ANALYSIS
# ─────────────────────────────────────────────
def shipping_segment_analysis(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle("Shipping Mode & Customer Segment Analysis", fontsize=15, fontweight="bold")

    # ── Ship mode distribution ─────────────────
    ship = df["Ship Mode"].value_counts()
    axes[0].pie(ship.values, labels=ship.index,
                autopct="%1.1f%%", startangle=90,
                colors=sns.color_palette("Set2", len(ship)),
                wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    axes[0].set_title("Order Share by Ship Mode")

    # ── Shipping days boxplot ─────────────────
    sns.boxplot(data=df, x="Ship Mode", y="Shipping Days",
                palette="Set2", ax=axes[1], linewidth=1,
                order=["Same Day", "First Class", "Second Class", "Standard Class"])
    axes[1].set_title("Shipping Days by Ship Mode")
    axes[1].set_ylabel("Days to Ship")
    axes[1].tick_params(axis="x", rotation=20)

    # ── Segment revenue ───────────────────────
    seg_rev = df.groupby("Segment")["Sales"].sum().sort_values(ascending=False)
    sns.barplot(x=seg_rev.index, y=seg_rev.values,
                palette="Set2", ax=axes[2], edgecolor="white")
    axes[2].set_title("Revenue by Customer Segment")
    axes[2].set_ylabel("Revenue ($)")
    axes[2].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    axes[2].bar_label(axes[2].containers[0],
                      labels=[f"${v:,.0f}" for v in seg_rev.values],
                      padding=4, fontsize=8)

    save_fig("08_shipping_segment_analysis.png")


# ─────────────────────────────────────────────
# 10. QUARTERLY SALES TREND
# ─────────────────────────────────────────────
def quarterly_trend(df: pd.DataFrame) -> None:
    qtr = df.groupby(["Order Year", "Order Quarter"])["Sales"].sum().reset_index()
    qtr["Period"] = "Q" + qtr["Order Quarter"].astype(str) + " " + qtr["Order Year"].astype(str)

    fig, ax = plt.subplots(figsize=(14, 5))
    colors = sns.color_palette("husl", len(qtr))
    bars = ax.bar(qtr["Period"], qtr["Sales"], color=colors, edgecolor="white", linewidth=0.5)
    ax.bar_label(bars, labels=[f"${v:,.0f}" for v in qtr["Sales"]], padding=4, fontsize=7, rotation=45)
    ax.set_title("Quarterly Revenue Trend", fontsize=14, fontweight="bold")
    ax.set_ylabel("Revenue ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.tick_params(axis="x", rotation=45)

    save_fig("09_quarterly_trend.png")


# ─────────────────────────────────────────────
# MAIN — RUN ALL EDA
# ─────────────────────────────────────────────
def run_eda_pipeline(clean_path: str) -> None:
    print("=" * 60)
    print("  EXPLORATORY DATA ANALYSIS PIPELINE")
    print("=" * 60)

    df = load_clean_data(clean_path)

    print("\n[1] KPI Summary")
    kpis = kpi_summary(df)

    print("\n[2] Monthly Sales Trend")
    monthly_sales_trend(df)

    print("\n[3] Profit Analysis")
    profit_analysis(df)

    print("\n[4] Top Products")
    top_products(df, n=15)

    print("\n[5] Region Analysis")
    region_analysis(df)

    print("\n[6] Category Performance")
    category_performance(df)

    print("\n[7] Customer Segmentation (RFM)")
    rfm = customer_segmentation(df)

    print("\n[8] Correlation Analysis")
    correlation_analysis(df)

    print("\n[9] Shipping & Segment Analysis")
    shipping_segment_analysis(df)

    print("\n[10] Quarterly Trend")
    quarterly_trend(df)

    print("\n" + "=" * 60)
    print("  ✅ EDA COMPLETE — All charts saved to dashboard/plots/")
    print("=" * 60)


if __name__ == "__main__":
    CLEAN_PATH = "../data/superstore_clean.csv"
    run_eda_pipeline(CLEAN_PATH)
