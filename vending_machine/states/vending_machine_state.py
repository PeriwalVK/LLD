from __future__ import annotations
from abc import ABC, abstractmethod
from os import name
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from vending_machine.models.vending_machine import VendingMachine
from vending_machine.models.vending_machine_order import VendingMachineOrder


class VendingMachineState(ABC):
    def __init__(self):
        pass

    @override
    def __str__(self):
        pass

    @abstractmethod
    def insert_coin(
        self, vending_machine: VendingMachine, coin: int
    ) -> VendingMachineState:
        pass

    @abstractmethod
    def choose_item(
        self, vending_machine: VendingMachine, product_id: str, qty: int
    ) -> VendingMachineState:
        pass

    @abstractmethod
    def dispense_item(self, vending_machine: VendingMachine) -> VendingMachineState:
        pass

    @abstractmethod
    def cancel_transaction(
        self, vending_machine: VendingMachine
    ) -> VendingMachineState:
        pass


class ReadyState(VendingMachineState):
    def __init__(self):
        super().__init__()
        self.name = "ReadyState"

    @override
    def __str__(self):
        return self.name

    @override
    def choose_item(
        self, vending_machine: VendingMachine, product_id: str, qty: int
    ) -> VendingMachineState:
        if product_id not in vending_machine.products:
            print("product not available...")
            return self
        if vending_machine.qty.get(product_id, 0) < qty:
            print(
                f"insufficient stock...only {vending_machine.qty.get(product_id, 0)} is available"
            )
            return self
        vending_machine.current_order = VendingMachineOrder(
            vending_machine.products[product_id], qty
        )
        vending_machine.current_inserted_coins = 0
        print(f"Item chosen, Please insert {vending_machine.current_order.total_amount} coins now...")
        return vending_machine.product_selected_state

    @override
    def insert_coin(
        self, vending_machine: VendingMachine, coin: int
    ) -> VendingMachineState:
        print("Can't insert coin now, please Select Product First...")
        return self

    @override
    def dispense_item(self, vending_machine: VendingMachine) -> VendingMachineState:
        print("Select Product First and then insert coins...")
        return self

    @override
    def cancel_transaction(
        self, vending_machine: VendingMachine
    ) -> VendingMachineState:
        print("Already on Ready State, No order in process currently...")
        return self


class ProductSelectedState(VendingMachineState):
    def __init__(self):
        super().__init__()
        self.name = "ProductSelectedState"

    @override
    def __str__(self):
        return self.name

    @override
    def choose_item(
        self, vending_machine: VendingMachine, product_id: str, qty: int
    ) -> VendingMachineState:
        print("Please complete or cancel existing order first...")
        return self

    @override
    def insert_coin(
        self, vending_machine: VendingMachine, coin: int
    ) -> VendingMachineState:
        total_amt = vending_machine.current_order.total_amount
        vending_machine.current_inserted_coins += coin
        print(
            f"{coin} coins inserted successfully, total inserted coins: {vending_machine.current_inserted_coins}"
        )
        if vending_machine.current_inserted_coins < total_amt:
            print(
                f"Total order amount {total_amt}, please insert {total_amt - vending_machine.current_inserted_coins} more..."
            )
            return self
        else:
            if vending_machine.current_inserted_coins > total_amt:
                print(
                    f"Total order amount {total_amt}, refunding excess {vending_machine.current_inserted_coins - total_amt} coins"
                )
                vending_machine.current_inserted_coins = total_amt
            return vending_machine.coin_inserted_state

    @override
    def dispense_item(self, vending_machine: VendingMachine) -> VendingMachineState:
        print(
            f"Can't Dispense, Total order amount {vending_machine.current_order.total_amount}, Insert {vending_machine.current_order.total_amount - vending_machine.current_inserted_coins} more coins first..."
        )
        return self

    @override
    def cancel_transaction(
        self, vending_machine: VendingMachine
    ) -> VendingMachineState:
        if vending_machine.current_inserted_coins > 0:
            print(f"refunding {vending_machine.current_inserted_coins} coins")
            vending_machine.current_inserted_coins = 0

        vending_machine.current_order.cancel_order()
        vending_machine.orders.append(vending_machine.current_order)
        vending_machine.current_order = None

        print("Order Cancelled...")

        return vending_machine.ready_state


class CoinInsertedState(VendingMachineState):
    def __init__(self):
        super().__init__()
        self.name = "CoinInsertedState"

    @override
    def __str__(self):
        return self.name

    @override
    def choose_item(
        self, vending_machine: VendingMachine, product_id: str, qty: int
    ) -> VendingMachineState:
        print(
            "Please complete or cancel existing order first [coins already inserted, pending dispense]..."
        )
        return self

    @override
    def insert_coin(
        self, vending_machine: VendingMachine, coin: int
    ) -> VendingMachineState:
        print(
            "Sufficient Coins already inserted, Please complete or cancel existing order first..."
        )
        return self

    @override
    def dispense_item(self, vending_machine: VendingMachine) -> VendingMachineState:
        curr_order = vending_machine.current_order
        print(
            f"Please wait, dispensing {curr_order.quantity} units of {curr_order.product.name} ..."
        )
        
        vending_machine.remove_product(curr_order.product.id, curr_order.quantity)
        vending_machine.total_earnings += curr_order.total_amount

        curr_order.complete_order()
        vending_machine.orders.append(curr_order)
        vending_machine.current_order = None

        vending_machine.current_inserted_coins = 0

        print("Items successfully dispensed...")

        return vending_machine.ready_state

    @override
    def cancel_transaction(
        self, vending_machine: VendingMachine
    ) -> VendingMachineState:
        if vending_machine.current_inserted_coins > 0:
            print(f"refunding {vending_machine.current_inserted_coins} coins")
            vending_machine.current_inserted_coins = 0

        vending_machine.current_order.cancel_order()
        vending_machine.orders.append(vending_machine.current_order)
        vending_machine.current_order = None

        print("Order Cancelled...")

        return vending_machine.ready_state
