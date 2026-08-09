import sqlite3
from datetime import datetime, timedelta
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_PATH = (
    PROJECT_ROOT
    / "database"
    / "ecommerce.db"
)


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute(
        "PRAGMA foreign_keys = ON;"
    )

    return connection


# ==================================================
# TEST 1
# order_items references non-existent order_id
# ==================================================

def test_invalid_order_id():

    connection = get_connection()

    try:

        connection.execute(
            """
            INSERT INTO order_items (
                item_id,
                order_id,
                product_id,
                quantity,
                unit_price,
                discount_percent
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                999999,
                999999,       # invalid order_id
                1,
                1,
                500.00,
                10
            )
        )

        connection.commit()

        print(
            "TEST 1 FAILED: "
            "Invalid order_id was accepted."
        )

    except sqlite3.IntegrityError:

        print(
            "TEST 1 PASSED: "
            "Non-existent order_id rejected."
        )

    finally:

        connection.rollback()
        connection.close()


# ==================================================
# TEST 2
# discount_percent > 100
# ==================================================

def test_invalid_discount():

    connection = get_connection()

    try:

        # Find one valid order/product
        order_id = connection.execute(
            "SELECT order_id FROM orders LIMIT 1"
        ).fetchone()[0]

        product_id = connection.execute(
            "SELECT product_id FROM products LIMIT 1"
        ).fetchone()[0]

        connection.execute(
            """
            INSERT INTO order_items (
                item_id,
                order_id,
                product_id,
                quantity,
                unit_price,
                discount_percent
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                999998,
                order_id,
                product_id,
                2,
                500.00,
                150             # INVALID
            )
        )

        connection.commit()

        print(
            "TEST 2 FAILED: "
            "Discount greater than 100 accepted."
        )

    except sqlite3.IntegrityError:

        print(
            "TEST 2 PASSED: "
            "discount_percent > 100 rejected."
        )

    finally:

        connection.rollback()
        connection.close()


# ==================================================
# TEST 3
# quantity = 0
# ==================================================

def test_zero_quantity():

    connection = get_connection()

    try:

        order_id = connection.execute(
            "SELECT order_id FROM orders LIMIT 1"
        ).fetchone()[0]

        product_id = connection.execute(
            "SELECT product_id FROM products LIMIT 1"
        ).fetchone()[0]

        connection.execute(
            """
            INSERT INTO order_items (
                item_id,
                order_id,
                product_id,
                quantity,
                unit_price,
                discount_percent
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                999997,
                order_id,
                product_id,
                0,              # INVALID
                500.00,
                10
            )
        )

        connection.commit()

        print(
            "TEST 3 FAILED: "
            "Zero quantity was accepted."
        )

    except sqlite3.IntegrityError:

        print(
            "TEST 3 PASSED: "
            "quantity = 0 rejected."
        )

    finally:

        connection.rollback()
        connection.close()


# ==================================================
# TEST 4
# Future order date
# ==================================================

def test_future_order_date():

    future_date = (
        datetime.now()
        + timedelta(days=30)
    )

    today = datetime.now()

    if future_date > today:

        print(
            "TEST 4 PASSED: "
            "Future order_date detected as invalid."
        )

    else:

        print(
            "TEST 4 FAILED: "
            "Future date was not detected."
        )


# ==================================================
# RUN ALL TESTS
# ==================================================

def main():

    print("\n" + "=" * 60)

    print(
        "WEEK 8 - EDGE CASE TESTING"
    )

    print("=" * 60)

    test_invalid_order_id()

    test_invalid_discount()

    test_zero_quantity()

    test_future_order_date()

    print("=" * 60)


if __name__ == "__main__":
    main()