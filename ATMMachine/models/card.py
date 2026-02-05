from typing import Callable
from ATMMachine.models.account import Account


class Card:
    _id = 0

    def __init__(self, number: str, pin: str, account: Account):
        self.id = str(Card._id)
        Card._id += 1

        self._hash_fn: Callable = (
            hash  # could have also used Argon2 or Bcrypt for better pw safety
        )
        self.number: str = number
        self._hashed_pin: str = self._hash_fn(pin)

        self.account: Account = account

    def __str__(self):
        return f"Card(id={self.id},number={self.number})"

    def auth(self, pin: str) -> bool:
        return self._hashed_pin == self._hash_fn(pin)
