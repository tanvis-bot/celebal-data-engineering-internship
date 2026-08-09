from pathlib import Path
from faker import Faker
import pandas as pd
import random


# --------------------------------------------------
# Setup
# --------------------------------------------------

fake = Faker("en_IN")

random.seed(42)
Faker.seed(42)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)


NUM_CUSTOMERS = 500
NUM_PRODUCTS = 500
NUM_ORDERS = 500
NUM_ORDER_ITEMS = 1000


# --------------------------------------------------
# Customers
# --------------------------------------------------

customer_types = [
    "REGULAR",
    "PREMIUM",
    "VIP"
]

customers = []

for customer_id in range(
    1,
    NUM_CUSTOMERS + 1
):

    email = fake.email()

    # Approximately 2% invalid emails
    if random.random() < 0.02:

        if random.choice([True, False]):
            email = email.replace("@", "")
        else:
            email = email.split("@")[0] + "@"

    customers.append(
        {
            "customer_id": customer_id,

            "customer_name": fake.name(),

            "email": email,

            "registration_date":
                fake.date_between(
                    start_date="-3y",
                    end_date="today"
                ).strftime("%Y-%m-%d"),

            "customer_type":
                random.choice(
                    customer_types
                )
        }
    )


customers_df = pd.DataFrame(customers)


# --------------------------------------------------
# Products
# --------------------------------------------------

category_map = {

    "Electronics": [
        "Mobile",
        "Laptop",
        "Accessories"
    ],

    "Clothing": [
        "Men",
        "Women",
        "Kids"
    ],

    "Home": [
        "Kitchen",
        "Furniture",
        "Decor"
    ],

    "Books": [
        "Fiction",
        "Education",
        "Comics"
    ]
}


products = []


for product_id in range(
    1,
    NUM_PRODUCTS + 1
):

    category = random.choice(
        list(category_map.keys())
    )

    subcategory = random.choice(
        category_map[category]
    )

    product_name = (
        fake.word()
        + " "
        + random.choice(
            [
                "Pro",
                "Classic",
                "Premium",
                "Plus"
            ]
        )
    )

    # Some names get extra spaces
    if random.random() < 0.05:
        product_name = (
            "   " + product_name + "   "
        )

    # Some names get mixed casing
    if random.random() < 0.05:
        product_name = product_name.upper()

    products.append(
        {
            "product_id": product_id,

            "product_name": product_name,

            "category": category,

            "subcategory": subcategory,

            "cost_price":
                round(
                    random.uniform(
                        100,
                        5000
                    ),
                    2
                )
        }
    )


products_df = pd.DataFrame(products)


# --------------------------------------------------
# Orders
# --------------------------------------------------

statuses = [
    "PLACED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
    "RETURNED"
]

regions = [
    "NORTH",
    "SOUTH",
    "EAST",
    "WEST"
]


orders = []


for order_id in range(
    1,
    NUM_ORDERS + 1
):

    customer_id = random.randint(
        1,
        NUM_CUSTOMERS
    )

    # Approximately 5% NULL customer IDs
    if random.random() < 0.05:
        customer_id = None

    order_datetime = (
        fake.date_time_between(
            start_date="-2y",
            end_date="now"
        )
    )

    # Some dates intentionally use DD-MM-YYYY
    if random.random() < 0.05:

        order_date = (
            order_datetime.strftime(
                "%d-%m-%Y"
            )
        )

    else:

        order_date = (
            order_datetime.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )


    orders.append(
        {
            "order_id": order_id,

            "customer_id": customer_id,

            "order_date": order_date,

            "status":
                random.choice(
                    statuses
                ),

            "region_code":
                random.choice(
                    regions
                )
        }
    )


orders_df = pd.DataFrame(orders)


# --------------------------------------------------
# Order Items
# --------------------------------------------------

order_items = []


for item_id in range(
    1,
    NUM_ORDER_ITEMS + 1
):

    quantity = random.randint(
        1,
        5
    )

    # Approximately 3% negative quantities = returns
    if random.random() < 0.03:
        quantity = -quantity


    order_items.append(
        {
            "item_id": item_id,

            # Always references an existing order
            "order_id":
                random.randint(
                    1,
                    NUM_ORDERS
                ),

            "product_id":
                random.randint(
                    1,
                    NUM_PRODUCTS
                ),

            "quantity":
                quantity,

            "unit_price":
                round(
                    random.uniform(
                        100,
                        8000
                    ),
                    2
                ),

            "discount_percent":
                random.randint(
                    0,
                    50
                )
        }
    )


order_items_df = pd.DataFrame(
    order_items
)


# --------------------------------------------------
# Save CSV files
# --------------------------------------------------

customers_df.to_csv(
    RAW_DIR / "customers.csv",
    index=False
)

products_df.to_csv(
    RAW_DIR / "products.csv",
    index=False
)

orders_df.to_csv(
    RAW_DIR / "orders.csv",
    index=False
)

order_items_df.to_csv(
    RAW_DIR / "order_items.csv",
    index=False
)


# --------------------------------------------------
# Verification
# --------------------------------------------------

print("\nDatasets generated successfully.")

print(
    "Customers:",
    len(customers_df)
)

print(
    "Products:",
    len(products_df)
)

print(
    "Orders:",
    len(orders_df)
)

print(
    "Order Items:",
    len(order_items_df)
)


print("\nFiles saved to:")
print(RAW_DIR)


print("\nColumns:")

print(
    "customers:",
    customers_df.columns.tolist()
)

print(
    "products:",
    products_df.columns.tolist()
)

print(
    "orders:",
    orders_df.columns.tolist()
)

print(
    "order_items:",
    order_items_df.columns.tolist()
)


print(
    "\nMissing customer_id:",
    orders_df["customer_id"]
    .isna()
    .sum()
)

print(
    "Negative quantity rows:",
    (
        order_items_df["quantity"] < 0
    ).sum()
)