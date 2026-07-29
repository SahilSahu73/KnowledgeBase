class Car:
    # Constructor
    def __init__(self, brand, model):
    # Attributes (private by convention with underscore)
        self._brand = brand
        self._model = model
        self._speed = 0

    # Method to accelerate
    def accelerate(self, increment: int):
        self._speed += increment

    # Method to display info
    def display_info(self):
        print(f"{self._brand} is running at {self._speed} km/hr.")

'''
This class Car defines what every Car object should look like (brand, model, speed)
and what it can do (accelerate, display status).
An object is an instance of class.
It's the actual thing you can interact with, store data in, and invoke methods on.
'''

# Another example of food delivery app
'''
The scenario:
Food delivery app needs to manage orders.
Each order belongs to a customer, contains a list of food items with prices, and tracks
whether it has been places or not. Customers build there orders by placing one item at a
time, once satisfied, they place the order. After that no more items can be added.
'''
class FoodOrder:
    def __init__(self, order_id: str, customer_name: str):
        self._order_id = order_id
        self._customer_name = customer_name
        self._items: list[str] = []
        self._total_amount = 0.0
        self._is_placed = False

    # Only allow adding items before the order is placed
    def add_item(self, item_name: str, price: float) -> None:
        if self._is_placed:
            print("Cannot add items after order is placed.")
            return
        self._items.append(item_name)
        self._total_amount += price

    def place_order(self) -> bool:
        if self._is_placed or not self._items:
            return False
        self._is_placed = True
        return True

    def get_item_count(self) -> int:
        return len(self._items)

    def display_order(self) -> None:
        status = "PLACED" if self._is_placed else "PENDING"
        print(f"Order {self._order_id} ({self._customer_name} - {status})")
        for item in self._items:
            print(f"  - {item}")
        print(f"Total: ${self._total_amount:.2f}")


if __name__ == "__main__":
    #   # creating objects of the Car class
    #   corolla = Car("Toyota", "Corolla")
    #   mustang = Car("Ford", "Mustang")
    #
    #   corolla.accelerate(50)
    #   mustang.accelerate(60)
    #
    #   # Displaying status of each car
    #   corolla.display_info()
    #   print("---------------")
    #   mustang.display_info()

    order1 = FoodOrder("ORD-101", "Alice")
    order1.add_item("Pizza", 12.99)
    order1.add_item("Pasta", 8.99)
    order1.add_item("Garlic Bread", 4.99)
    order1.add_item("Diet Coke", 2.49)
    order1.place_order()

    order2 = FoodOrder("ORD-102", "Sahil")
    order2.add_item("Burger", 7.49)
    order2.add_item("Fries", 3.89)

    order1.display_order()
    print("-----")
    order2.display_order()

