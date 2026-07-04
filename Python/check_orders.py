import pandas as pd

orders = pd.read_csv(
    r"D:\data engineer project\RetailAnalyticsPlatform\data\raw\olist_orders_dataset.csv"
)

print("Total Orders:", len(orders))

print("\nColumns:")
print(orders.columns)

print("\nFirst 5 Rows:")
print(orders.head())