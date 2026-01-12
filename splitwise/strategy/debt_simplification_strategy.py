from abc import ABC, abstractmethod
from collections import defaultdict
import copy
from typing import Dict, List, override

from splitwise.constants import DebtSimplificationType


class DebtSimplificationStrategy(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def simplify_debts(
        self, balances: Dict[str, Dict[str, float]]
    ) -> Dict[str, Dict[str, float]]:
        pass


class GreedyDebtSimplification(DebtSimplificationStrategy):
    @override
    def __init__(self):
        super().__init__()
        self._positives: List[tuple[str, float]] = []
        self._negatives: List[tuple[str, float]] = []

        self._final_result: Dict[str, Dict[str, float]] = defaultdict(
            lambda: defaultdict(float)
        )

    @override
    def simplify_debts(
        self, balances: Dict[str, Dict[str, float]]
    ) -> Dict[str, Dict[str, float]]:
        _reverse_flag = (
            False  # when True then always unoptimised bcz smaller processed first
        )

        print("Simplifying debts using greedy...")

        for user_id in balances.keys():
            net_balance = sum(balances[user_id].values(), 0)
            if net_balance > 0:
                self._positives.append((user_id, net_balance))
            elif net_balance < 0:
                self._negatives.append((user_id, -net_balance))

        self._positives.sort(key=lambda x: x[1], reverse=_reverse_flag)
        self._negatives.sort(key=lambda x: x[1], reverse=_reverse_flag)

        # print(self._positives, self._negatives)

        while self._positives and self._negatives:
            pos_user, pos_balance = self._positives.pop()
            neg_user, neg_balance = self._negatives.pop()

            min_ = min(pos_balance, neg_balance)

            self._final_result[pos_user][neg_user] = min_
            self._final_result[neg_user][pos_user] = -min_

            if pos_balance > neg_balance:
                self._positives.append((pos_user, pos_balance - neg_balance))
                self._positives.sort(key=lambda x: x[1], reverse=_reverse_flag)
            elif pos_balance < neg_balance:
                self._negatives.append((neg_user, neg_balance - pos_balance))
                self._negatives.sort(key=lambda x: x[1], reverse=_reverse_flag)

            # print(self._positives, self._negatives)

        return self._final_result


class OptimalBacktrackingSimplification(DebtSimplificationStrategy):
    @override
    def __init__(self):
        super().__init__()
        self._positives: List[tuple[str, float]] = []
        self._negatives: List[tuple[str, float]] = []

        self._curr_balance: Dict[str, Dict[str, float]] = defaultdict(
            lambda: defaultdict(float)
        )
        self._curr_answer: Dict[str, Dict[str, float]] = defaultdict(
            lambda: defaultdict(float)
        )
        self._curr_cnt: int = 0
        self._curr_min_cnt = float("inf")

    def _solve(self, pos_visited: List[bool], neg_visited: List[bool]) -> int:
        if all(pos_visited) and all(neg_visited):
            if self._curr_cnt < self._curr_min_cnt:
                self._curr_min_cnt = self._curr_cnt
                # print(
                #     f"jhalak of balance while updating answer: {dict(self._curr_balance)}"
                # )
                self._curr_answer = copy.deepcopy(self._curr_balance)

        for i in range(len(self._positives)):
            if pos_visited[i]:
                continue

            for j in range(len(self._negatives)):
                if neg_visited[j]:
                    continue

                pos_user, pos_balance = self._positives[i]
                neg_user, neg_balance = self._negatives[j]

                min_ = min(pos_balance, neg_balance)

                self._curr_balance[pos_user][neg_user] = min_
                self._curr_balance[neg_user][pos_user] = -min_

                if pos_balance < neg_balance:
                    pos_visited[i] = True
                    self._negatives[j] = (neg_user, neg_balance - pos_balance)
                elif pos_balance > neg_balance:
                    neg_visited[j] = True
                    self._positives[i] = (pos_user, pos_balance - neg_balance)
                else:
                    pos_visited[i] = True
                    neg_visited[j] = True

                self._curr_cnt += 1
                self._solve(pos_visited, neg_visited)
                self._curr_cnt -= 1

                pos_visited[i] = False
                neg_visited[j] = False
                self._positives[i] = (pos_user, pos_balance)
                self._negatives[j] = (neg_user, neg_balance)

                del self._curr_balance[pos_user][neg_user]
                del self._curr_balance[neg_user][pos_user]

    @override
    def simplify_debts(
        self, balances: Dict[str, Dict[str, float]]
    ) -> Dict[str, Dict[str, float]]:
        print("Simplifying debts using optimal backtracking...Time complexity O(n!)")

        for user_id in balances.keys():
            net_balance = sum(balances[user_id].values(), 0)
            if net_balance > 0:
                self._positives.append((user_id, net_balance))
            elif net_balance < 0:
                self._negatives.append((user_id, -net_balance))

        self._positives.sort(key=lambda x: x[1])
        self._negatives.sort(key=lambda x: x[1])

        pos_visited: List[bool] = [False for _ in self._positives]
        neg_visited: List[bool] = [False for _ in self._negatives]

        self._solve(pos_visited, neg_visited)

        return self._curr_answer


class DebtSimplificationStrategyFactory:
    @staticmethod
    def get_debt_simplification_strategy(
        type: DebtSimplificationType,
    ) -> DebtSimplificationStrategy:
        if type == DebtSimplificationType.GREEDY:
            return GreedyDebtSimplification()
        elif type == DebtSimplificationType.OPTIMAL_BACKTRACKING:
            return OptimalBacktrackingSimplification()
        else:
            return GreedyDebtSimplification()  # default
