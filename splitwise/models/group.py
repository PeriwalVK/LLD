from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from email.policy import default
from turtle import pos
from typing import Dict, List, override

from splitwise.constants import DebtSimplificationType, ExpenseType, SplitType
from splitwise.models.expense import Expense
from splitwise.models.user import User
from splitwise.strategy.debt_simplification_strategy import (
    DebtSimplificationStrategy,
    DebtSimplificationStrategyFactory,
)


class Observable(ABC):
    """
    Could have also implemented below methods but User itself is observer
    and methods to add remove users will be already there in Group class
    so directly implement krdo
    """

    # @abstractmethod
    # def add_observer(self, observer):
    #     pass

    # @abstractmethod
    # def remove_observer(self, observer):
    #     pass

    @abstractmethod
    def notify_observers(self, message):
        pass


class Group(Observable):
    _id = 0

    def __init__(self, name: str):
        self.id = str(Group._id)
        Group._id += 1
        self.name = name

        self.expenses: Dict[str, Expense] = dict()

        self.users: Dict[str, User] = dict()
        # self.balances: Dict[str, Dict[str, float]] = dict()
        self.balances: Dict[str, Dict[str, float]] = defaultdict(
            lambda: defaultdict(float)
        )

    def __str__(self):
        return f"Group(id={self.id}, name={self.name})"

    @override
    def notify_observers(self, message):
        for user in self.users.values():
            user.receive_notification(message)

    def add_user(self, user: User):
        if user.id not in self.users:
            self.users[user.id] = user
            # self.balances[user.id] = dict()
        else:
            print(f"user {user} already exists in group {self}")

    def remove_user(self, user_id: str) -> bool:
        if user_id not in self.users:
            print(f"user with id {user_id} does not exist in group {self}")
            return False

        for each in self.balances[user_id].values():
            if each != 0:
                print(
                    f"Can't remove user {self.users[user_id]} - has outstanding balances"
                )
                return False

        del self.users[user_id]
        del self.balances[user_id]
        return True
        # for balances in self.balances.values():
        #     if user_id in balances:
        #         del balances[user_id]

    def _add_to_balances(self, expense: Expense):
        # self.balances[expense.paid_by] = self.balances.get(expense.paid_by, dict())

        for user_id, amount in zip(expense.users, expense.splits):
            if user_id == expense.paid_by:
                continue

            self.balances[expense.paid_by][user_id] += amount
            if self.balances[expense.paid_by][user_id] == 0:
                del self.balances[expense.paid_by][user_id]
            if not self.balances[expense.paid_by]:
                del self.balances[expense.paid_by]
            self.users[expense.paid_by].update_balance(user_id, amount)

            self.balances[user_id][expense.paid_by] -= amount
            if self.balances[user_id][expense.paid_by] == 0:
                del self.balances[user_id][expense.paid_by]
            if not self.balances[user_id]:
                del self.balances[user_id]
            self.users[user_id].update_balance(expense.paid_by, -amount)

    def add_expense(
        self,
        description: str,
        amount: float,
        paid_by: str,
        split_type: SplitType,
        users: List[str],
        values: List[float] = None,
    ):
        expense = Expense(
            description,
            ExpenseType.EXPENSE,
            amount,
            paid_by,
            split_type,
            users,
            values,
            self.id,
        )
        self.expenses[expense.id] = expense
        self._add_to_balances(expense)
        self.notify_observers(f"new expense was added to group {self.name}: {expense}")

    def settle_expense(
        self,
        paid_by: str,
        paid_to: str,
        amount: float,
    ):
        expense = Expense(
            "Settlement",
            ExpenseType.SETTLEMENT,
            amount,
            paid_by,
            None,
            [paid_to],
            None,
            self.id,
        )
        self.expenses[expense.id] = expense
        self._add_to_balances(expense)

    def simplify_debts(
        self, type: DebtSimplificationType = DebtSimplificationType.GREEDY
    ):
        final_result: Dict[str, Dict[str, float]] = (
            DebtSimplificationStrategyFactory.get_debt_simplification_strategy(
                type
            ).simplify_debts(self.balances)
        )
        self._update_users_balances(self.balances, final_result)
        self.balances = final_result

    def _update_users_balances(
        self,
        old_balances: Dict[str, Dict[str, float]],
        new_balances: Dict[str, Dict[str, float]],
    ):
        # userid_set = old_balances.keys() | new_balances.keys()
        for user_id in old_balances.keys() | new_balances.keys():
            balances_diff = Counter(new_balances.get(user_id, dict()))
            balances_diff.subtract(Counter(old_balances.get(user_id, dict())))

            for uid in balances_diff:
                self.users[user_id].update_balance(uid, balances_diff[uid])

    def print_balances(self):
        print(f"\n Balances for group {self}:")
        for user_id in self.balances:
            print(
                f"{self.users[user_id]}: NET {sum(self.balances[user_id].values(), 0)} : {dict(self.balances[user_id])}"
            )

    def _is_fully_settled(self) -> bool:
        for balance in self.balances.values():
            for amount in balance.values():
                if amount != 0:
                    return False
        return True
