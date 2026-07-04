-- Find all orders where sales are greater than the average sales. (Subquery)  
-- Finds all orders where the sales amount is greater than the average sales of all orders.
SELECT * FROM orders
WHERE sales > (SELECT AVG(sales) FROM orders)
LIMIT 10;

-- Find the highest sales order for each customer. (Subquery)  
-- Retrieves the highest sales order for every customer using a subquery.
SELECT *
FROM orders o
WHERE sales = (
    SELECT MAX(sales)
    FROM orders
    WHERE customer_id = o.customer_id
)
LIMIT 10;

-- Calculate total sales for each customer. (CTE)  
-- Calculates the total sales made by each customer using a Common Table Expression (CTE).
WITH customer_sales AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT * FROM customer_sales
LIMIT 10;

-- Find customers whose total sales are above average. (CTE + Subquery)  
-- Displays customers whose total sales are higher than the average customer sales.
WITH customer_sales AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT *
FROM customer_sales
WHERE total_sales > (
    SELECT AVG(total_sales)
    FROM customer_sales
)
LIMIT 10;

-- Rank all customers based on total sales. (Window Function)  
-- Ranks customers based on their total sales using the RANK() window function.
WITH customer_sales AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT customer_id,
       total_sales,
       RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
FROM customer_sales
LIMIT 10;

-- Assign row numbers to each order within a customer. (Window Function + PARTITION BY)  
-- Assigns a row number to each order within every customer using PARTITION BY.
SELECT order_id,
       customer_id,
       sales,
       ROW_NUMBER() OVER (
           PARTITION BY customer_id
           ORDER BY sales DESC
       ) AS row_num
FROM orders
LIMIT 10;

-- Display top 3 customers based on total sales. (Window Function)  
-- Displays the top 3 customers with the highest total sales.
WITH customer_sales AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT *
FROM (
    SELECT customer_id,
           total_sales,
           RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
    FROM customer_sales
)
WHERE sales_rank <= 3;

-- Write one final query that shows: Customer Name  ,Total Sales  ,Rank  (Use JOIN + CTE + Window Function together) 
-- Combines JOIN, CTE, and a window function to show customer name, total sales, and sales rank.
WITH customer_sales AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT c.customer_name,
       cs.total_sales,
       RANK() OVER (ORDER BY cs.total_sales DESC) AS sales_rank
FROM customer_sales cs
JOIN customers c
ON cs.customer_id = c.customer_id
LIMIT 10;

-- Who are the top 5 customers?  
-- Retrieves the top 5 customers based on total sales.
WITH customer_sales AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT c.customer_name,
       total_sales
FROM customer_sales cs
JOIN customers c
ON cs.customer_id = c.customer_id
ORDER BY total_sales DESC
LIMIT 5;

-- Who are the bottom 5 customers?  
-- Retrieves the bottom 5 customers based on total sales.
WITH customer_sales AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT c.customer_name,
       total_sales
FROM customer_sales cs
JOIN customers c
ON cs.customer_id = c.customer_id
ORDER BY total_sales ASC
LIMIT 5;

-- Which customers made only one order?  
-- Identifies customers who have placed only one order.
SELECT c.customer_name,
       COUNT(o.order_id) AS total_orders
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY c.customer_id
HAVING COUNT(o.order_id) = 1
LIMIT 10;

-- Which customers have above-average sales?  
-- Displays customers whose total sales are above the average customer sales.
WITH customer_sales AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT c.customer_name,
       total_sales
FROM customer_sales cs
JOIN customers c
ON cs.customer_id = c.customer_id
WHERE total_sales > (
    SELECT AVG(total_sales)
    FROM customer_sales
)
LIMIT 10;

-- What is the highest order value per customer? 
-- Finds the highest order value placed by each customer.
SELECT *
FROM orders o
WHERE sales = (
    SELECT MAX(sales)
    FROM orders
    WHERE customer_id = o.customer_id
)
LIMIT 10;