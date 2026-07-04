import pandas as pd
import pyodbc

file_path = r"D:\data engineer project\RetailAnalyticsPlatform\data\raw\olist_customers_dataset.csv"

df = pd.read_csv(file_path)

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS01;"
    "DATABASE=RetailDw;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

print("Connected to SQL Server")
print("Rows Found:", len(df))

for index, row in df.iterrows():

    cursor.execute("""
        INSERT INTO dbo.dim_Customer
        (Customer_ID, Customer_city, Customer_State)
        VALUES (?, ?, ?)
    """,
    row['customer_id'],
    row['customer_city'],
    row['customer_state'])

conn.commit()

print("Data Loaded Successfully!")

conn.close()