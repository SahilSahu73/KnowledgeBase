from enum import Enum

'''
Enum (enumeration) - data type that defines a fixed set of named constants.
Unlike strings or integers, enums are type-safe, meaning the compiler ensures that
you can only use values that actually exist in your defined set.
They ensure that a variable can only take one out of a predefined set of valid options.

Examples:
 - order states -> (e.g. "PENDING", "IN_PROGRESS", "COMPLETED")
 - user Roles -> (e.g. "Admin", "CUSTOMER", "DRIVER")
'''

class OrderStatus(Enum):
    PLACED = "PLACED"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

status = OrderStatus.SHIPPED

print(status)
if status == OrderStatus.SHIPPED:
    print(f"Your package is on your way - {status}")



'''
Enums with Properties and Methods

Each enum value can hold additional data and even define behavior.
'''
class Coin(Enum):
    PENNY = 1
    NICKEL = 5
    DIME = 10
    QUATER = 25

    def __init__(self, value):
        self.coin_value = value

    def get_value(self):
        return self.coin_value

total = Coin.DIME.get_value() + Coin.QUATER.get_value()
print(total)
