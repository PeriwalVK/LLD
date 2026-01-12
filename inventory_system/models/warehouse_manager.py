from typing import Dict
from inventory_system.models.replenishment_strategy import IReplenishmentStrategy
from inventory_system.models.warehouse import Warehouse


class WarehouseManager:
    def __init__(self, id: str, name: str, replenishment_strategy: IReplenishmentStrategy, warehouses: Dict[str, Warehouse]=dict()):
        self.id = id
        self.name = name
        self.warehouses: Dict[str, Warehouse] = warehouses
        self.replenishment_strategy = replenishment_strategy
    
    def add_warehouse(self, warehouse: Warehouse):
        self.warehouses[warehouse.id] = warehouse
    
    def remove_warehouse(self, warehouse: Warehouse):
        del self.warehouses[warehouse.id]
    
    def set_replenishment_strategy(self, replenishment_strategy: IReplenishmentStrategy):
        self.replenishment_strategy = replenishment_strategy
    
    def 
    


