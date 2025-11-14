import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta


def random_datetime(rng: np.random.Generator, start: datetime, end: datetime) -> datetime:
    delta = end - start
    random_seconds = rng.integers(0, int(delta.total_seconds()))
    return start + timedelta(seconds=int(random_seconds))


def build_users(rng: np.random.Generator, count: int) -> pd.DataFrame:
    first_names = [
        "Avery",
        "Jordan",
        "Parker",
        "Morgan",
        "Riley",
        "Logan",
        "Quinn",
        "Taylor",
        "Sawyer",
        "Harper",
    ]
    last_names = [
        "Chen",
        "Singh",
        "Garcia",
        "Patel",
        "Brown",
        "Nguyen",
        "Khan",
        "Silva",
        "Lopez",
        "Adams",
    ]
    domain_choices = ["example.com", "shopper.io", "mail.net"]
    user_rows = []
    start = datetime(2023, 1, 1)
    end = datetime(2025, 1, 1)

    for user_id in range(1, count + 1):
        first = rng.choice(first_names)
        last = rng.choice(last_names)
        full_name = f"{first} {last}"
        base_email = f"{first.lower()}.{last.lower()}"
        email = f"{base_email}{rng.integers(1, 999)}@{rng.choice(domain_choices)}"
        created_at = random_datetime(rng, start, end)
        user_rows.append(
            {
                "user_id": user_id,
                "name": full_name,
                "email": email,
                "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return pd.DataFrame(user_rows)


def build_products(rng: np.random.Generator, count: int) -> pd.DataFrame:
    categories = [
        "Electronics",
        "Home",
        "Outdoors",
        "Fashion",
        "Beauty",
        "Sports",
        "Toys",
        "Automotive",
    ]
    adjectives = [
        "Premium",
        "Compact",
        "Eco",
        "Smart",
        "Vintage",
        "Portable",
        "Deluxe",
        "Classic",
    ]
    items = [
        "Speaker",
        "Backpack",
        "Lamp",
        "Camera",
        "Watch",
        "Jacket",
        "Sneakers",
        "Drone",
        "Cookware",
        "Tent",
        "Blender",
        "Monitor",
        "Tablet",
        "Headphones",
        "Chair",
        "Desk",
        "Sunglasses",
        "Fitness Band",
    ]

    product_rows = []
    for product_id in range(1, count + 1):
        category = rng.choice(categories)
        name = f"{rng.choice(adjectives)} {rng.choice(items)}"
        price = round(rng.uniform(10, 400), 2)
        product_rows.append(
            {
                "product_id": product_id,
                "name": name,
                "category": category,
                "price": price,
            }
        )

    return pd.DataFrame(product_rows)


def build_orders(
    rng: np.random.Generator, users_df: pd.DataFrame, count: int
) -> pd.DataFrame:
    order_rows = []
    now = datetime(2025, 1, 15)

    for order_id in range(1, count + 1):
        user = users_df.sample(n=1, random_state=rng.integers(0, 1_000_000)).iloc[0]
        user_created = datetime.strptime(user["created_at"], "%Y-%m-%d %H:%M:%S")
        order_date = random_datetime(rng, user_created, now)
        order_rows.append(
            {
                "order_id": order_id,
                "user_id": int(user["user_id"]),
                "order_date": order_date.strftime("%Y-%m-%d %H:%M:%S"),
                "total_amount": 0.0,  # placeholder, filled later
            }
        )

    return pd.DataFrame(order_rows)


def build_order_items(
    rng: np.random.Generator, orders_df: pd.DataFrame, products_df: pd.DataFrame
) -> pd.DataFrame:
    item_rows = []
    item_id = 1
    product_prices = products_df.set_index("product_id")["price"].to_dict()

    for _, order in orders_df.iterrows():
        num_items = int(rng.integers(1, 5))
        chosen_products = rng.choice(
            products_df["product_id"], size=num_items, replace=False
        )
        for product_id in chosen_products:
            quantity = int(rng.integers(1, 4))
            price = product_prices[int(product_id)]
            subtotal = round(price * quantity, 2)
            item_rows.append(
                {
                    "item_id": item_id,
                    "order_id": int(order["order_id"]),
                    "product_id": int(product_id),
                    "quantity": quantity,
                    "subtotal": subtotal,
                }
            )
            item_id += 1

    return pd.DataFrame(item_rows)


def build_payments(
    rng: np.random.Generator, orders_df: pd.DataFrame
) -> pd.DataFrame:
    methods = ["card", "paypal", "bank_transfer", "wallet"]
    statuses = ["Completed", "Pending", "Failed", "Refunded"]
    status_probs = [0.7, 0.15, 0.1, 0.05]
    payment_rows = []

    for _, order in orders_df.iterrows():
        payment_rows.append(
            {
                "payment_id": len(payment_rows) + 1,
                "order_id": int(order["order_id"]),
                "payment_method": rng.choice(methods),
                "status": rng.choice(statuses, p=status_probs),
                "amount": round(order["total_amount"], 2),
            }
        )

    return pd.DataFrame(payment_rows)


def main():
    rng = np.random.default_rng(42)
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    users_df = build_users(rng, 85)
    products_df = build_products(rng, 70)
    orders_df = build_orders(rng, users_df, 120)
    order_items_df = build_order_items(rng, orders_df, products_df)

    order_totals = (
        order_items_df.groupby("order_id")["subtotal"].sum().reindex(
            orders_df["order_id"], fill_value=0.0
        )
    )
    orders_df["total_amount"] = order_totals.round(2).values

    payments_df = build_payments(rng, orders_df)

    users_df.to_csv(data_dir / "users.csv", index=False)
    products_df.to_csv(data_dir / "products.csv", index=False)
    orders_df.to_csv(data_dir / "orders.csv", index=False)
    order_items_df.to_csv(data_dir / "order_items.csv", index=False)
    payments_df.to_csv(data_dir / "payments.csv", index=False)


if __name__ == "__main__":
    main()

