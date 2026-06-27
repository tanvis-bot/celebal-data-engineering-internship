-- SECTION A : SQL Basics

--Q1. Write a query to display all columns and rows from the customer's table. 
SELECT * FROM customers;

--Q2. Retrieve only the first_name, last_name, and city of all customers. 
SELECT first_name, last_name, city FROM customers;

--Q3. List all unique categories available in the products table. 
SELECT DISTINCT category FROM products;

--Q4. Identify the Primary Key of each table in the schema. Explain why a Primary Key must be unique and NOT NULL. 
--Answer: In the schema, the Primary Key is defined in the CREATE TABLE statement for each table.
-- Primary Keys for 4 tables is customer_id, product_id, order_id, and item_id.
-- A Primary Key must be unique and NOT NULL because it serves as a unique identifier for each record. 
-- It ensures that each row can be uniquely identified, which is essential for maintaining data integrity and establishing relationships between tables in a relational database.


--Q5. What constraints are applied to the email column in the customers table? What would happen if you tried to insert a duplicate email? 
--INSERT INTO customers VALUES (109, 'Rahul', 'Verma', 'aarav.s@email.com', 'Nagpur', 'Maharashtra', '2024-09-01', TRUE);


--Q6. Try inserting a product with unit_price = -50. What happens and which constraint prevents it? Write both the INSERT statement and explain the error. 
--INSERT INTO products VALUES (209, 'USB Cable', 'Electronics', 'Boat', -50, 100);


-- SECTION B : Filtering & Optimization
-- Q7. Retrieve all orders with status = 'Delivered'.
SELECT * FROM orders WHERE status = 'Delivered';

-- Q8. Find all products in the 'Electronics' category with a unit_price greater than ₹2000.
SELECT * FROM products WHERE category = 'Electronics' AND unit_price > 2000;

-- Q9. List all customers who joined in the year 2024 and belong to the state 'Maharashtra'.
SELECT * FROM customers WHERE join_date BETWEEN '2024-01-01' AND '2024-12-31' AND state = 'Maharashtra';

-- Q10. Find all orders placed between '2024-08-10' and '2024-08-25' (inclusive) that are NOT cancelled.
SELECT * FROM orders WHERE order_date BETWEEN '2024-08-10' AND '2024-08-25' AND status <> 'Cancelled';

-- Q11. Explain what the index idx_orders_date does. How would it improve the performance of a query that filters orders by order_date? Write a sample query that would benefit from this index.
-- Answer: The idx_orders_date index speeds up filtering and searching on the order_date column by reducing full table scans.
SELECT * FROM orders WHERE order_date = '2024-08-15';

-- Q12. If you run SELECT * FROM customers WHERE YEAR(join_date)=2024; would the index on join_date be used? Explain why or why not, and rewrite the query to be index-friendly (SARGable).
-- Answer: No because applying a function like YEAR() on an indexed column prevents efficient index usage. Use a date range instead.
SELECT * FROM customers WHERE join_date BETWEEN '2024-01-01' AND '2024-12-31';





--SECTION C: Aggregation (GROUP BY, SUM, COUNT, AVG, MIN, MAX) 
-- Q13. Count the total number of orders in the orders table.
SELECT COUNT(*) AS total_orders FROM orders;

-- Q14. Find the total revenue (SUM of total_amount) from all 'Delivered' orders.
SELECT SUM(total_amount) AS total_revenue FROM orders WHERE status = 'Delivered';

-- Q15. Calculate the average unit_price of products in each category.
SELECT category, AVG(unit_price) AS average_price FROM products GROUP BY category;

-- Q16. For each order status, find the count of orders and the total revenue. Sort the result by total revenue in descending order.
SELECT status, COUNT(*) AS order_count, SUM(total_amount) AS total_revenue FROM orders GROUP BY status ORDER BY total_revenue DESC;

-- Q17. Find the most expensive (MAX) and cheapest (MIN) product in each category.
SELECT category, MAX(unit_price) AS highest_price, MIN(unit_price) AS lowest_price FROM products GROUP BY category;

