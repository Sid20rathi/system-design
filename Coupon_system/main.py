## Have to design a coupon system that can generate coupons and apply them to orders.

from abc import ABC , abstractmethod


class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price



class CartItem():
    def __init__(self,product,quantity):
        self.product = product
        self.quantity = quantity

    def total_price(self):
        return self.product.price * self.quantity

class Cart:
    def __init__(self):
        self.items = []
        self.applied_coupons = []

    def add_item(self, product, quantity):
        self.items.append(CartItem(product, quantity))

    def total_amount(self):
        return sum(item.total_price() for item in self.items)

    def apply_discount(self, discount, coupon_name):
        self.applied_coupons.append((coupon_name, discount))

    def __str__(self):
        return f"Cart Total: {self.total_amount()}"

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate_discount(self, amount):
        pass


class FlatDiscount(DiscountStrategy):
    def __init__(self, discount):
        self.discount = discount

    def calculate_discount(self, amount):
        return min(self.discount, amount)


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent):
        self.percent = percent

    def calculate_discount(self, amount):
        return amount * self.percent / 100


class CappedPercentageDiscount(DiscountStrategy):
    def __init__(self, percent, cap):
        self.percent = percent
        self.cap = cap

    def calculate_discount(self, amount):
        return min(amount * self.percent / 100, self.cap)




class Coupon:
    def __init__(
        self,
        name,
        strategy,
        min_amount=0,
        applicable_product_ids=None,
        stackable=True
    ):
        self.name = name
        self.strategy = strategy
        self.min_amount = min_amount
        self.applicable_product_ids = applicable_product_ids or []
        self.stackable = stackable
        self.next = None

    def set_next(self, next_coupon):
        self.next = next_coupon
        return next_coupon

    def apply(self, cart):
        total_discount = 0

        # Product-level discount
        if self.applicable_product_ids:
            for item in cart.items:
                if item.product.product_id in self.applicable_product_ids:
                    discount = self.strategy.calculate_discount(item.total_price())
                    total_discount += discount

        # Cart-level discount
        else:
            cart_total = cart.total_amount()
            if cart_total >= self.min_amount:
                total_discount = self.strategy.calculate_discount(cart_total)

        if total_discount > 0:
            print(f"{self.name} applied: -{total_discount}")
            cart.apply_discount(total_discount, self.name)

            # Reduce price logically (not mutating product)
            self._reduce_cart(cart, total_discount)

            if not self.stackable:
                print(f"{self.name} is non-stackable. Stopping chain.")
                return cart

        if self.next:
            return self.next.apply(cart)

        return cart

    def _reduce_cart(self, cart, discount):
        # distribute discount proportionally
        total = cart.total_amount()
        if total == 0:
            return

        ratio = discount / total

        for item in cart.items:
            reduction = item.total_price() * ratio
            item.product.price -= reduction / item.quantity


class CouponManager:
    _instance = None

    def __init__(self):
        self.coupons = []

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def register_coupon(self, coupon):
        self.coupons.append(coupon)

    def apply_coupons(self, cart):
        if not self.coupons:
            return cart

        head = self.coupons[0]
        current = head

        for coupon in self.coupons[1:]:
            current = current.set_next(coupon)

        return head.apply(cart)


if __name__ == "__main__":
    # Products
    p1 = Product(1, "Laptop", 1000)
    p2 = Product(2, "Phone", 500)
    p3 = Product(3, "Headphones", 200)

    # Cart
    cart = Cart()
    cart.add_item(p1, 1)
    cart.add_item(p2, 2)
    cart.add_item(p3, 3)

    print(f"Initial Cart Total:",cart.total_amount())

    # Strategies
    flat_100 = FlatDiscount(100)
    percent_10 = PercentageDiscount(10)
    capped_20 = CappedPercentageDiscount(20, 150)

    # Coupons
    c1 = Coupon("FLAT100", flat_100, min_amount=500)
    c2 = Coupon("PHONE10", percent_10, applicable_product_ids=[2])
    c3 = Coupon("BIG20", capped_20, min_amount=500, stackable=False)

    # Manager
    manager = CouponManager.get_instance()
    manager.register_coupon(c1)
    manager.register_coupon(c2)
    manager.register_coupon(c3)

    # Apply
    final_cart = manager.apply_coupons(cart)

    print("\n--- FINAL BILL ---")
    print(f"Final Total: {final_cart.total_amount()}")
    print(f"Coupons Applied: {final_cart.applied_coupons}")