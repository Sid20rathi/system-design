# System design for the 10 minute delivery system


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
        

