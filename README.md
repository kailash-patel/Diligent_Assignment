# Diligent_Assignment
# Diligent Assignment

This project generates synthetic e-commerce datasets (CSV files) and loads them into an SQLite database. It also provides a sample SQL query for analyzing user purchases with payment details.

## Project Structure

- `generate_data.py` – Creates realistic CSV datasets in `data/`
- `ingest_to_sqlite.py` – Loads CSVs into `ecommerce.db`
- `data/` – Output folder containing `users.csv`, `products.csv`, `orders.csv`, `order_items.csv`, `payments.csv`

## Requirements

- Python 3.9+
- pip packages: `pandas`, `numpy`

Install dependencies:

```bash
pip install pandas numpy
```

## Generate Synthetic Data

```bash
python generate_data.py
```

This creates five CSV files under `data/` with 70–120 rows each, maintaining referential integrity between users, orders, products, order items, and payments.

## Load Data into SQLite

```bash
python ingest_to_sqlite.py
```

- Creates/overwrites `ecommerce.db`
- Builds tables `users`, `products`, `orders`, `order_items`, `payments`
- Inserts all CSV rows using pandas + sqlite3
- Prints `Data successfully ingested.` when done

## Sample Analysis Query

```sql
SELECT
    u.name AS user_name,
    p.name AS product_name,
    oi.quantity,
    oi.subtotal,
    pay.payment_method,
    pay.status AS payment_status
FROM users AS u
JOIN orders AS o ON o.user_id = u.user_id
JOIN order_items AS oi ON oi.order_id = o.order_id
JOIN products AS p ON p.product_id = oi.product_id
JOIN payments AS pay ON pay.order_id = o.order_id;
```

Run it with any SQLite client (e.g., `sqlite3 ecommerce.db`) to list every purchased product with associated user and payment information.

## Pushing to GitHub

If the remote repository uses `main`:

```bash
git branch -M main
git remote add origin https://github.com/<username>/Diligent_Assignment.git
git push -u origin main
```

