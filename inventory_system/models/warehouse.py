from ast import Dict
from typing import List
from inventory_system.models.product import Product


class Warehouse:
    def __init__(self, id: str, name: str, products: Dict[str, Product]=dict()):
        self.id = id
        self.name = name
        self.products: Dict[str, Product] = products
        
    def add_product(self, product: Product):
        self.products[product.sku] = product
    
    def remove_product(self, product: Product):
        del self.products[product.sku]

    def get_available_qty(self, sku):
        return 0 if sku not in self.products else self.products[sku].qty
    