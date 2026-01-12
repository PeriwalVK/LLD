from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, override


class Observer(ABC):
    @abstractmethod
    def receive_notification(self, message: str) -> None:
        pass


class User(Observer):
    _id = 0

    def __init__(self, name: str):
        self.id: str = str(User._id)
        User._id += 1

        self.name = name
        self.balances: Dict[str, float] = defaultdict(float)  # user id to amount

    def __str__(self):
        return f"User(id={self.id}, name={self.name})"

    @override
    def receive_notification(self, message):
        print(f"[Notified {self.name}]: <{message}>")

    def update_balance(self, user_id: str, amount: float):
        self.balances[user_id] += amount
        if self.balances[user_id] == 0:
            del self.balances[user_id]

    def get_balance(self, user_id: str) -> float:
        return self.balances[user_id]

    def print_balances(self):
        print(
            f"Balances for user {self}: NET {sum(self.balances.values(), 0)} : {dict(self.balances)}"
        )
