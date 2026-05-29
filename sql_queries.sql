-- ============================================================
--  E-Commerce Sales & Customer Analytics Dashboard
--  SQL Analysis Queries
--  Database : ecommerce_db
--  Table    : superstore_sales
--  Author   : Data Analyst Intern
-- ============================================================

-- ─────────────────────────────────────────────────────────────
-- TABLE SCHEMA (for reference)
-- ─────────────────────────────────────────────────────────────
/*
CREATE TABLE superstore_sales (
    row_id         INT           PRIMARY KEY,
    order_id       VARCHAR(20)   NOT NULL,
    order_date     DATE          NOT NULL,
    ship_date      DATE,
    ship_mode      VARCHAR(30),
    customer_id    VARCHAR(20),
    customer_name  VARCHAR(100),
    segment        VARCHAR(30),
    country        VARCHAR(50),
    city           VARCHAR(50),
    state          VARCHAR(50),
    region         VARCHAR(20),
    product_id     VARCHAR(25),
    category       VARCHAR(30),
    sub_category   VARCHAR(30),
    product_name   VARCHAR(200),
    sales          DECIMAL(10,2),
    quantity       INT,
    discount       DECIMAL(4,2),
    profit         DECIMAL(10,2)
);
*/


-- ════════════════════════════════════════════════════════════
-- 1. DATABASE OVERVIEW & HEALTH CHECK
-- ════════════════════════════════════════════════════════════

-- Total records
SELECT COUNT(*)            AS total_rows,
       COUNT(DISTINCT order_id)     AS unique_orders,
       COUNT(DISTINCT customer_id)  AS unique_customers,
       COUNT(DISTINCT product_id)   AS unique_products,
       MIN(order_date)              AS earliest_order,
       MAX(order_date)              AS latest_order
FROM   superstore_sales;

-- Check for NULLs
SELECT
    SUM(CASE WHEN order_id      IS NULL THEN 1 ELSE 0 END) AS null_order_id,
    SUM(CASE WHEN order_date    IS NULL THEN 1 ELSE 0 END) AS null_order_date,
    SUM(CASE WHEN customer_name IS NULL THEN 1 ELSE 0 END) AS null_customer,
    SUM(CASE WHEN sales         IS NULL THEN 1 ELSE 0 END) AS null_sales,
    SUM(CASE WHEN profit        IS NULL THEN 1 ELSE 0 END) AS null_profit
FROM   superstore_sales;


-- ════════════════════════════════════════════════════════════
-- 2. KPI METRICS
-- ════════════════════════════════════════════════════════════

SELECT
    ROUND(SUM(sales),  2)                                   AS total_revenue,
    ROUND(SUM(profit), 2)                                   AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2)    AS profit_margin_pct,
    COUNT(DISTINCT order_id)                                AS total_orders,
    COUNT(DISTINCT customer_id)                             AS total_customers,
    ROUND(SUM(sales) / NULLIF(COUNT(DISTINCT order_id), 0), 2)
                                                            AS avg_order_value,
    ROUND(AVG(DATEDIFF(ship_date, order_date)), 1)          AS avg_shipping_days
FROM   superstore_sales;


-- ════════════════════════════════════════════════════════════
-- 3. TOP 10 CUSTOMERS BY REVENUE
-- ════════════════════════════════════════════════════════════

SELECT
    customer_name,
    segment,
    region,
    COUNT(DISTINCT order_id)               AS total_orders,
    ROUND(SUM(sales),  2)                  AS total_revenue,
    ROUND(SUM(profit), 2)                  AS total_profit,
    ROUND(SUM(profit)/NULLIF(SUM(sales),0)*100, 2) AS profit_margin_pct,
    ROUND(SUM(sales)/NULLIF(COUNT(DISTINCT order_id),0), 2) AS avg_order_value
FROM   superstore_sales
GROUP  BY customer_name, segment, region
ORDER  BY total_revenue DESC
LIMIT  10;


-- ════════════════════════════════════════════════════════════
-- 4. HIGHEST PROFIT CATEGORIES & SUB-CATEGORIES
-- ════════════════════════════════════════════════════════════

-- Category level
SELECT
    category,
    ROUND(SUM(sales),  2)                          AS total_sales,
    ROUND(SUM(profit), 2)                          AS total_profit,
    ROUND(SUM(profit)/NULLIF(SUM(sales),0)*100, 2) AS profit_margin_pct,
    SUM(quantity)                                  AS units_sold,
    COUNT(DISTINCT order_id)                       AS order_count
