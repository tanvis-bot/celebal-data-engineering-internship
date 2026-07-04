# Week 3 - SQL Analysis using Subqueries, CTEs & Window Functions

## Objective

Analyze the Superstore dataset using SQL by applying Subqueries, Common Table Expressions (CTEs), Window Functions, and JOINs to solve business-related queries and generate meaningful customer sales insights.

---

## Tools Used

- SQLite
- VS Code
- SQL
- Git & GitHub

---

## Dataset

- **Dataset:** Sample Superstore Dataset
- **Source:** Kaggle Superstore Dataset
- The dataset contains customer, order, product, sales, quantity, discount, and profit information.

---

## Folder Structure

```
Week3/
│
├── data/
│   └── superstore.csv
│
├── database/
│   └── superstore.db
│
├── queries/
│   ├── create_tables.sql
│   ├── insert_data.sql
│   └── solutions.sql
│
├── screenshots/
│   └── Query output screenshots
│
└── README.md
```

---

## Steps Performed

1. Imported the Superstore dataset into SQLite.
2. Created the `superstore_raw` table from the CSV file.
3. Created normalized tables: `customers`, `orders`, and `products`.
4. Inserted unique records into each table using `SELECT DISTINCT`.
5. Solved business problems using SQL queries.
6. Applied Subqueries to compare sales and find highest-value orders.
7. Used CTEs to calculate customer-wise total sales.
8. Used Window Functions to rank customers and assign row numbers.
9. Combined JOINs, CTEs, and Window Functions for final customer ranking.
10. Validated query outputs and captured screenshots.

---

## SQL Concepts Used

### Subqueries
- Compared sales against average sales.
- Retrieved the highest sales order for each customer.

### Common Table Expressions (CTEs)
- Calculated total sales for each customer.
- Identified customers with above-average sales.

### Window Functions
- Ranked customers using `RANK()`.
- Assigned row numbers using `ROW_NUMBER()` with `PARTITION BY`.

### JOINs
- Combined customer and order information.
- Generated customer-wise sales ranking using multiple tables.

---

## Business Insights

- Identified the top-performing customers based on total sales.
- Found customers whose sales exceeded the average customer sales.
- Ranked customers according to their total revenue contribution.
- Identified customers who placed only a single order.
- Retrieved the highest-value order placed by each customer.
- Combined customer information with sales data for comprehensive analysis.

---

## Conclusion

This assignment demonstrates the use of advanced SQL concepts such as Subqueries, CTEs, Window Functions, and JOINs to analyze sales data, generate customer insights, and answer business questions using a relational database.