import pandas as pd
import pyodbc

# Generate dates
dates = pd.date_range(
    start="2016-01-01",
    end="2018-12-31"
)

df = pd.DataFrame({
    "date_key": dates.strftime("%Y%m%d"),
    "full_date": dates,
    "year": dates.year,
    "month": dates.month,
    "day": dates.day,
    "quater": dates.quarter
})

print("Total Dates:", len(df))

# SQL Connection
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS01;"
    "DATABASE=RetailDw;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

for index, row in df.iterrows():

    cursor.execute("""
    INSERT INTO dbo.dim_date
    (date_key, full_date, year, month, day, quater)
    VALUES (?, ?, ?, ?, ?, ?)
    """,

    row["date_key"],
    row["full_date"],
    row["year"],
    row["month"],
    row["day"],
    row["quater"]
    )

conn.commit()

print("Date Dimension Loaded Successfully!")

cursor.close()
conn.close()