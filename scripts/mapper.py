
#!/usr/bin/env python3

import sys
import csv

reader = csv.reader(sys.stdin)

for row in reader:
    if not row or row[0] == "OrderID":
        continue

    if len(row) != 8:
        continue

    order_id, date, product, category, quantity, price, region, payment = row

    quantity = int(quantity)
    price = float(price)
    revenue = quantity * price
    month = date[:7]

    # Product analytics
    print(f"PRODUCT|{product}\t{revenue},{quantity}")

    # Region analytics
    print(f"REGION|{region}\t{revenue},{quantity}")

    # Category analytics
    print(f"CATEGORY|{category}\t{revenue},{quantity}")

    # Monthly analytics
    print(f"MONTH|{month}\t{revenue},{quantity}")

    # Payment analytics
    print(f"PAYMENT|{payment}\t{revenue},{quantity}")
