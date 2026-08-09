# Week 8 – E-Commerce Order Analytics System

## Project Overview

This project implements an end-to-end E-Commerce Order Analytics System using Python, Pandas, SQLite, and SQL.

The system generates realistic e-commerce datasets containing intentional data-quality issues, cleans and validates the data, loads the cleaned datasets into a relational SQLite database, performs business analytics using SQL, and provides a Python command-line reporting tool.

---

## Technologies Used

- Python
- Pandas
- SQLite
- SQL
- Faker
- VS Code

---

## Dataset

Four datasets are used in the project:

### Customers
- customer_id
- customer_name
- email
- registration_date
- customer_type

Customer types:
- REGULAR
- PREMIUM
- VIP

### Products
- product_id
- product_name
- category
- subcategory
- cost_price

### Orders
- order_id
- customer_id
- order_date
- status
- region_code

Order statuses:
- PLACED
- SHIPPED
- DELIVERED
- CANCELLED
- RETURNED

### Order Items
- item_id
- order_id
- product_id
- quantity
- unit_price
- discount_percent

Negative quantities represent product returns.

---

## Project Workflow

### Part 1 – Data Generation

Python and Faker were used to generate realistic sample datasets.

Intentional data-quality issues were introduced, including:

- Missing customer IDs
- Invalid email addresses
- Incorrect date formats
- Mixed-case and whitespace issues in product names
- Negative quantities representing returns

---

### Part 2 – Data Cleaning

Pandas was used to:

- Standardize date formats
- Handle missing customer IDs
- Normalize product names
- Validate customer emails
- Remove duplicates
- Validate numerical values
- Check referential integrity
- Export cleaned datasets

A data-quality report is generated at:

`output/issues_report.txt`

---

### Part 3 – SQL Analytics

The cleaned datasets are loaded into SQLite.

The database includes:

- Primary keys
- Foreign keys
- CHECK constraints
- Indexes

SQL analysis includes:

#### Basic Queries
1. Revenue per product category
2. Top 10 customers by total order value
3. Month-wise order count

#### Intermediate Queries
4. Customers with no delivered orders
5. Products with more returns than purchases
6. Return rate per category

#### Advanced Queries
7. Running revenue totals by region
8. Product ranking using DENSE_RANK
9. Customer order-gap analysis using LAG
10. Multi-level CTE segmentation
11. Lifetime-value segmentation using NTILE
12. Year-over-year revenue comparison
13. First vs most recent purchased category
14. Cumulative customer revenue distribution
15. Cohort retention analysis
16. Frequently bought-together products

---

## Part 4 – Python + SQL CLI

The reporting CLI accepts:

- Report type: daily / weekly / monthly
- Start date
- End date

It generates:

- Total orders
- Total revenue
- Unique customers
- Top 3 products
- Previous-period comparison
- Revenue percentage change

Run:

```bash
python Week8/scripts/report_cli.py
```

---

## Part 5 – Edge Case Testing

Python test functions validate:

- Invalid order IDs
- Discounts greater than 100%
- Zero quantity
- Future order dates

Run:

```bash
python Week8/scripts/test_edge_cases.py
```

---

## Folder Structure

```text
Week8/
├── data/
│   ├── raw/
│   └── cleaned/
├── database/
├── output/
│   └── sample_reports/
├── screenshots/
├── scripts/
├── sql/
├── README.md
└── requirements.txt
```

---

## How to Run

### 1. Generate data

```bash
python Week8/scripts/generate_data.py
```

### 2. Clean data

```bash
python Week8/scripts/clean_data.py
```

### 3. Build SQLite database

```bash
python Week8/scripts/load_database.py
```

### 4. Run SQL analytics

```bash
sqlite3 Week8/database/ecommerce.db
```

Inside SQLite:

```sql
.read Week8/sql/aggregations.sql
.read Week8/sql/window_functions.sql
```

### 5. Run CLI

```bash
python Week8/scripts/report_cli.py
```

### 6. Run edge-case tests

```bash
python Week8/scripts/test_edge_cases.py
```

---

## Key Learning Outcomes

This project demonstrates:

- Data generation
- Data cleaning
- Data validation
- Referential integrity
- SQL joins and aggregations
- CTEs
- Window functions
- Customer segmentation
- Cohort analysis
- Python-SQL integration
- CLI development
- Edge-case handling

---

## Author

**Tanvi Ballal**

Celebal Technologies – Data Engineering Internship

Week 8 Assignment