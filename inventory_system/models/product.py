from abc import ABC
from inventory_system.constants import ProductCategory


class Product(ABC):
    def __init__(self, sku: str, name: str, price: float, qty: int, category: ProductCategory, threshold: int):
        self.sku = sku
        self.name = name
        self.price = price
        self.qty = qty
        self.threshold = threshold
        self.category: ProductCategory = category
    
    def add_qty(self, cnt: int):
        self.qty += cnt
        print(f"updated qty for {self.sku} is {self.qty}")
    
    def reduce_qty(self, qty: int):
        self.qty -= qty

class ElectronicsProduct(Product):
    def __init__(self, sku: str, name: str, price: float, qty: int, threshold: int, warranty: int):
        super().__init__(sku, name, price, qty, ProductCategory.ELECTRONICS, threshold)
        self.warranty = warranty

class ClothingProduct(Product):
    def __init__(self, sku: str, name: str, price: float, qty: int, threshold: int, size: str):
        super().__init__(sku, name, price, qty, ProductCategory.CLOTHING, threshold)
        self.size = size

class FoodProduct(Product):
    def __init__(self, sku: str, name: str, price: float, qty: int, threshold: int, expiry_date: str):
        super().__init__(sku, name, price, qty, ProductCategory.FOOD, threshold)
        self.expiry_date = expiry_date
