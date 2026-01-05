from vending_machine.constants import OrderStatus
from vending_machine.models.product import Product


class VendingMachineOrder:
    def __init__(self, product: Product, qty: int):
        self.product: Product = product
        self.quantity: int = qty
        self.total_amount: float = qty * product.price
        self.status: OrderStatus = OrderStatus.IN_PROGRESS

    def cancel_order(self):
        self.status = OrderStatus.CANCELLED

    def complete_order(self):
        self.status = OrderStatus.COMPLETED

    # def get_order_status(self) -> OrderStatus:
    #     return self.status
