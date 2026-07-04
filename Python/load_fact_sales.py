import pandas as pd
import pyodbc

# Source files
orders = pd.read_csv(
    r"D:\data engineer project\RetailAnalyticsPlatform\data\raw\olist_orders_dataset.csv"
)

items = pd.read_csv(
    r"D:\data engineer project\RetailAnalyticsPlatform\data\raw\olist_order_items_dataset.csv"
)

payments = pd.read_csv(
    r"D:\data engineer project\RetailAnalyticsPlatform\data\raw\olist_order_payments_dataset.csv"
)

# SQL Connection
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS01;"
    "DATABASE=RetailDw;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

print("Connected to SQL Server")

# Preview counts
print("Orders:", len(orders))
print("Items:", len(items))
print("Payments:", len(payments))

#loading the data

import pandas as pd
import pyodbc

# Source files
orders = pd.read_csv(
    r"D:\data engineer project\RetailAnalyticsPlatform\data\raw\olist_orders_dataset.csv"
)

items = pd.read_csv(
    r"D:\data engineer project\RetailAnalyticsPlatform\data\raw\olist_order_items_dataset.csv"
)

payments = pd.read_csv(
    r"D:\data engineer project\RetailAnalyticsPlatform\data\raw\olist_order_payments_dataset.csv"
)

# SQL Connection
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS01;"
    "DATABASE=RetailDw;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

print("Connected to SQL Server")

# Preview counts
print("Orders:", len(orders))
print("Items:", len(items))
print("Payments:", len(payments))
import pandas as pd
import pyodbc

# ==========================
# Load Source Files
# ==========================

orders = pd.read_csv(
    r"D:\data engineer project\RetailAnalyticsPlatform\data\raw\olist_orders_dataset.csv"
)

items = pd.read_csv(
    r"D:\data engineer project\RetailAnalyticsPlatform\data\raw\olist_order_items_dataset.csv"
)

payments = pd.read_csv(
    r"D:\data engineer project\RetailAnalyticsPlatform\data\raw\olist_order_payments_dataset.csv"
)

print("Orders:", len(orders))
print("Items:", len(items))
print("Payments:", len(payments))

# ==========================
# Connect SQL Server
# ==========================

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS01;"
    "DATABASE=RetailDw;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

print("Connected to SQL Server")

# ==========================
# Load Dimension Tables
# ==========================

customer_dim = pd.read_sql(
    "SELECT customer_key, Customer_ID FROM dbo.dim_customer",
    conn
)

# Remove duplicate customers
customer_dim = customer_dim.drop_duplicates(
    subset=["Customer_ID"]
)

print("Customer Dim Rows:", len(customer_dim))
print("Distinct Customer IDs:",
      customer_dim["Customer_ID"].nunique())

product_dim = pd.read_sql(
    "SELECT product_key, product_id FROM dbo.dim_product",
    conn
)

# ==========================
# Prepare Date Key
# ==========================

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

orders["date_key"] = (
    orders["order_purchase_timestamp"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

# ==========================
# Build Fact Dataset
# ==========================

fact_df = orders[[
    "order_id",
    "customer_id",
    "date_key"
]]

fact_df = fact_df.merge(
    items[["order_id", "product_id"]],
    on="order_id",
    how="inner"
)
print("Payment Rows:", len(payments))
print("Distinct Orders:", payments["order_id"].nunique())

# Check rows after items merge
print("Rows after items merge:", len(fact_df))
print("Distinct orders after items merge:",
      fact_df["order_id"].nunique())

# Aggregate payments first
payment_summary = (
    payments.groupby("order_id", as_index=False)
    ["payment_value"]
    .sum()
)

# Merge aggregated payments
fact_df = fact_df.merge(
    payment_summary,
    on="order_id",
    how="inner"
)

print("Rows after payment merge:", len(fact_df))
print("Distinct orders after payment merge:",
      fact_df["order_id"].nunique())

# ==========================
# Map Customer Key
# ==========================

fact_df = fact_df.merge(
    customer_dim,
    left_on="customer_id",
    right_on="Customer_ID",
    how="left"
)

print("Rows after customer merge:", len(fact_df))
print("Distinct orders after customer merge:", fact_df["order_id"].nunique())

# ==========================
# Map Product Key
# ==========================

fact_df = fact_df.merge(
    product_dim,
    on="product_id",
    how="left"
)
print("Rows after product merge:", len(fact_df))
print("Distinct orders after product merge:", fact_df["order_id"].nunique())

# ==========================
# Create Quantity
# ==========================

fact_df["quantity"] = 1

# ==========================
# Keep Final Columns
# ==========================
print(fact_df.columns)

print("Rows before final select:", len(fact_df))
print("Distinct orders before final select:", fact_df["order_id"].nunique())

fact_df = fact_df[
    [
        "order_id",
        "customer_key",
        "product_key",
        "date_key",
        "payment_value",
        "quantity"
    ]
]

print("\nFact Rows:", len(fact_df))
print(fact_df.head())

# ===========================
# Load Into SQL Server
# ===========================
print("Fact Rows:", len(fact_df))
print(fact_df.head())

print("Null Customer Keys:", fact_df["customer_key"].isna().sum())
print("Null Product Keys:", fact_df["product_key"].isna().sum())
print("Null Date Keys:", fact_df["date_key"].isna().sum())

for index, row in fact_df.iterrows():

    cursor.execute(
        """
        INSERT INTO dbo.fact_sales
        (
            order_id,
            customer_key,
            product_key,
            date_key,
            payment_value,
            quantity
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            str(row["order_id"]),
            int(row["customer_key"]),
            int(row["product_key"]),
            int(row["date_key"]),
            float(row["payment_value"]),
            int(row["quantity"])
        )
    )

conn.commit()

cursor.execute("SELECT COUNT(*) FROM dbo.fact_sales")
count = cursor.fetchone()[0]
print("Rows in fact_sales:", count)

cursor.execute("SELECT TOP 5 * FROM dbo.fact_sales")

for r in cursor.fetchall():
    print(r)

print("Fact Sales Loaded Successfully!")