FROM   superstore_sales
GROUP  BY category
ORDER  BY total_profit DESC;

-- Sub-category level
SELECT
    category,
    sub_category,
    ROUND(SUM(sales),  2)                          AS total_sales,
    ROUND(SUM(profit), 2)                          AS total_profit,
    ROUND(SUM(profit)/NULLIF(SUM(sales),0)*100, 2) AS profit_margin_pct,
    ROUND(AVG(discount)*100, 1)                    AS avg_discount_pct,
    SUM(quantity)                                  AS units_sold
FROM   superstore_sales
GROUP  BY category, sub_category
ORDER  BY total_profit DESC;


-- ════════════════════════════════════════════════════════════
-- 5. MONTHLY REVENUE TREND
-- ════════════════════════════════════════════════════════════

SELECT
    YEAR(order_date)                            AS order_year,
    MONTH(order_date)                           AS order_month,
    DATE_FORMAT(order_date, '%b %Y')            AS month_label,
    COUNT(DISTINCT order_id)                    AS orders,
    ROUND(SUM(sales),  2)                       AS monthly_revenue,
    ROUND(SUM(profit), 2)                       AS monthly_profit,
    ROUND(SUM(profit)/NULLIF(SUM(sales),0)*100, 2) AS profit_margin_pct,
    ROUND(
        (SUM(sales) - LAG(SUM(sales)) OVER (ORDER BY YEAR(order_date), MONTH(order_date)))
        / NULLIF(LAG(SUM(sales)) OVER (ORDER BY YEAR(order_date), MONTH(order_date)), 0) * 100
    , 2) AS mom_growth_pct          -- Month-over-Month growth
FROM   superstore_sales
GROUP  BY order_year, order_month
ORDER  BY order_year, order_month;


-- ════════════════════════════════════════════════════════════
-- 6. QUARTERLY REVENUE WITH RUNNING TOTAL
-- ════════════════════════════════════════════════════════════

WITH quarterly AS (
    SELECT
        YEAR(order_date)      AS yr,
        QUARTER(order_date)   AS qtr,
        ROUND(SUM(sales),  2) AS quarterly_revenue,
        ROUND(SUM(profit), 2) AS quarterly_profit
    FROM   superstore_sales
    GROUP  BY yr, qtr
)
SELECT
    yr,
    qtr,
    quarterly_revenue,
    quarterly_profit,
    SUM(quarterly_revenue) OVER (
        PARTITION BY yr ORDER BY qtr
    ) AS cumulative_revenue_ytd,
    ROUND(
        (quarterly_revenue - LAG(quarterly_revenue) OVER (ORDER BY yr, qtr))
        / NULLIF(LAG(quarterly_revenue) OVER (ORDER BY yr, qtr), 0) * 100
    , 2) AS qoq_growth_pct
FROM   quarterly
ORDER  BY yr, qtr;


-- ════════════════════════════════════════════════════════════
-- 7. AVERAGE ORDER VALUE (AOV) BY SEGMENT & REGION
-- ════════════════════════════════════════════════════════════

SELECT
    segment,
    region,
    COUNT(DISTINCT order_id)                          AS total_orders,
    ROUND(SUM(sales),  2)                             AS total_revenue,
    ROUND(SUM(sales)/NULLIF(COUNT(DISTINCT order_id),0), 2) AS avg_order_value,
    ROUND(SUM(profit)/NULLIF(COUNT(DISTINCT order_id),0), 2) AS avg_profit_per_order
FROM   superstore_sales
GROUP  BY segment, region
ORDER  BY avg_order_value DESC;


-- ════════════════════════════════════════════════════════════
-- 8. CUSTOMER PURCHASE FREQUENCY & RETENTION
-- ════════════════════════════════════════════════════════════

-- Purchase frequency per customer
SELECT
    customer_name,
    segment,
    region,
    COUNT(DISTINCT order_id)           AS order_count,
    MIN(order_date)                    AS first_order,
    MAX(order_date)                    AS last_order,
    DATEDIFF(MAX(order_date), MIN(order_date)) AS customer_lifetime_days,
    ROUND(SUM(sales),  2)              AS lifetime_value,
    ROUND(AVG(sales),  2)              AS avg_order_value,
    CASE
        WHEN COUNT(DISTINCT order_id) >= 5 THEN 'High Frequency'
        WHEN COUNT(DISTINCT order_id) >= 2 THEN 'Medium Frequency'
        ELSE 'Single Purchase'
    END                                AS purchase_frequency_segment
