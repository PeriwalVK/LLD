import os
import sys


root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if root not in sys.path:
    sys.path.insert(0, root)


if __name__ == "__main__":
    from vending_machine.models.product import Product
    from vending_machine.models.vending_machine import VendingMachine

    v = VendingMachine()

    # coke = Product("COKE", 50)
    # chips = Product("CHIPS", 20)
    # yogurt = Product("YOGURT", 30)
    # ice_cream = Product("ICE_CREAM", 40)

    # v.add_product(coke, 10)
    # v.add_product(chips, 10)
    # v.add_product(yogurt, 10)
    # v.add_product(ice_cream, 10)

    # v.list_stock()





    v.initialise()
    v.start()
