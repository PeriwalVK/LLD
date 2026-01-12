from abc import ABC, abstractmethod
from typing import List, override

from splitwise.constants import SplitType


class SplitStrategy(ABC):
    @abstractmethod
    def __init__(self, split_type: SplitType):
        self.split_type = split_type

    @abstractmethod
    def get_splits(
        self, amount: float, users: List[str], values: List[float]
    ) -> List[float]:
        pass


class EqualSplitStrategy(SplitStrategy):
    @override
    def __init__(self):
        super().__init__(SplitType.EQUAL)

    @override
    def get_splits(
        self, amount: float, users: List[str], values: List[float]
    ) -> List[float]:
        return [amount / len(users)] * len(users)


class ExactSplitStrategy(SplitStrategy):
    @override
    def __init__(self):
        super().__init__(SplitType.EXACT)

    @override
    def get_splits(
        self, amount: float, users: List[str], values: List[float]
    ) -> List[float]:
        _sum_values = sum(values)
        return [(value / _sum_values) * amount for value in values]
        # return values


class PercentageSplitStrategy(SplitStrategy):
    @override
    def __init__(self):
        super().__init__(SplitType.PERCENTAGE)

    @override
    def get_splits(
        self, amount: float, users: List[str], values: List[float]
    ) -> List[float]:
        return [(value / 100) * amount for value in values]


class SplitStrategyFactory:
    _equal_split_strategy = EqualSplitStrategy()
    _exact_split_strategy = ExactSplitStrategy()
    _percentage_split_strategy = PercentageSplitStrategy()

    def get_split_strategy(split_type: SplitType):
        if split_type == SplitType.EQUAL:
            return SplitStrategyFactory._equal_split_strategy
        elif split_type == SplitType.EXACT:
            return SplitStrategyFactory._exact_split_strategy
        elif split_type == SplitType.PERCENTAGE:
            return SplitStrategyFactory._percentage_split_strategy
        else:
            # raise ValueError("Invalid split type")
            return SplitStrategyFactory._equal_split_strategy  # default