FROM   superstore_sales
GROUP  BY customer_name, segment, region
ORDER  BY order_count DESC
LIMIT  20;

-- Frequency distribution
SELECT
    purchase_band,
    COUNT(*) AS customers,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct_of_customers
FROM (
    SELECT
        customer_id,
        CASE
            WHEN COUNT(DISTINCT order_id) = 1       THEN '1 Order'
            WHEN COUNT(DISTINCT order_id) BETWEEN 2 AND 4 THEN '2–4 Orders'
            WHEN COUNT(DISTINCT order_id) BETWEEN 5 AND 9 THEN '5–9 Orders'
            ELSE '10+ Orders'
        END AS purchase_band
    FROM   superstore_sales
    GROUP  BY customer_id
) t
GROUP  BY purchase_band
ORDER  BY customers DESC;


-- ════════════════════════════════════════════════════════════
-- 9. REGION-WISE SALES & MARKET SHARE
-- ════════════════════════════════════════════════════════════

SELECT
    region,
    COUNT(DISTINCT order_id)                          AS orders,
    COUNT(DISTINCT customer_id)                       AS customers,
    ROUND(SUM(sales),  2)                             AS total_revenue,
    ROUND(SUM(profit), 2)                             AS total_profit,
    ROUND(SUM(profit)/NULLIF(SUM(sales),0)*100, 2)    AS profit_margin_pct,
    ROUND(SUM(sales)*100.0/SUM(SUM(sales)) OVER (), 2) AS revenue_market_share_pct,
    ROUND(SUM(sales)/NULLIF(COUNT(DISTINCT order_id),0), 2) AS avg_order_value
FROM   superstore_sales
GROUP  BY region
ORDER  BY total_revenue DESC;


-- ════════════════════════════════════════════════════════════
-- 10. TOP 10 PROFITABLE PRODUCTS
-- ════════════════════════════════════════════════════════════

SELECT
    product_name,
    category,
    sub_category,
    SUM(quantity)                              AS units_sold,
    ROUND(SUM(sales),  2)                      AS total_sales,
    ROUND(SUM(profit), 2)                      AS total_profit,
    ROUND(SUM(profit)/NULLIF(SUM(sales),0)*100, 2) AS profit_margin_pct,
    ROUND(AVG(discount)*100, 1)               AS avg_discount_pct
FROM   superstore_sales
GROUP  BY product_name, category, sub_category
ORDER  BY total_profit DESC
LIMIT  10;


-- ════════════════════════════════════════════════════════════
-- 11. LOSS-MAKING PRODUCTS (BOTTOM 10 BY PROFIT)
-- ════════════════════════════════════════════════════════════

SELECT
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales),  2)  AS total_sales,
    ROUND(SUM(profit), 2)  AS total_profit,
    ROUND(AVG(discount)*100, 1) AS avg_discount_pct,
    SUM(quantity)          AS units_sold
FROM   superstore_sales
GROUP  BY product_name, category, sub_category
HAVING total_profit < 0
ORDER  BY total_profit ASC
LIMIT  10;


-- ════════════════════════════════════════════════════════════
-- 12. SHIPPING MODE PERFORMANCE
-- ════════════════════════════════════════════════════════════

SELECT
    ship_mode,
    COUNT(DISTINCT order_id)                          AS total_orders,
    ROUND(SUM(sales),  2)                             AS total_revenue,
    ROUND(SUM(profit), 2)                             AS total_profit,
    ROUND(AVG(DATEDIFF(ship_date, order_date)), 1)    AS avg_shipping_days,
    ROUND(SUM(sales)*100.0/SUM(SUM(sales)) OVER (), 2) AS revenue_share_pct
FROM   superstore_sales
GROUP  BY ship_mode
ORDER  BY total_orders DESC;


-- ════════════════════════════════════════════════════════════
-- 13. DISCOUNT IMPACT ANALYSIS
-- ════════════════════════════════════════════════════════════

SELECT
    discount_band,
    COUNT(*)                           AS order_lines,
    ROUND(AVG(sales),  2)              AS avg_sales,
    ROUND(AVG(profit), 2)              AS avg_profit,
    ROUND(SUM(profit)/NULLIF(SUM(sales),0)*100, 2) AS profit_margin_pct,
    ROUND(SUM(sales),  2)              AS total_sales
