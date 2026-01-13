from ATMMachine.models.account import Account


class Card:
    _id = 0

    def __init__(self, number: str, pin: str, account: Account):
        self.id = str(Card._id)
        Card._id += 1
        
        self.number: str = number
        self.pin: str = pin
        self.account: Account = account
    
    def __str__(self):
        return f"Card(id={self.id},number={self.number})"
