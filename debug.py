def calculate_total_price(items, discount_rate):
    total = 0
    for item in items:
        # Intentional error, trying to access 'price' attribute
        total += item.price * (1 - discount_rate)
    return total

shopping_cart = [
    {'name': 'Shirt', 'cost': 50},
    {'name': 'Pants', 'cost': 100}
]

import pdb
pdb.set_trace()  # Debugger will pause here
result = calculate_total_price(shopping_cart, 0.1)
print(result)