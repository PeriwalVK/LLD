import os
import sys


root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if root not in sys.path:
    sys.path.insert(0, root)

from ATMMachine.constants import NoteType
from ATMMachine.models.account import Account
from ATMMachine.models.atm_machine import ATMMachine
from ATMMachine.models.atm_manager import ATMMachineManager
from ATMMachine.models.card import Card
from ATMMachine.models.card_manager import CardManager


if __name__ == "__main__":
    _card_number = "123456"
    _card_pin = "1234"
    _wrong_pin = "5678"
    _account_bal = 10000000

    _atm_cash_composition = {
        NoteType.NOTE_100: 0,
        NoteType.NOTE_200: 3,
        NoteType.NOTE_500: 2,
        NoteType.NOTE_2000: 0,
    }

    card: Card = Card(
        _card_number, _card_pin, Account("John Doe", "acc_123456", _account_bal)
    )

    card_manager = CardManager()  # is singleton

    # cm2 = CardManager()
    # print(card_manager is cm2)
    card_manager.add_card(card)
    # print(card_manager)

    atm_manager = ATMMachineManager()

    atm = ATMMachine()
    atm_manager.add_atm(atm)

    for note_type, count in _atm_cash_composition.items():
        atm_manager.add_cash(atm.id, note_type, count)
    # atm_manager.add_cash(atm.id, NoteType.NOTE_100, 10)
    # atm_manager.add_cash(atm.id, NoteType.NOTE_200, 10)
    # atm_manager.add_cash(atm.id, NoteType.NOTE_500, 10)
    # atm_manager.add_cash(atm.id, NoteType.NOTE_2000, 10)

    print("########################## IDLE STATE ##########################")
    atm_manager.insert_pin(atm.id, _card_pin)
    atm_manager.withdraw(atm.id, 1000)
    atm_manager.remove_card(atm.id)
    atm_manager.insert_card(atm.id, card.id)

    print("########################## Card Inserted State ##########################")
    atm_manager.insert_card(atm.id, card.id)
    atm_manager.withdraw(atm.id, 1000)
    atm_manager.remove_card(atm.id)
    atm_manager.insert_card(atm.id, card.id)

    atm_manager.insert_pin(atm.id, _wrong_pin)
    atm_manager.insert_pin(atm.id, _card_pin)

    print("########################## PIN Inserted State ##########################")
    atm_manager.insert_card(atm.id, card.id)
    atm_manager.insert_pin(atm.id, _card_pin)
    atm_manager.remove_card(atm.id)
    atm_manager.insert_card(atm.id, card.id)
    atm_manager.insert_pin(atm.id, _card_pin)

    atm_manager.withdraw(atm.id, _account_bal + 1000)
    atm_manager.withdraw(atm.id, atm.balance + 1)
    atm_manager.withdraw(
        atm.id, 1100
    )
    print(atm.cash)

    atm_manager.insert_card(atm.id, card.id)
    atm_manager.insert_pin(atm.id, _card_pin)
    atm_manager.withdraw(
        atm.id, 500
    )
    print(atm.cash)

    # atm_manager.insert_pin(atm.id, _card_pin)
    # atm_manager.insert_pin(atm.id, _card_pin)

    # print(atm.card_manager)
