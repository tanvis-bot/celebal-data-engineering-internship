-- Insert Customers
INSERT OR IGNORE INTO customers
SELECT DISTINCT
    "Customer ID",
    "Customer Name",
    Segment,
    Country,
    City,
    State,
    "Postal Code",
    Region
FROM superstore_raw;

-- Insert Products
INSERT OR IGNORE INTO products
SELECT DISTINCT
    "Product ID",
    "Product Name",
    Category,
    "Sub-Category"
FROM superstore_raw;

-- Insert Orders
INSERT OR IGNORE INTO orders
SELECT DISTINCT
    "Order ID",
    "Order Date",
    "Ship Date",
    "Ship Mode",
    "Customer ID",
    CAST(Sales AS REAL),
    CAST(Quantity AS INTEGER),
    CAST(Discount AS REAL),
    CAST(Profit AS REAL)
FROM superstore_raw;