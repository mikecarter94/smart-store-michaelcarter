
import pandas as pd
import sqlite3
import pathlib
import sys

# For local imports, temporarily add project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Constants
DW_DIR = pathlib.Path("data").joinpath("dw")
DB_PATH = DW_DIR.joinpath("smart_sales.db")
PREPARED_DATA_DIR = pathlib.Path("data").joinpath("prepared")

def create_schema(cursor: sqlite3.Cursor) -> None:
    """Drop and recreate tables in the data warehouse."""

    # Drop tables to force updated schema (especially during dev)
    cursor.execute("DROP TABLE IF EXISTS sale")
    cursor.execute("DROP TABLE IF EXISTS customer")
    cursor.execute("DROP TABLE IF EXISTS product")

    # Now recreate all tables with updated columns
    cursor.execute("""
        CREATE TABLE customer (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            region TEXT,
            join_date TEXT,
            LoyaltyPoints INTEGER,
            preferred_contact_method TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT,
            unit_price REAL,
            stock_quantity INTEGER,
            supplier TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE sale (
            sale_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_id INTEGER,
            sale_amount REAL,
            sale_date TEXT,
            discount_percent REAL,
            payment_type TEXT,
            store_id TEXT,
            campaign_id TEXT, --
            FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
            FOREIGN KEY (product_id) REFERENCES product (product_id)
        )
    """)


def delete_existing_records(cursor: sqlite3.Cursor) -> None:
    """Delete all existing records and reset primary keys."""
    cursor.execute("DELETE FROM customer")
    cursor.execute("DELETE FROM product")
    cursor.execute("DELETE FROM sale")

def insert_customers(customers_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert customer data into the customer table."""
    customers_df.to_sql("customer", cursor.connection, if_exists="append", index=False)

def insert_products(products_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert product data into the product table."""
    products_df.to_sql("product", cursor.connection, if_exists="append", index=False)

def insert_sales(sales_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert sales data into the sales table."""
    sales_df.to_sql("sale", cursor.connection, if_exists="append", index=False)

import os

def load_data_to_db() -> None:
    conn = None  # ensure variable exists
    try:
        print("Working directory:", os.getcwd())  # where Python is running from
        print("DW_DIR (should be under /data/dw):", DW_DIR.resolve())
        print("DB_PATH:", DB_PATH.resolve())

        # ✅ Ensure /data/dw directory exists
        DW_DIR.mkdir(parents=True, exist_ok=True)

        # ✅ Create the DB file
        conn = sqlite3.connect(DB_PATH)
        print("Connected to database.")

        cursor = conn.cursor()

        # Create schema and clear existing records
        create_schema(cursor)
        print("Schema created.")

        delete_existing_records(cursor)
        print("Old records deleted.")

        # Load prepared data using pandas
        customers_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("customers_data_prepared.csv"))
        customers_df = customers_df.drop(columns=["Unnamed: 0"], errors="ignore")
        customers_df = customers_df.rename(columns={
            "CustomerID": "customer_id",
            "Name": "name",
            "Region": "region",
            "JoinDate": "join_date",
            "LoyaltyPoints": "LoyaltyPoints",
            "preferred_contact_method": "preferred_contact_method"
        })

# ✅ Drop duplicate primary keys based on customer_id
        customers_df = customers_df.drop_duplicates(subset="customer_id")

        print("Customers loaded:", len(customers_df), "rows")
        print("Duplicate customer IDs:", customers_df['customer_id'].duplicated().sum())


        products_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("products_data_prepared.csv"))
        products_df = products_df.drop(columns=["Unnamed: 0"], errors="ignore")
        print("Products loaded:", len(products_df), "rows")

        sales_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("sales_data_prepared.csv"))
        sales_df = sales_df.drop(columns=["Unnamed: 0"], errors="ignore")
        sales_df = sales_df.rename(columns={
            "TransactionID": "sale_id",  
            "CustomerID": "customer_id",
            "ProductID": "product_id",
            "SaleAmount": "sale_amount",
            "SaleDate": "sale_date",
            "StoreID": "store_id",
            "DiscountPercent": "discount_percent",
            "CampaignID": "campaign_id",
            "PaymentType": "payment_type",
        })

        # Optional: drop duplicates if needed
        sales_df = sales_df.drop_duplicates(subset="sale_id")

        print("Sales loaded:", len(sales_df), "rows")
        print("Duplicate sale IDs:", sales_df['sale_id'].duplicated().sum())




        print("CSV files loaded.")

        # Insert data into the database
        insert_customers(customers_df, cursor)
        insert_products(products_df, cursor)
        insert_sales(sales_df, cursor)

        print("Data inserted into DB.")
        conn.commit()
        print("Transaction committed.")

    except Exception as e:
        print("Error occurred:", e)
    finally:
        if conn:
            conn.close()
            print("Connection closed.")
if __name__ == "__main__":
    load_data_to_db()