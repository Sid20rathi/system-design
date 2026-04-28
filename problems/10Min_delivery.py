# System design for the 10 minute delivery system

from abc import ABC , abstractmethod
class Product:
    def __init__(self,id,name,price):
        self.id = id
        self.name = name
        self.price = price


class PersihableProduct(Product):
    def __init__(self,id,name,price,expiry):
        super().__init__(self,id,name,price)
        self.expiry = expiry

class Productfactory():
    @staticmethod
    def create_product(product_type, *args, **kwargs):
        if product_type == "perishable":
            return PersihableProduct(*args, **kwargs)
        return Product(*args, **kwargs)
        

class InventoryStore(ABC):

    @abstractmethod
    def addd_item(self,store_id,product,quantiy):
        pass

    @abstractmethod
    def remove_item(self,store_id,product_id,quantity):
        pass

    @abstractmethod
    def restock(self,store_id,product_id):
        pass

class Dbstore(InventoryStore):

    def __init__(self):
        self.db={}
    
    def add_item(self,store_id,product,quantity):
        self.db.setdefault(store_id,{})
        self.db[store_id][product.product.id] = self.db[store_id].get(product.product_id, 0) + quantity

    def remove_item(self,store_id,product_id,quantity):
        if self.db[store_id].get(product_id,0)< quantity:
            raise Exception("Insufficient stock")
        self.db[store_id][product_id] -= quantity
    
    def get_stock(self,store_id,product_id):
        # it find the current quantity of the item in the stock or in the store
        return self.db.get(store_id,{}).get(product_id,0)



class InventoryStore:

    def __init__(self,inventory_store):
        self.inventory_store = inventory_store

    def add_stock(self,store_id,product,qty):
        self.inventory_store.add_item(store_id,product,qty)

    def remove_stock(self,store_id,product_id,qty):
        self.inventory_store.remove_item(store_id,product_id,qty)
    

    def check_stock(self, store_id, product_id):
        return self.inventory_store.get_stock(store_id, product_id)




class ReplenishmentStrategy(ABC):

    @abstractmethod
    def should_replenish(self, current_stock):
        pass

class ThresholdStrategy(ReplenishmentStrategy):

    def __init__(self, threshold):
        self.threshold = threshold

    def should_replenish(self, current_stock):
        return current_stock < self.threshold



class WeeklyStrategy(ReplenishmentStrategy):

    def should_replenish(self, current_stock):
        
        return True


import math

class DarkStore:
    def __init__(self, store_id, lat, lon):
        self.store_id = store_id
        self.lat = lat
        self.lon = lon

class DarkStoreManager:

    _instance = None

    def __init__(self):
        self.stores = []

    @staticmethod
    def get_instance():
        if not DarkStoreManager._instance:
            DarkStoreManager._instance = DarkStoreManager()
        return DarkStoreManager._instance

    def add_store(self, store):
        self.stores.append(store)

    def get_nearby_stores(self, user_lat, user_lon, radius_km=5):
        def distance(lat1, lon1, lat2, lon2):
            return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

        return [
            store for store in self.stores
            if distance(user_lat, user_lon, store.lat, store.lon) <= radius_km
        ]


class Cart:
    def __init__(self):
        self.items = {}  # product_id -> quantity

    def add_item(self, product_id, qty):
        self.items[product_id] = self.items.get(product_id, 0) + qty



class OrderService:

    def __init__(self, inventory_manager, dark_store_manager):
        self.inventory_manager = inventory_manager
        self.dark_store_manager = dark_store_manager

    def place_order(self, cart, user_lat, user_lon):
        stores = self.dark_store_manager.get_nearby_stores(user_lat, user_lon)

        allocation = {}  # store_id -> {product_id: qty}

        for product_id, qty in cart.items.items():
            remaining = qty

            for store in stores:
                stock = self.inventory_manager.check_stock(store.store_id, product_id)

                if stock > 0:
                    taken = min(stock, remaining)
                    allocation.setdefault(store.store_id, {})
                    allocation[store.store_id][product_id] = taken

                    remaining -= taken
                    if remaining == 0:
                        break

            if remaining > 0:
                raise Exception("Out of stock")

        return allocation