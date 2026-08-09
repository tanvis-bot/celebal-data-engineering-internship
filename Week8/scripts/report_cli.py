import sqlite3
from datetime import datetime, timedelta

DB_PATH = "Week8/database/ecommerce.db"


def connect_db():
    try:
        return sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None


def get_summary(conn, start_date, end_date):
    query = """
    SELECT
        COUNT(DISTINCT o.order_id) AS total_orders,
        ROUND(
            COALESCE(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 0),
            2
        ) AS total_revenue,
        COUNT(DISTINCT o.customer_id) AS unique_customers
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE DATE(o.order_date) BETWEEN DATE(?) AND DATE(?)
    """

    return conn.execute(query, (start_date, end_date)).fetchone()


def get_top_products(conn, start_date, end_date):
    query = """
    SELECT
        p.product_name,
        SUM(oi.quantity) AS quantity_sold,
        ROUND(
            SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)),
            2
        ) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    JOIN products p
        ON oi.product_id = p.product_id
    WHERE DATE(o.order_date) BETWEEN DATE(?) AND DATE(?)
    GROUP BY p.product_id, p.product_name
    ORDER BY revenue DESC
    LIMIT 3
    """

    return conn.execute(query, (start_date, end_date)).fetchall()


def previous_period(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    days = (end - start).days + 1

    previous_end = start - timedelta(days=1)
    previous_start = previous_end - timedelta(days=days - 1)

    return (
        previous_start.strftime("%Y-%m-%d"),
        previous_end.strftime("%Y-%m-%d")
    )


def run_report(start_date, end_date):
    conn = connect_db()

    if conn is None:
        return

    try:
        # Validate dates
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        if start > end:
            print("\nError: Start date cannot be after end date.")
            return

        total_orders, revenue, customers = get_summary(
            conn, start_date, end_date
        )

        print("\n==========================================")
        print("        E-COMMERCE ANALYTICS REPORT")
        print("==========================================")
        print(f"Period           : {start_date} to {end_date}")
        print(f"Total Orders     : {total_orders}")
        print(f"Total Revenue    : {revenue}")
        print(f"Unique Customers : {customers}")

        print("\nTOP 3 PRODUCTS")
        print("------------------------------------------")

        products = get_top_products(conn, start_date, end_date)

        if products:
            for i, product in enumerate(products, start=1):
                print(
                    f"{i}. {product[0]} | "
                    f"Qty: {product[1]} | Revenue: {product[2]}"
                )
        else:
            print("No products found for this period.")

        # Previous period comparison
        prev_start, prev_end = previous_period(start_date, end_date)

        prev_orders, prev_revenue, prev_customers = get_summary(
            conn, prev_start, prev_end
        )

        print("\nPREVIOUS PERIOD COMPARISON")
        print("------------------------------------------")
        print(f"Previous Period  : {prev_start} to {prev_end}")
        print(f"Previous Orders  : {prev_orders}")
        print(f"Previous Revenue : {prev_revenue}")
        print(f"Previous Customers: {prev_customers}")

        if prev_revenue and prev_revenue != 0:
            growth = ((revenue - prev_revenue) / prev_revenue) * 100
            print(f"Revenue Growth   : {growth:.2f}%")
        else:
            print("Revenue Growth   : N/A")

        print("==========================================\n")

    except ValueError:
        print("\nError: Enter dates in YYYY-MM-DD format.")

    except sqlite3.Error as e:
        print(f"\nSQL error: {e}")

    finally:
        conn.close()


def main():

    print("\n==========================================")
    print("       E-COMMERCE REPORTING TOOL")
    print("==========================================")

    report_type = input(
        "Enter report type (daily/weekly/monthly): "
    ).strip().lower()

    valid_types = [
        "daily",
        "weekly",
        "monthly"
    ]

    if report_type not in valid_types:

        print(
            "\nInvalid report type."
        )

        print(
            "Choose daily, weekly, or monthly."
        )

        return

    print(
        f"\nSelected report type: "
        f"{report_type.upper()}"
    )

    start_date = input(
        "Start date (YYYY-MM-DD): "
    ).strip()

    end_date = input(
        "End date   (YYYY-MM-DD): "
    ).strip()

    run_report(
        start_date,
        end_date
    )

if __name__ == "__main__":
    main()