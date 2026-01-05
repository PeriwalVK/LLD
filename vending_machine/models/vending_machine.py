from typing import Dict, List
from vending_machine.models.vending_machine_order import VendingMachineOrder
from vending_machine.models.product import Product
from vending_machine.states.vending_machine_state import (
    CoinInsertedState,
    ProductSelectedState,
    ReadyState,
    VendingMachineState,
)


class VendingMachine:
    def __init__(self):
        self.ready_state: VendingMachineState = ReadyState()
        self.coin_inserted_state: VendingMachineState = CoinInsertedState()
        self.product_selected_state: VendingMachineState = ProductSelectedState()

        self.curr_state: VendingMachineState = None

        self.products: Dict[str, Product] = dict()
        self.qty: Dict[str, int] = dict()

        self.orders: List[VendingMachineOrder] = []


        self.current_order: VendingMachineOrder = None
        self.current_inserted_coins = 0

        # self.current_chosen_item: Product = None
        # self.current_chosen_item_qty: int = 0
        # self.current_target_coin: int = 0
        self.total_earnings: int = 0
    
    def initialise(self):
        self.curr_state = self.ready_state
    
    def start(self):
        print("Select one of the below options")
        
        break_ = False
        while not break_:
            print(f'\n{"="*20}')
            print(f"current state: {self.curr_state}")
            print(f"\nA: Add Product, \nL: List Stock, \nC: Choose Item, \nI: Insert Coin, \nD: Dispense Item, \nR: Refund/Cancel Item, \nQ: Quit\n{"="*20}\n")
            choice = input("Enter your choice: ").upper()
            if choice == "A":
                name = input("Enter product name: ")
                price = float(input("Enter product price: "))
                qty = int(input("Enter product quantity: "))
                self.add_product(Product(name, price), qty)
            elif choice == "L":
                self.list_stock()
            elif choice == "C":
                self.list_stock()
                product_id = input("Enter product id: ")
                qty = int(input("Enter product quantity: "))
                self.choose_item(product_id, qty)
            elif choice == "I":
                coin = int(input("Enter coin: "))
                self.insert_coin(coin)
            elif choice == "D":
                self.despense_item()
            elif choice == "R":
                self.cancel_transaction()
            elif choice == "Q":
                if self.curr_state != self.ready_state:
                    print("Please cancel or complete existing order...")
                else:
                    break_ = True
            else:
                print("Invalid choice")

    def add_product(self, product: Product, qty: int):
        self.products[product.id] = product
        self.qty[product.id] = self.qty.get(product.id, 0) + qty
    
    def remove_product(self, product_id: str, qty: int):
        if self.qty[product_id] < qty:
            raise Exception("Insufficient stock")
        self.qty[product_id] -= qty
        if self.qty[product_id] == 0:
            del self.products[product_id]
            del self.qty[product_id]
        

    def list_stock(self):
        
        if self.products:
            for key in self.products:
                print(f"id={self.products[key].id}, Name={self.products[key].name}, price={self.products[key].price}, qty={self.qty.get(key,0)}")
        else:
            print("No products in Vending Machine right now")

    def choose_item(self, product_id: str, qty: int) -> VendingMachineState:
        self.curr_state = self.curr_state.choose_item(self, product_id, qty)

    def insert_coin(self, coin: int):
        self.curr_state = self.curr_state.insert_coin(self, coin)

    def despense_item(self):
        self.curr_state = self.curr_state.dispense_item(self)

    def cancel_transaction(self):
        self.curr_state = self.curr_state.cancel_transaction(self)
