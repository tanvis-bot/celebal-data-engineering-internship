-- Customers table
CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT,
    segment TEXT,
    country TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    region TEXT
);

-- Products table
CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    sub_category TEXT
);

-- Orders table
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    order_date TEXT,
    ship_date TEXT,
    ship_mode TEXT,
    customer_id TEXT,
    sales REAL,
    quantity INTEGER,
    discount REAL,
    profit REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);