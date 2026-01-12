from typing import List
from splitwise.constants import ExpenseType, SplitType
from splitwise.strategy.split_strategy import SplitStrategy, SplitStrategyFactory


class Expense:
    _id = 0

    def __init__(
        self,
        description: str,
        expense_type: ExpenseType,
        amount: float,
        paid_by: str,
        split_type: SplitType,
        users: List[str],
        values: List[float] = None,
        group_id: str = None,
    ):
        self.id = Expense._id
        Expense._id += 1

        self.paid_by: str = paid_by
        self.amount: float = amount
        self.description: str = description

        self.expense_type: ExpenseType = expense_type

        self.split_type: SplitType = split_type
        self.values: List[float] = values

        self.users: List[str] = users
        self.splits: List[float] = self._calculate_splits()

        self.group_id: str = group_id

    def _calculate_splits(self):
        if self.expense_type == ExpenseType.EXPENSE:
            split_strategy: SplitStrategy = SplitStrategyFactory.get_split_strategy(self.split_type)
            return split_strategy.get_splits(self.amount, self.users, self.values)
        elif self.expense_type == ExpenseType.SETTLEMENT:
            return [self.amount]
        else:
            raise ValueError("Invalid expense type")

    def __str__(self):
        return f"Expense(id={self.id}, description={self.description}, amount={self.amount})"
