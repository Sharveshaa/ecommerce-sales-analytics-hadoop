
import csv
import random
from datetime import datetime, timedelta

random.seed(42)

products = {
    "Laptop": ("Electronics", 50000),
    "Mobile": ("Electronics", 15000),
    "Tablet": ("Electronics", 25000),
    "Headphones": ("Accessories", 2000),
    "Mouse": ("Accessories", 500),
    "Keyboard": ("Accessories", 1200),
    "Monitor": ("Electronics", 12000),
    "Chair": ("Furniture", 8000),
    "Desk": ("Furniture", 10000),
    "Backpack": ("Fashion", 1800),
    "Shoes": ("Fashion", 3000),
    "Watch": ("Fashion", 5000)
}

regions = ["North", "South", "East", "West", "Central"]
payments = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]

start_date = datetime(2025, 1, 1)

with open("sales.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "OrderID", "Date", "Product", "Category",
        "Quantity", "Price", "Region", "PaymentMode"
    ])

    for order_id in range(10001, 20001):
        product = random.choice(list(products.keys()))
        category, price = products[product]

        quantity = random.randint(1, 5)
        order_date = start_date + timedelta(
            days=random.randint(0, 364)
        )

        region = random.choice(regions)
        payment = random.choice(payments)

        writer.writerow([
            order_id,
            order_date.strftime("%Y-%m-%d"),
            product,
            category,
            quantity,
            price,
            region,
            payment
        ])

print("Dataset generated successfully!")
print("Total transactions: 10000")
print("Columns: 8")
