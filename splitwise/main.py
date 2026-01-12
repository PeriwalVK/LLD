import os
import sys


root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if root not in sys.path:
    sys.path.insert(0, root)

from splitwise.constants import DebtSimplificationType, SplitType
from splitwise.models.group import Group
from splitwise.models.splitwise import Splitwise
from splitwise.models.user import User

if __name__ == "__main__":
    splitwise = Splitwise()

    # greedy_simplification: DebtSimplificationStrategy = GreedyDebtSimplification()

    user0 = User("User 0")
    user1 = User("User 1")
    user2 = User("User 2")
    user3 = User("User 3")
    user4 = User("User 4")
    user5 = User("User 5")
    user6 = User("User 6")
    user7 = User("User 7")
    # user8 = User("User 8")
    # user9 = User("User 9")

    splitwise.add_user(user0)
    splitwise.add_user(user1)
    splitwise.add_user(user2)
    splitwise.add_user(user3)
    splitwise.add_user(user4)
    splitwise.add_user(user5)
    splitwise.add_user(user6)
    splitwise.add_user(user7)
    # splitwise.add_user(user8)
    # splitwise.add_user(user9)

    group0 = Group("H0000000li")
    group1 = Group("Diwal11111")

    splitwise.add_group(group0)
    splitwise.add_group(group1)

    splitwise.add_user_to_group(user0.id, group0.id)
    splitwise.add_user_to_group(user1.id, group0.id)
    splitwise.add_user_to_group(user2.id, group0.id)
    splitwise.add_user_to_group(user3.id, group0.id)
    splitwise.add_user_to_group(user4.id, group0.id)
    splitwise.add_user_to_group(user5.id, group0.id)
    splitwise.add_user_to_group(user6.id, group0.id)
    splitwise.add_user_to_group(user7.id, group0.id)
    # splitwise.add_user_to_group(user8.id, group0.id)
    # splitwise.add_user_to_group(user9.id, group0.id)

    splitwise.add_user_to_group(user0.id, group1.id)
    splitwise.add_user_to_group(user1.id, group1.id)
    splitwise.add_user_to_group(user2.id, group1.id)
    splitwise.add_user_to_group(user3.id, group1.id)
    splitwise.add_user_to_group(user4.id, group1.id)
    splitwise.add_user_to_group(user5.id, group1.id)
    splitwise.add_user_to_group(user6.id, group1.id)
    splitwise.add_user_to_group(user7.id, group1.id)
    # splitwise.add_user_to_group(user8.id, group1.id)
    # splitwise.add_user_to_group(user9.id, group1.id)

    ########################################## group 0 ##########################################

    ############################# CASE 1 ##############################################
    # splitwise.add_expense_to_group(
    #     group0.id, "Expense 40", 40, user4.id, SplitType.EQUAL, [user0.id, user4.id]
    # )
    # splitwise.add_expense_to_group(
    #     group0.id, "Expense 51", 60, user5.id, SplitType.EQUAL, [user1.id, user5.id]
    # )
    # splitwise.add_expense_to_group(
    #     group0.id, "Expense 62", 60, user6.id, SplitType.EQUAL, [user2.id, user6.id]
    # )
    # splitwise.add_expense_to_group(
    #     group0.id, "Expense 73", 60, user7.id, SplitType.EQUAL, [user3.id, user7.id]
    # )
    # splitwise.add_expense_to_group(
    #     group0.id, "Expense 75", 20, user7.id, SplitType.EQUAL, [user5.id, user7.id]
    # )

    ################################## CASE 2 (greedy always unoptimised) ###########################

    splitwise.add_expense_to_group(
        group0.id, "Expense 1-2", 40, user1.id, SplitType.EQUAL, [user2.id]
    )
    splitwise.add_expense_to_group(
        group0.id,
        "Expense 0-34",
        50,
        user0.id,
        SplitType.EXACT,
        [user3.id, user4.id],
        [30, 20],
    )

    #################################### CASE 3 ########################################
    # splitwise.add_expense_to_group(
    #     group0.id,
    #     "Expense 01",
    #     100,
    #     user0.id,
    #     SplitType.EXACT,
    #     [user0.id, user1.id, user2.id, user3.id],
    #     [1, 1, 1, 1],
    # )

    # splitwise.add_expense_to_group(
    #     group0.id,
    #     "Expense 02",
    #     100,
    #     user1.id,
    #     SplitType.PERCENTAGE,
    #     [user0.id, user2.id, user3.id, user4.id],
    #     [10, 20, 30, 40],
    # )

    group0.print_balances()
    print("")

    group0.simplify_debts(DebtSimplificationType.GREEDY)
    group0.print_balances()
    print("")

    group0.simplify_debts(DebtSimplificationType.OPTIMAL_BACKTRACKING)
    group0.print_balances()
    print("")

    ########################################################## group 1 ##########################################
    # # splitwise.add_expense_to_group(
    # #     group1.id,
    # #     "Expense n",
    # #     100,
    # #     user2.id,
    # #     SplitType.EXACT,
    # #     [user1.id, user2.id],
    # #     [80, 20],
    # # )
    # splitwise.add_expense_to_group(
    #     group1.id, "Expense 10", 100, user0.id, SplitType.EQUAL, [user0.id, user1.id]
    # )
    # splitwise.add_expense_to_group(
    #     group1.id,
    #     "Expense 11",
    #     100,
    #     user0.id,
    #     SplitType.EXACT,
    #     [user0.id, user1.id, user2.id, user3.id],
    #     [1, 1, 1, 1],
    # )

    # splitwise.add_expense_to_group(
    #     group1.id,
    #     "Expense 12",
    #     100,
    #     user1.id,
    #     SplitType.PERCENTAGE,
    #     [user0.id, user2.id, user3.id, user4.id],
    #     [10, 20, 30, 40],
    # )

    # # group1.print_balances()
    # # print("")

    ##############################################################################################

    # user0.print_balances()
    # user1.print_balances()
    # user2.print_balances()
    splitwise.print_balances(group=True, user=True)
