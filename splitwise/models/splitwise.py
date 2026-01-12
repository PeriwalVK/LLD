from typing import Dict, List
from splitwise.constants import SplitType
from splitwise.models.group import Group
from splitwise.models.user import User


class Splitwise:
    def __init__(self):
        self.groups: Dict[str, Group] = dict()
        self.users: dict[str, User] = dict()

    def get_group(self, group_id: str):
        if group_id not in self.groups:
            print(f"group with id {group_id} does not exist in splitwise")
            return
        return self.groups[group_id]

    def add_group(self, group: Group):
        self.groups[group.id] = group

    def remove_group(self, group_id: str):
        group = self.get_group(group_id)
        if group._is_fully_settled():
            print(f"Group {self} is fully settled -> deleting...")
            del self.groups[group_id]
        else:
            print(f"Group {self} is NOT fully settled -> CAN NOT DELETE")

    def get_user(self, user_id: str):
        if user_id not in self.users:
            print(f"user with id {user_id} does not exist in splitwise")
            return
        return self.users[user_id]

    def add_user(self, user: User):
        self.users[user.id] = user

    def add_user_to_group(self, user_id: str, group_id: str):
        group = self.get_group(group_id)
        user = self.get_user(user_id)
        if group and user:
            group.add_user(user)

    def remove_user_from_group(self, user_id: str, group_id: str):
        group = self.get_group(group_id)
        user = self.get_user(user_id)
        if group and user:
            group.remove_user(user)

    def add_expense_to_group(
        self,
        group_id: str,
        description: str,
        amount: float,
        paid_by: str,
        split_type: SplitType,
        users: List[str],
        values: List[float] = None,
    ):
        group = self.get_group(group_id)
        if group:
            group.add_expense(description, amount, paid_by, split_type, users, values)

    def print_balances(self, group=False, user=False):
        if group:
            for each_group in self.groups.values():
                each_group.print_balances()
        if user:
            print("\n")
            for each_user in self.users.values():
                each_user.print_balances()
