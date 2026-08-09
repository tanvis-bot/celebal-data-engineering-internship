from pathlib import Path
import re
import pandas as pd


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
CLEAN_DIR = PROJECT_ROOT / "data" / "cleaned"
OUTPUT_DIR = PROJECT_ROOT / "output"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


issues = []


# --------------------------------------------------
# Load Raw Data
# --------------------------------------------------

customers = pd.read_csv(RAW_DIR / "customers.csv")
products = pd.read_csv(RAW_DIR / "products.csv")
orders = pd.read_csv(RAW_DIR / "orders.csv")
order_items = pd.read_csv(RAW_DIR / "order_items.csv")


print("Raw datasets loaded successfully.")

print("Customers:", len(customers))
print("Products:", len(products))
print("Orders:", len(orders))
print("Order Items:", len(order_items))


# --------------------------------------------------
# 1. clean_orders()
# --------------------------------------------------

def clean_orders(df):
    df = df.copy()

    print("\nCleaning orders...")

    # Duplicate check
    duplicate_count = df.duplicated().sum()

    issues.append(
        f"Duplicate order rows found: {duplicate_count}"
    )

    df = df.drop_duplicates()


    # Missing customer IDs
    missing_customer_count = df["customer_id"].isna().sum()

    issues.append(
        f"Orders with missing customer_id: "
        f"{missing_customer_count}"
    )

    # Implementation choice:
    # remove orders without customer_id so the cleaned
    # SQL database maintains a valid customer relationship.
    df = df.dropna(subset=["customer_id"])

    df["customer_id"] = df["customer_id"].astype(int)


    # Fix mixed date formats
    def parse_order_date(value):

        if pd.isna(value):
            return pd.NaT

        value = str(value).strip()

        # Expected format
        try:
            return pd.to_datetime(
                value,
                format="%Y-%m-%d %H:%M:%S"
            )
        except ValueError:
            pass

        # Intentional incorrect DD-MM-YYYY format
        try:
            return pd.to_datetime(
                value,
                format="%d-%m-%Y"
            )
        except ValueError:
            return pd.NaT


    df["order_date"] = df["order_date"].apply(
        parse_order_date
    )

    invalid_dates = df["order_date"].isna().sum()

    issues.append(
        f"Unparseable order dates removed: {invalid_dates}"
    )

    df = df.dropna(subset=["order_date"])


    # Standardize date format
    df["order_date"] = df["order_date"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    # Standardize status
    df["status"] = (
        df["status"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    valid_statuses = [
        "PLACED",
        "SHIPPED",
        "DELIVERED",
        "CANCELLED",
        "RETURNED"
    ]

    invalid_status_count = (
        ~df["status"].isin(valid_statuses)
    ).sum()

    issues.append(
        f"Orders with invalid status removed: "
        f"{invalid_status_count}"
    )

    df = df[df["status"].isin(valid_statuses)]


    # Standardize region
    df["region_code"] = (
        df["region_code"]
        .astype(str)
        .str.strip()
        .str.upper()
    )


    print(
        "Orders cleaned:",
        len(df)
    )

    return df


# --------------------------------------------------
# 2. clean_products()
# --------------------------------------------------

def clean_products(df):
    df = df.copy()

    print("\nCleaning products...")

    duplicate_count = df.duplicated().sum()

    issues.append(
        f"Duplicate product rows found: {duplicate_count}"
    )

    df = df.drop_duplicates()


    # Assignment specifically requires:
    # trim spaces + title case
    df["product_name"] = (
        df["product_name"]
        .astype(str)
        .str.strip()
        .str.title()
    )


    df["category"] = (
        df["category"]
        .astype(str)
        .str.strip()
        .str.title()
    )


    df["subcategory"] = (
        df["subcategory"]
        .astype(str)
        .str.strip()
        .str.title()
    )


    # Cost price numeric validation
    df["cost_price"] = pd.to_numeric(
        df["cost_price"],
        errors="coerce"
    )

    invalid_prices = (
        df["cost_price"].isna()
        | (df["cost_price"] <= 0)
    ).sum()

    issues.append(
        f"Products with invalid cost_price removed: "
        f"{invalid_prices}"
    )

    df = df[
        df["cost_price"].notna()
        & (df["cost_price"] > 0)
    ]


    print(
        "Products cleaned:",
        len(df)
    )

    return df


# --------------------------------------------------
# 3. validate_emails()
# --------------------------------------------------

def validate_emails(df):
    """
    Return customer_ids whose emails are invalid.
    """

    invalid_customer_ids = []

    email_pattern = (
        r"^[A-Za-z0-9._%+-]+@"
        r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    for _, row in df.iterrows():

        email = row["email"]

        if (
            pd.isna(email)
            or not re.match(
                email_pattern,
                str(email).strip()
            )
        ):
            invalid_customer_ids.append(
                row["customer_id"]
            )

    return invalid_customer_ids


# --------------------------------------------------
# Clean Customers
# --------------------------------------------------

def clean_customers(df):
    df = df.copy()

    print("\nCleaning customers...")

    duplicate_count = df.duplicated().sum()

    issues.append(
        f"Duplicate customer rows found: "
        f"{duplicate_count}"
    )

    df = df.drop_duplicates()


    invalid_email_ids = validate_emails(df)

    issues.append(
        f"Customers with invalid emails: "
        f"{len(invalid_email_ids)}"
    )

    issues.append(
        "Invalid email customer IDs: "
        + ", ".join(
            map(str, invalid_email_ids)
        )
    )


    # For clean dataset, remove invalid email records.
    df = df[
        ~df["customer_id"].isin(
            invalid_email_ids
        )
    ]


    df["customer_name"] = (
        df["customer_name"]
        .astype(str)
        .str.strip()
        .str.title()
    )


    df["email"] = (
        df["email"]
        .astype(str)
        .str.strip()
        .str.lower()
    )


    df["customer_type"] = (
        df["customer_type"]
        .astype(str)
        .str.strip()
        .str.upper()
    )


    valid_types = [
        "REGULAR",
        "PREMIUM",
        "VIP"
    ]

    invalid_types = (
        ~df["customer_type"].isin(valid_types)
    ).sum()

    issues.append(
        f"Invalid customer_type records removed: "
        f"{invalid_types}"
    )

    df = df[
        df["customer_type"].isin(valid_types)
    ]


    df["registration_date"] = pd.to_datetime(
        df["registration_date"],
        errors="coerce"
    )

    invalid_registration_dates = (
        df["registration_date"].isna().sum()
    )

    issues.append(
        f"Invalid registration dates removed: "
        f"{invalid_registration_dates}"
    )

    df = df.dropna(
        subset=["registration_date"]
    )


    df["registration_date"] = (
        df["registration_date"]
        .dt.strftime("%Y-%m-%d")
    )


    print(
        "Customers cleaned:",
        len(df)
    )

    return df


# --------------------------------------------------
# Clean Order Items
# --------------------------------------------------

def clean_order_items(df):
    df = df.copy()

    print("\nCleaning order items...")

    duplicate_count = df.duplicated().sum()

    issues.append(
        f"Duplicate order-item rows found: "
        f"{duplicate_count}"
    )

    df = df.drop_duplicates()


    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    df["unit_price"] = pd.to_numeric(
        df["unit_price"],
        errors="coerce"
    )

    df["discount_percent"] = pd.to_numeric(
        df["discount_percent"],
        errors="coerce"
    )


    # IMPORTANT:
    # Negative quantity means RETURN.
    # Do NOT remove negative quantities.

    null_quantity = df["quantity"].isna().sum()

    issues.append(
        f"Order items with invalid quantity: "
        f"{null_quantity}"
    )

    df = df.dropna(subset=["quantity"])


    invalid_price = (
        df["unit_price"].isna()
        | (df["unit_price"] <= 0)
    ).sum()

    issues.append(
        f"Order items with invalid unit_price: "
        f"{invalid_price}"
    )

    df = df[
        df["unit_price"].notna()
        & (df["unit_price"] > 0)
    ]


    invalid_discount = (
        df["discount_percent"].isna()
        | (df["discount_percent"] < 0)
        | (df["discount_percent"] > 100)
    ).sum()

    issues.append(
        f"Invalid discount_percent values: "
        f"{invalid_discount}"
    )

    df = df[
        df["discount_percent"].notna()
        & (df["discount_percent"] >= 0)
        & (df["discount_percent"] <= 100)
    ]


    print(
        "Order items cleaned:",
        len(df)
    )

    return df


# --------------------------------------------------
# 4. check_referential_integrity()
# --------------------------------------------------

def check_referential_integrity(
    order_items_df,
    orders_df
):
    """
    Find order_items referencing an order_id
    that doesn't exist in orders.
    """

    valid_order_ids = set(
        orders_df["order_id"]
    )

    invalid_items = order_items_df[
        ~order_items_df["order_id"].isin(
            valid_order_ids
        )
    ]

    return invalid_items


# --------------------------------------------------
# Run Cleaning
# --------------------------------------------------

customers_clean = clean_customers(
    customers
)

products_clean = clean_products(
    products
)

orders_clean = clean_orders(
    orders
)

order_items_clean = clean_order_items(
    order_items
)


# --------------------------------------------------
# Referential Integrity
# --------------------------------------------------

invalid_order_items = (
    check_referential_integrity(
        order_items_clean,
        orders_clean
    )
)

issues.append(
    "Order items referencing non-existent orders: "
    f"{len(invalid_order_items)}"
)


# Remove invalid references from clean dataset
order_items_clean = order_items_clean[
    order_items_clean["order_id"].isin(
        orders_clean["order_id"]
    )
]


# Product referential-integrity check
invalid_products = order_items_clean[
    ~order_items_clean["product_id"].isin(
        products_clean["product_id"]
    )
]

issues.append(
    "Order items referencing non-existent products: "
    f"{len(invalid_products)}"
)


order_items_clean = order_items_clean[
    order_items_clean["product_id"].isin(
        products_clean["product_id"]
    )
]


# Customer referential-integrity check
invalid_customer_orders = orders_clean[
    ~orders_clean["customer_id"].isin(
        customers_clean["customer_id"]
    )
]

issues.append(
    "Orders referencing non-existent customers: "
    f"{len(invalid_customer_orders)}"
)


orders_clean = orders_clean[
    orders_clean["customer_id"].isin(
        customers_clean["customer_id"]
    )
]


# Re-check order_items because removing orders above
# may make some items invalid.
order_items_clean = order_items_clean[
    order_items_clean["order_id"].isin(
        orders_clean["order_id"]
    )
]


# --------------------------------------------------
# Export Cleaned CSVs
# --------------------------------------------------

customers_clean.to_csv(
    CLEAN_DIR / "customers_clean.csv",
    index=False
)

products_clean.to_csv(
    CLEAN_DIR / "products_clean.csv",
    index=False
)

orders_clean.to_csv(
    CLEAN_DIR / "orders_clean.csv",
    index=False
)

order_items_clean.to_csv(
    CLEAN_DIR / "order_items_clean.csv",
    index=False
)


# --------------------------------------------------
# Issues Report
# --------------------------------------------------

report_path = (
    OUTPUT_DIR / "issues_report.txt"
)

with open(
    report_path,
    "w",
    encoding="utf-8"
) as report:

    report.write(
        "WEEK 8 - DATA CLEANING ISSUES REPORT\n"
    )

    report.write(
        "=" * 50 + "\n\n"
    )

    for issue in issues:
        report.write(issue + "\n")

    report.write("\n")
    report.write("=" * 50 + "\n")

    report.write(
        f"Final customers: "
        f"{len(customers_clean)}\n"
    )

    report.write(
        f"Final products: "
        f"{len(products_clean)}\n"
    )

    report.write(
        f"Final orders: "
        f"{len(orders_clean)}\n"
    )

    report.write(
        f"Final order_items: "
        f"{len(order_items_clean)}\n"
    )


# --------------------------------------------------
# Final Output
# --------------------------------------------------

print("\n" + "=" * 50)

print("DATA CLEANING COMPLETED")

print("=" * 50)

print(
    "Customers:",
    len(customers_clean)
)

print(
    "Products:",
    len(products_clean)
)

print(
    "Orders:",
    len(orders_clean)
)

print(
    "Order Items:",
    len(order_items_clean)
)

print(
    "\nIssues report:",
    report_path
)

print(
    "\nCleaned CSV files created successfully."
)