FROM (
    SELECT *,
        CASE
            WHEN discount = 0           THEN 'No Discount'
            WHEN discount <= 0.10       THEN '1–10%'
            WHEN discount <= 0.20       THEN '11–20%'
            WHEN discount <= 0.30       THEN '21–30%'
            ELSE '31%+'
        END AS discount_band
    FROM superstore_sales
) t
GROUP  BY discount_band
ORDER  BY avg_profit DESC;


-- ════════════════════════════════════════════════════════════
-- 14. CUSTOMER LIFETIME VALUE (CLV) — TOP 10
-- ════════════════════════════════════════════════════════════

WITH customer_orders AS (
    SELECT
        customer_id,
        customer_name,
        segment,
        COUNT(DISTINCT order_id)        AS order_count,
        ROUND(SUM(sales), 2)            AS total_revenue,
        ROUND(AVG(sales), 2)            AS avg_order_value,
        DATEDIFF(MAX(order_date), MIN(order_date)) AS customer_lifetime_days
    FROM   superstore_sales
    GROUP  BY customer_id, customer_name, segment
)
SELECT
    customer_name,
    segment,
    order_count,
    total_revenue,
    avg_order_value,
    customer_lifetime_days,
    -- Simplified CLV: AOV × Purchase Frequency × Lifespan (years)
    ROUND(
        avg_order_value
        * (order_count / GREATEST(customer_lifetime_days / 365.0, 1))
        * 3   -- assumed 3-year horizon
    , 2) AS estimated_clv_3yr
FROM   customer_orders
ORDER  BY total_revenue DESC
LIMIT  10;


-- ════════════════════════════════════════════════════════════
-- 15. STATE-LEVEL PERFORMANCE (TOP 10 STATES)
-- ════════════════════════════════════════════════════════════

SELECT
    state,
    region,
    COUNT(DISTINCT order_id)                   AS total_orders,
    COUNT(DISTINCT customer_id)                AS unique_customers,
    ROUND(SUM(sales),  2)                      AS total_revenue,
    ROUND(SUM(profit), 2)                      AS total_profit,
    ROUND(SUM(profit)/NULLIF(SUM(sales),0)*100,2) AS profit_margin_pct
FROM   superstore_sales
GROUP  BY state, region
ORDER  BY total_revenue DESC
LIMIT  10;


-- ════════════════════════════════════════════════════════════
-- 16. REPEAT vs NEW CUSTOMER REVENUE SPLIT
-- ════════════════════════════════════════════════════════════

WITH customer_type AS (
    SELECT
        customer_id,
        CASE WHEN COUNT(DISTINCT order_id) > 1 THEN 'Repeat' ELSE 'New' END AS ctype
    FROM   superstore_sales
    GROUP  BY customer_id
)
SELECT
    ct.ctype           AS customer_type,
    COUNT(DISTINCT s.customer_id)  AS customers,
    COUNT(DISTINCT s.order_id)     AS orders,
    ROUND(SUM(s.sales),  2)        AS total_revenue,
    ROUND(SUM(s.profit), 2)        AS total_profit,
    ROUND(SUM(s.sales)*100.0/SUM(SUM(s.sales)) OVER (), 2) AS revenue_share_pct
FROM   superstore_sales s
JOIN   customer_type ct USING (customer_id)
GROUP  BY ct.ctype;


-- ════════════════════════════════════════════════════════════
-- 17. YEAR-OVER-YEAR GROWTH SUMMARY
-- ════════════════════════════════════════════════════════════

WITH yearly AS (
    SELECT
        YEAR(order_date)      AS yr,
        ROUND(SUM(sales),  2) AS total_revenue,
        ROUND(SUM(profit), 2) AS total_profit,
        COUNT(DISTINCT order_id)     AS total_orders,
        COUNT(DISTINCT customer_id)  AS total_customers
    FROM   superstore_sales
    GROUP  BY yr
)
SELECT
    yr,
    total_revenue,
    total_profit,
    total_orders,
    total_customers,
    ROUND(
        (total_revenue - LAG(total_revenue) OVER (ORDER BY yr))
        / NULLIF(LAG(total_revenue) OVER (ORDER BY yr), 0) * 100
    , 2) AS yoy_revenue_growth_pct,
    ROUND(
        (total_profit - LAG(total_profit) OVER (ORDER BY yr))
        / NULLIF(LAG(total_profit) OVER (ORDER BY yr), 0) * 100
    , 2) AS yoy_profit_growth_pct
FROM   yearly
ORDER  BY yr;
