import pandas as pd
import pyodbc

# Read products file
file_path = r"D:\data engineer project\RetailAnalyticsPlatform\data\raw\olist_products_dataset.csv"
df = pd.read_csv(file_path)

# Keep only required columns
df = df[['product_id', 'product_category_name']]

# Replace missing categories
df['product_category_name'] = df['product_category_name'].fillna('Unknown')

print("Products Found:", len(df))

# SQL Server Connection
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS01;"
    "DATABASE=RetailDw;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

# Insert data
for index, row in df.iterrows():
    cursor.execute("""
        INSERT INTO dbo.dim_product
        (product_id, product_category)
        VALUES (?, ?)
    """,
    row['product_id'],
    row['product_category_name'])

conn.commit()

print("Products Loaded Successfully!")

cursor.close()
conn.close()

