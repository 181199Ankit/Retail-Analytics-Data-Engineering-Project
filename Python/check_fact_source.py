import pandas as pd

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

print("\nOrders Columns:")
print(orders.columns)

print("\nItems Columns:")
print(items.columns)

print("\nPayments Columns:")
print(payments.columns)