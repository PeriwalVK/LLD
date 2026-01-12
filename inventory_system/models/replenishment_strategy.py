from abc import ABC, abstractmethod

from inventory_system.constants import ProductCategory
from inventory_system.models.product import Product
from inventory_system.models.warehouse import Warehouse


class IReplenishmentStrategy(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def replenish(self, warehouse: Warehouse, product: Product):
        pass

class JustInTimeReplenishmentStrategy(IReplenishmentStrategy):
    def __init__(self):
        self.count = {
            ProductCategory.CLOTHING: 2,
            ProductCategory.ELECTRONICS: 3,
            ProductCategory.FOOD: 4
        }
    def replenish(self, warehouse: Warehouse, product: Product):
        if product.sku in warehouse.products:
            warehouse.products[product.sku].qty += self.count[product.category] 