-- Q18. List all product categories where the average unit_price is greater than ₹2000. (Hint: Use HAVING clause)
SELECT category, AVG(unit_price) AS average_price FROM products GROUP BY category HAVING AVG(unit_price) > 2000;


--SECTION D — Joins & Relationships 
-- Q19. Write an INNER JOIN query to display each order along with the customer's first_name and last_name. Show: order_id, order_date, first_name, last_name, total_amount.
SELECT o.order_id, o.order_date, c.first_name, c.last_name, o.total_amount FROM orders o INNER JOIN customers c ON o.customer_id = c.customer_id;

-- Q20. Using a LEFT JOIN, list ALL customers and their orders (if any). Customers with no orders should still appear with NULL values for order columns.
SELECT c.customer_id, c.first_name, c.last_name, o.order_id, o.order_date, o.status, o.total_amount FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id;

-- Q21. Write a query using JOINs across three tables (orders → order_items → products) to show: order_id, product_name, quantity, unit_price, and discount_pct for each order item.
SELECT o.order_id, p.product_name, oi.quantity, oi.unit_price, oi.discount_pct FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id;

-- Q22. Explain the difference between LEFT JOIN and RIGHT JOIN with an example from this schema. When would you use a FULL OUTER JOIN?
-- Answer: LEFT JOIN returns all rows from the left table and matching rows from the right table. RIGHT JOIN returns all rows from the right table and matching rows from the left table (SQLite does not support RIGHT JOIN directly). FULL OUTER JOIN returns all rows from both tables, including unmatched rows from either side.

-- Q23. Identify all Foreign Key relationships in the schema. Explain what would happen if you tried to insert an order with customer_id = 999 (which doesn't exist in customers).
-- Answer: Foreign Keys are orders.customer_id → customers.customer_id, order_items.order_id → orders.order_id, and order_items.product_id → products.product_id. Inserting an order with customer_id = 999 would violate the foreign key constraint and the insertion would fail.


--SECTION E — Advanced Concepts (CASE, ACID, Transactions) 
-- Q24. Write a query using CASE to classify products into price tiers: Budget (<1000), Mid-Range (1000–3000), Premium (>3000).
SELECT product_name, unit_price, CASE WHEN unit_price < 1000 THEN 'Budget' WHEN unit_price BETWEEN 1000 AND 3000 THEN 'Mid-Range' ELSE 'Premium' END AS price_tier FROM products;

-- Q25. Using a CASE statement inside an aggregate function, count how many orders are 'Delivered' vs 'Not Delivered' (all other statuses). Display the result in a single row.
SELECT SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_orders, SUM(CASE WHEN status <> 'Delivered' THEN 1 ELSE 0 END) AS not_delivered_orders FROM orders;

-- Q26. Explain each letter of ACID. Give a real-world example (e.g., bank transfer) showing why each property is important.
-- Answer:
-- A (Atomicity): Either all operations in a transaction succeed or none do.
-- C (Consistency): A transaction keeps the database in a valid state before and after execution.
-- I (Isolation): Concurrent transactions do not interfere with each other.
-- D (Durability): Once committed, changes are permanently saved even if the system crashes.
-- Example: In a bank transfer, money is deducted from one account and added to another. If any step fails, the transaction is rolled back, ensuring data remains accurate.

-- Q27. Write a SQL transaction to insert a new order, insert two order items, update stock quantities, and COMMIT or ROLLBACK atomically.
BEGIN TRANSACTION;
INSERT INTO orders VALUES (1011, 102, DATE('now'), 'Pending', 1598.00);
INSERT INTO order_items VALUES (5016, 1011, 206, 1, 1299.00, 0);
INSERT INTO order_items VALUES (5017, 1011, 208, 1, 299.00, 0);
UPDATE products SET stock_qty = stock_qty - 1 WHERE product_id = 206;
UPDATE products SET stock_qty = stock_qty - 1 WHERE product_id = 208;
COMMIT;
-- If any statement fails before COMMIT, execute: ROLLBACK;


