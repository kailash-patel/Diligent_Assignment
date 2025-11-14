import sqlite3
from pathlib import Path

import pandas as pd


def load_csv_to_sqlite(cursor, table_name: str, csv_path: Path, dtype=None):
    df = pd.read_csv(csv_path, dtype=dtype)
    df.to_sql(table_name, cursor.connection, if_exists="replace", index=False)


def main():
    data_dir = Path("data")
    if not data_dir.exists():
        raise FileNotFoundError("The 'data' directory does not exist.")

    csv_files = {
        "users": data_dir / "users.csv",
        "products": data_dir / "products.csv",
        "orders": data_dir / "orders.csv",
        "order_items": data_dir / "order_items.csv",
        "payments": data_dir / "payments.csv",
    }

    missing = [name for name, path in csv_files.items() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing CSV files: {', '.join(missing)}")

    connection = sqlite3.connect("ecommerce.db")
    try:
        cursor = connection.cursor()

        load_csv_to_sqlite(
            cursor,
            "users",
            csv_files["users"],
            dtype={
                "user_id": "int64",
                "name": "string",
                "email": "string",
                "created_at": "string",
            },
        )

        load_csv_to_sqlite(
            cursor,
            "products",
            csv_files["products"],
            dtype={
                "product_id": "int64",
                "name": "string",
                "category": "string",
                "price": "float64",
            },
        )

        load_csv_to_sqlite(
            cursor,
            "orders",
            csv_files["orders"],
            dtype={
                "order_id": "int64",
                "user_id": "int64",
                "order_date": "string",
                "total_amount": "float64",
            },
        )

        load_csv_to_sqlite(
            cursor,
            "order_items",
            csv_files["order_items"],
            dtype={
                "item_id": "int64",
                "order_id": "int64",
                "product_id": "int64",
                "quantity": "int64",
                "subtotal": "float64",
            },
        )

        load_csv_to_sqlite(
            cursor,
            "payments",
            csv_files["payments"],
            dtype={
                "payment_id": "int64",
                "order_id": "int64",
                "payment_method": "string",
                "status": "string",
                "amount": "float64",
            },
        )

        connection.commit()
    finally:
        connection.close()

    print("Data successfully ingested.")


if __name__ == "__main__":
    main()

