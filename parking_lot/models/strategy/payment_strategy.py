from abc import ABC


class PaymentStrategy(ABC):
    def __init__(self):
        pass

    def make_payment(self, amount):
        pass

class CashPaymentStrategy(PaymentStrategy):
    def __init__(self):
        super().__init__()
    
    def make_payment(self, amount):
        print(f"[CashPaymentStrategy]: Paid ${amount} using cash.")


class UPIPaymentStrategy(PaymentStrategy):
    def __init__(self):
        super().__init__()
    
    def make_payment(self, amount):
        print(f"[UPIPaymentStrategy]: Paid ${amount} using UPI.")

class CardPaymentStrategy(PaymentStrategy):
    def __init__(self):
        super().__init__()
    
    def make_payment(self, amount):
        print(f"[CardPaymentStrategy]: Paid ${amount} using Card.")