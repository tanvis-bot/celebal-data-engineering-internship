.headers on
.mode box

-- =====================================================
-- WEEK 8 - PART 3 SQL ANALYSIS
-- BASIC + INTERMEDIATE QUERIES
-- =====================================================


-- =====================================================
-- Q1. TOTAL REVENUE PER CATEGORY
--
-- Revenue =
-- quantity * unit_price *
-- (1 - discount_percent / 100)
--
-- Negative quantity represents returns, so returned
-- units automatically reduce net revenue.
-- =====================================================

SELECT
    p.category,

    ROUND(
        SUM(
            oi.quantity
            * oi.unit_price
            * (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_revenue

FROM order_items AS oi

JOIN products AS p
    ON oi.product_id = p.product_id

GROUP BY
    p.category

ORDER BY
    total_revenue DESC;



-- =====================================================
-- Q2. TOP 10 CUSTOMERS BY TOTAL ORDER VALUE
-- =====================================================

SELECT
    c.customer_id,
    c.customer_name,
    c.customer_type,

    COUNT(
        DISTINCT o.order_id
    ) AS total_orders,

    ROUND(
        SUM(
            oi.quantity
            * oi.unit_price
            * (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_order_value

FROM customers AS c

JOIN orders AS o
    ON c.customer_id = o.customer_id

JOIN order_items AS oi
    ON o.order_id = oi.order_id

GROUP BY
    c.customer_id,
    c.customer_name,
    c.customer_type

ORDER BY
    total_order_value DESC

LIMIT 10;



-- =====================================================
-- Q3. MONTH-WISE ORDER COUNT FOR LAST 12 MONTHS
-- =====================================================

SELECT
    strftime(
        '%Y-%m',
        order_date
    ) AS order_month,

    COUNT(*) AS total_orders

FROM orders

WHERE
    datetime(order_date)
    >= datetime(
        'now',
        '-12 months'
    )

GROUP BY
    strftime(
        '%Y-%m',
        order_date
    )

ORDER BY
    order_month;



-- =====================================================
-- Q4. CUSTOMERS WHO PLACED ORDERS BUT NEVER HAD
-- ANY ORDER DELIVERED
--
-- The supplied schema has order-level "status";
-- it does not contain a separate item-delivery status.
-- Therefore DELIVERED is checked using orders.status.
-- =====================================================

SELECT
    c.customer_id,
    c.customer_name,

    COUNT(
        DISTINCT o.order_id
    ) AS total_orders

FROM customers AS c

JOIN orders AS o
    ON c.customer_id = o.customer_id

GROUP BY
    c.customer_id,
    c.customer_name

HAVING
    COUNT(
        DISTINCT o.order_id
    ) > 0

    AND

    SUM(
        CASE
            WHEN o.status = 'DELIVERED'
            THEN 1
            ELSE 0
        END
    ) = 0

ORDER BY
    total_orders DESC;



-- =====================================================
-- -- Q5. Products that were ordered but had
-- more returns than purchases
-- =====================================================

WITH product_stats AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,

        SUM(
            CASE
                WHEN oi.quantity > 0
                THEN oi.quantity
                ELSE 0
            END
        ) AS purchased_units,

        SUM(
            CASE
                WHEN oi.quantity < 0
                THEN ABS(oi.quantity)
                ELSE 0
            END
        ) AS returned_units

    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id

    GROUP BY
        p.product_id,
        p.product_name,
        p.category
)

SELECT
    product_id,
    product_name,
    category,
    purchased_units,
    returned_units

FROM product_stats

WHERE returned_units > purchased_units

ORDER BY returned_units DESC;


-- =====================================================
-- Q6. RETURN RATE PER CATEGORY
--
-- Return Rate =
-- returned units / total units * 100
-- =====================================================

WITH category_stats AS (
    SELECT
        p.category,

        SUM(
            CASE
                WHEN oi.quantity > 0
                THEN oi.quantity
                ELSE 0
            END
        ) AS purchased_units,

        SUM(
            CASE
                WHEN oi.quantity < 0
                THEN ABS(oi.quantity)
                ELSE 0
            END
        ) AS returned_units

    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id

    GROUP BY p.category
)

SELECT
    category,
    purchased_units,
    returned_units,

    purchased_units + returned_units
        AS total_units,

    ROUND(
        returned_units * 100.0 /
        (purchased_units + returned_units),
        2
    ) AS return_rate_percent

FROM category_stats

ORDER BY return_rate_percent DESC;

