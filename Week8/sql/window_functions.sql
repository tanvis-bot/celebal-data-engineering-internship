.headers on
.mode box

-- Q7: Running total of revenue per region

WITH daily_region_revenue AS (
    SELECT
        o.region_code,
        DATE(o.order_date) AS order_date,

        ROUND(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount_percent / 100.0)
            ),
            2
        ) AS daily_revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    GROUP BY
        o.region_code,
        DATE(o.order_date)
)

SELECT
    region_code,
    order_date,
    daily_revenue,

    ROUND(
        SUM(daily_revenue) OVER (
            PARTITION BY region_code
            ORDER BY order_date
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ),
        2
    ) AS running_total

FROM daily_region_revenue

ORDER BY
    region_code,
    order_date;

-- Q8: Rank products by revenue within category

WITH product_revenue AS (
    SELECT
        p.category,
        p.product_id,
        p.product_name,

        ROUND(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount_percent / 100.0)
            ),
            2
        ) AS total_revenue

    FROM products p

    JOIN order_items oi
        ON p.product_id = oi.product_id

    GROUP BY
        p.category,
        p.product_id,
        p.product_name
)

SELECT
    category,
    product_name,
    total_revenue,

    DENSE_RANK() OVER (
        PARTITION BY category
        ORDER BY total_revenue DESC
    ) AS rank_in_category

FROM product_revenue

ORDER BY
    category,
    rank_in_category;


-- Q9: Days between consecutive customer orders

WITH order_gaps AS (
    SELECT
        customer_id,
        DATE(order_date) AS order_date,

        LAG(
            DATE(order_date)
        ) OVER (
            PARTITION BY customer_id
            ORDER BY DATE(order_date)
        ) AS previous_order_date

    FROM orders
),

gap_values AS (
    SELECT
        customer_id,
        order_date,
        previous_order_date,

        CAST(
            JULIANDAY(order_date)
            - JULIANDAY(previous_order_date)
            AS INTEGER
        ) AS days_gap

    FROM order_gaps
),

customer_gap_summary AS (
    SELECT
        customer_id,

        ROUND(
            AVG(days_gap),
            2
        ) AS avg_days_gap

    FROM gap_values

    WHERE previous_order_date IS NOT NULL

    GROUP BY customer_id
)

SELECT
    g.customer_id,
    g.order_date,
    g.previous_order_date,
    g.days_gap,
    s.avg_days_gap,

    CASE
        WHEN s.avg_days_gap > 30
        THEN 'At Risk'
        ELSE 'Active'
    END AS customer_status

FROM gap_values g

LEFT JOIN customer_gap_summary s
    ON g.customer_id = s.customer_id

ORDER BY
    g.customer_id,
    g.order_date;

-- Q10: Multi-level CTE customer segmentation by monthly revenue

WITH customer_monthly_revenue AS (
    SELECT
        o.customer_id,
        strftime('%Y-%m', o.order_date) AS month,

        ROUND(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount_percent / 100.0)
            ),
            2
        ) AS monthly_revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    GROUP BY
        o.customer_id,
        strftime('%Y-%m', o.order_date)
),

customer_categories AS (
    SELECT
        customer_id,
        month,
        monthly_revenue,

        CASE
            WHEN monthly_revenue > 10000
            THEN 'High'

            WHEN monthly_revenue >= 5000
                 AND monthly_revenue <= 10000
            THEN 'Medium'

            ELSE 'Low'
        END AS spend_category

    FROM customer_monthly_revenue
)

SELECT
    month,
    spend_category,
    COUNT(DISTINCT customer_id) AS customer_count

FROM customer_categories

GROUP BY
    month,
    spend_category

ORDER BY
    month,
    spend_category;

-- Q11: Divide customers into 4 quartiles by lifetime value

WITH customer_lifetime_value AS (
    SELECT
        c.customer_id,

        ROUND(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount_percent / 100.0)
            ),
            2
        ) AS total_value

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    GROUP BY
        c.customer_id
),

customer_quartiles AS (
    SELECT
        customer_id,
        total_value,

        NTILE(4) OVER (
            ORDER BY total_value DESC
        ) AS quartile

    FROM customer_lifetime_value
)

SELECT
    customer_id,
    total_value,
    quartile,

    CASE quartile
        WHEN 1 THEN 'Platinum'
        WHEN 2 THEN 'Gold'
        WHEN 3 THEN 'Silver'
        WHEN 4 THEN 'Bronze'
    END AS quartile_label

FROM customer_quartiles

ORDER BY
    quartile,
    total_value DESC;


-- Q12: Compare each month's revenue with the same month previous year

WITH monthly_revenue AS (
    SELECT
        CAST(
            strftime('%Y', o.order_date)
            AS INTEGER
        ) AS year,

        CAST(
            strftime('%m', o.order_date)
            AS INTEGER
        ) AS month,

        ROUND(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount_percent / 100.0)
            ),
            2
        ) AS revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    GROUP BY
        strftime('%Y', o.order_date),
        strftime('%m', o.order_date)
),

yoy_data AS (
    SELECT
        current.year,
        current.month,
        current.revenue,

        previous.revenue
            AS prev_year_revenue

    FROM monthly_revenue current

    LEFT JOIN monthly_revenue previous
        ON previous.year = current.year - 1
        AND previous.month = current.month
)

SELECT
    year,
    month,
    revenue,
    prev_year_revenue,

    CASE
        WHEN prev_year_revenue IS NULL
             OR prev_year_revenue = 0
        THEN NULL

        ELSE ROUND(
            (
                revenue - prev_year_revenue
            )
            * 100.0
            / prev_year_revenue,
            2
        )
    END AS yoy_growth_percent

