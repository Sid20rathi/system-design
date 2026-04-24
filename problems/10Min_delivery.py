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




