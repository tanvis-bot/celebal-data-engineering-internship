from pathlib import Path
import sqlite3
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CLEAN_DIR = PROJECT_ROOT / "data" / "cleaned"
DATABASE_DIR = PROJECT_ROOT / "database"

DATABASE_PATH = DATABASE_DIR / "ecommerce.db"
SCHEMA_PATH = PROJECT_ROOT / "sql" / "schema.sql"


# --------------------------------------------------
# Check cleaned files
# --------------------------------------------------

files = {
    "customers":
        CLEAN_DIR / "customers_clean.csv",

    "products":
        CLEAN_DIR / "products_clean.csv",

    "orders":
        CLEAN_DIR / "orders_clean.csv",

    "order_items":
        CLEAN_DIR / "order_items_clean.csv"
}


for name, path in files.items():

    if not path.exists():

        raise FileNotFoundError(
            f"Missing cleaned file: {path}"
        )


# --------------------------------------------------
# Load CSVs
# --------------------------------------------------

customers = pd.read_csv(
    files["customers"]
)

products = pd.read_csv(
    files["products"]
)

orders = pd.read_csv(
    files["orders"]
)

order_items = pd.read_csv(
    files["order_items"]
)


print("Cleaned datasets loaded.")

print(
    "Customers:",
    len(customers)
)

print(
    "Products:",
    len(products)
)

print(
    "Orders:",
    len(orders)
)

print(
    "Order Items:",
    len(order_items)
)


# --------------------------------------------------
# Create Database
# --------------------------------------------------

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# Delete previous DB if it exists
if DATABASE_PATH.exists():

    DATABASE_PATH.unlink()

    print(
        "\nOld ecommerce.db removed."
    )


connection = sqlite3.connect(
    DATABASE_PATH
)

connection.execute(
    "PRAGMA foreign_keys = ON;"
)


# --------------------------------------------------
# Create Schema
# --------------------------------------------------

schema_sql = SCHEMA_PATH.read_text(
    encoding="utf-8"
)

connection.executescript(
    schema_sql
)

print(
    "Database schema created successfully."
)


# --------------------------------------------------
# Insert helper
# --------------------------------------------------

def insert_dataframe(
    table_name,
    dataframe
):

    columns = dataframe.columns.tolist()

    placeholders = ", ".join(
        ["?"] * len(columns)
    )

    column_string = ", ".join(
        columns
    )

    sql = f"""
        INSERT INTO {table_name}
        ({column_string})
        VALUES ({placeholders})
    """

    records = list(
        dataframe.itertuples(
            index=False,
            name=None
        )
    )

    connection.executemany(
        sql,
        records
    )

    print(
        f"{table_name}: "
        f"{len(records)} rows inserted"
    )


# --------------------------------------------------
# Insert in parent → child order
# --------------------------------------------------

try:

    insert_dataframe(
        "customers",
        customers
    )

    insert_dataframe(
        "products",
        products
    )

    insert_dataframe(
        "orders",
        orders
    )

    insert_dataframe(
        "order_items",
        order_items
    )

    connection.commit()

except Exception as error:

    connection.rollback()

    print(
        "\nDatabase loading failed:"
    )

    print(error)

    connection.close()

    raise


# --------------------------------------------------
# Verify row counts
# --------------------------------------------------

print(
    "\nDATABASE ROW COUNTS"
)

print(
    "=" * 45
)


for table_name in [
    "customers",
    "products",
    "orders",
    "order_items"
]:

    count = connection.execute(
        f"""
        SELECT COUNT(*)
        FROM {table_name}
        """
    ).fetchone()[0]

    print(
        f"{table_name}: {count}"
    )


# --------------------------------------------------
# Foreign Key Check
# --------------------------------------------------

violations = connection.execute(
    "PRAGMA foreign_key_check;"
).fetchall()


print(
    "\nFOREIGN KEY CHECK"
)

print(
    "=" * 45
)


if len(violations) == 0:

    print(
        "PASSED - No foreign key violations"
    )

else:

    print(
        "FAILED"
    )

    for row in violations:
        print(row)


# --------------------------------------------------
# Show tables
# --------------------------------------------------

tables = connection.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
    """
).fetchall()


print(
    "\nTABLES CREATED"
)

print(
    "=" * 45
)


for table in tables:
    print(table[0])


# --------------------------------------------------
# Sample join
# --------------------------------------------------

sample_query = """
SELECT
    o.order_id,
    o.order_date,
    o.region_code,
    c.customer_name,
    p.product_name,
    p.category,
    oi.quantity,
    oi.unit_price,
    oi.discount_percent
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
LIMIT 10;
"""


sample = pd.read_sql_query(
    sample_query,
    connection
)


print(
    "\nSAMPLE JOINED DATA"
)

print(
    "=" * 45
)

print(
    sample.to_string(
        index=False
    )
)


connection.close()


print(
    "\nDatabase created successfully:"
)

print(
    DATABASE_PATH
)