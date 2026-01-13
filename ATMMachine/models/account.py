class Account:
    def __init__(self, holder_name: str, number: str, balance: float):
        self.holder_name: str = holder_name
        self.number: str = number
        self.balance: float = balance