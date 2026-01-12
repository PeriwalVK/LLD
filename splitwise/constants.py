from enum import Enum


class SplitType(Enum):
    EQUAL = "EQUAL"
    EXACT = "EXACT"
    PERCENTAGE = "PERCENTAGE"

class DebtSimplificationType(Enum):
    GREEDY = "GREEDY"
    OPTIMAL_BACKTRACKING = "OPTIMAL_BACKTRACKING"
    

class ExpenseType(Enum):
    EXPENSE = "EXPENSE"
    SETTLEMENT = "SETTLEMENT"