FROM yoy_data

ORDER BY
    year,
    month;

-- Q13: First and most recent purchased category per customer

WITH customer_purchases AS (
    SELECT
        o.customer_id,
        o.order_date,
        p.category,

        ROW_NUMBER() OVER (
            PARTITION BY o.customer_id
            ORDER BY o.order_date ASC
        ) AS first_rank,

        ROW_NUMBER() OVER (
            PARTITION BY o.customer_id
            ORDER BY o.order_date DESC
        ) AS recent_rank

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    WHERE oi.quantity > 0
),

first_category AS (
    SELECT
        customer_id,
        category AS first_category
    FROM customer_purchases
    WHERE first_rank = 1
),

recent_category AS (
    SELECT
        customer_id,
        category AS recent_category
    FROM customer_purchases
    WHERE recent_rank = 1
)

SELECT
    f.customer_id,
    f.first_category,
    r.recent_category,

    CASE
        WHEN f.first_category <> r.recent_category
        THEN 'Yes'
        ELSE 'No'
    END AS category_shift

FROM first_category f

JOIN recent_category r
    ON f.customer_id = r.customer_id

ORDER BY
    f.customer_id;



-- Q14: Cumulative revenue distribution by customer

WITH customer_revenue AS (
    SELECT
        c.customer_id,

        ROUND(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount_percent / 100.0)
            ),
            2
        ) AS revenue

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    GROUP BY
        c.customer_id
),

ranked_customers AS (
    SELECT
        customer_id,
        revenue,

        SUM(revenue) OVER (
            ORDER BY revenue DESC
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ) AS cumulative_revenue,

        SUM(revenue) OVER () AS total_revenue

    FROM customer_revenue
)

SELECT
    customer_id,
    revenue,

    ROUND(
        cumulative_revenue,
        2
    ) AS cumulative_revenue,

    ROUND(
        cumulative_revenue
        * 100.0
        / total_revenue,
        2
    ) AS cumulative_percent

FROM ranked_customers

ORDER BY
    revenue DESC;

-- Q15: Cohort retention analysis

WITH customer_orders AS (
    SELECT
        c.customer_id,

        strftime(
            '%Y-%m',
            c.registration_date
        ) AS cohort_month,

        strftime(
            '%Y-%m',
            o.order_date
        ) AS order_month,

        (
            (
                CAST(
                    strftime('%Y', o.order_date)
                    AS INTEGER
                )
                -
                CAST(
                    strftime('%Y', c.registration_date)
                    AS INTEGER
                )
            ) * 12

            +

            (
                CAST(
                    strftime('%m', o.order_date)
                    AS INTEGER
                )
                -
                CAST(
                    strftime('%m', c.registration_date)
                    AS INTEGER
                )
            )
        ) AS month_number

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id
),

cohort_activity AS (
    SELECT
        cohort_month,
        month_number,

        COUNT(
            DISTINCT customer_id
        ) AS active_customers

    FROM customer_orders

    WHERE month_number BETWEEN 0 AND 3

    GROUP BY
        cohort_month,
        month_number
),

cohort_pivot AS (
    SELECT
        cohort_month,

        MAX(
            CASE
                WHEN month_number = 0
                THEN active_customers
                ELSE 0
            END
        ) AS month_0,

        MAX(
            CASE
                WHEN month_number = 1
                THEN active_customers
                ELSE 0
            END
        ) AS month_1,

        MAX(
            CASE
                WHEN month_number = 2
                THEN active_customers
                ELSE 0
            END
        ) AS month_2,

        MAX(
            CASE
                WHEN month_number = 3
                THEN active_customers
                ELSE 0
            END
        ) AS month_3

    FROM cohort_activity

    GROUP BY
        cohort_month
)

SELECT
    cohort_month,

    month_0,
    month_1,
    month_2,
    month_3,

    CASE
        WHEN month_0 = 0
        THEN 0
        ELSE ROUND(
            month_1 * 100.0 / month_0,
            2
        )
    END AS retention_month_1,

    CASE
        WHEN month_0 = 0
        THEN 0
        ELSE ROUND(
            month_2 * 100.0 / month_0,
            2
        )
    END AS retention_month_2,

    CASE
        WHEN month_0 = 0
        THEN 0
        ELSE ROUND(
            month_3 * 100.0 / month_0,
            2
        )
    END AS retention_month_3

FROM cohort_pivot

ORDER BY
    cohort_month;

-- Q16: Products frequently bought together

WITH product_pairs AS (
    SELECT
        oi1.order_id,

        oi1.product_id AS product_a_id,
        oi2.product_id AS product_b_id

    FROM order_items oi1

    JOIN order_items oi2
        ON oi1.order_id = oi2.order_id

        AND oi1.product_id < oi2.product_id

    WHERE
        oi1.quantity > 0
        AND oi2.quantity > 0
)

SELECT
    p1.product_name AS product_a,
    p2.product_name AS product_b,

    COUNT(
        DISTINCT pp.order_id
    ) AS times_bought_together

FROM product_pairs pp

JOIN products p1
    ON pp.product_a_id = p1.product_id

JOIN products p2
    ON pp.product_b_id = p2.product_id

GROUP BY
    pp.product_a_id,
    pp.product_b_id,
    p1.product_name,
    p2.product_name

ORDER BY
    times_bought_together DESC,
    product_a,
    product_b

LIMIT 20;

