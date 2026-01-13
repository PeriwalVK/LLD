from collections import defaultdict
from typing import Dict

from ATMMachine.constants import NoteType
from ATMMachine.models.card import Card
from ATMMachine.models.card_manager import CardManager
from ATMMachine.state.atm_state import (
    ATMState,
    CardInsertedState,
    IDLEState,
    PinAuthenticatedState,
)


class ATMMachine:
    _id = 0

    def __init__(self):
        self.id = str(ATMMachine._id)
        ATMMachine._id += 1

        self.cash: Dict[NoteType, int] = defaultdict(int)
        self.balance: int = 0

        self._idle_state: ATMState = IDLEState(self)
        self._card_inserted_state: ATMState = CardInsertedState(self)
        self._pin_authenticated_state: ATMState = PinAuthenticatedState(self)
        self._curr_state: ATMState = self._idle_state

        self._current_card_id: str = None

        self.card_manager: CardManager = CardManager()

    def __str__(self):
        return f"ATMMachine(id={self.id})"

    def add_cash(self, note_type: NoteType, count: int):
        self.cash[note_type] += count
        self.balance += note_type.value * count

    def get_note_count(self, note_type: NoteType):
        return self.cash[note_type]

    def remove_cash(self, note_type: NoteType, count: int):
        self.cash[note_type] -= count
        self.balance -= note_type.value * count

    # def _set_card(self, card: Card):
    #     self._state.set_card(self, card)

    def _set_current_card(self, card_id: str) -> bool:
        if not self.card_manager.is_valid_card(card_id):
            return False
        self._current_card_id = card_id
        return True

    def _unset_current_card(self):
        self._current_card_id = None

    def insert_card(self, card_id: str):
        self._curr_state = self._curr_state.insert_card(card_id)

    def insert_pin(self, pin: str):
        self._curr_state = self._curr_state.insert_pin(pin)

    def withdraw(self, amount: int):
        self._curr_state = self._curr_state.withdraw(amount)

    def remove_card(self):
        self._curr_state = self._curr_state.remove_card()
