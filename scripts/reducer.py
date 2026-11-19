
#!/usr/bin/env python3

import sys

current_key = None
total_revenue = 0.0
total_quantity = 0
total_orders = 0

def output_result(key, revenue, quantity, orders):
    print(
        f"{key}\t"
        f"Revenue: {revenue:.2f}\t"
        f"Quantity: {quantity}\t"
        f"Records: {orders}"
    )

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    key, values = line.split("\t", 1)
    revenue, quantity = values.split(",")

    revenue = float(revenue)
    quantity = int(quantity)

    if current_key is not None and key != current_key:
        output_result(
            current_key,
            total_revenue,
            total_quantity,
            total_orders
        )

        total_revenue = 0.0
        total_quantity = 0
        total_orders = 0

    current_key = key
    total_revenue += revenue
    total_quantity += quantity
    total_orders += 1

if current_key is not None:
    output_result(
        current_key,
        total_revenue,
        total_quantity,
        total_orders
    )
